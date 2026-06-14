#!/usr/bin/env python3
"""P1 통일 전처리 — 공통 branch (DESIGN §3).

raw 2 sample(CellRanger ARC: GEX+Peaks 통합 matrix + velocyto loom)
  → GEX/Peaks 분리 → per-sample QC(+doublet) → spliced/unspliced 병합
  → 두 timepoint 결합(per-cell day0/day7 라벨) → 공통 정규화/HVG/neighbor graph
  → method-agnostic Leiden annotation → 통합 MuData 저장.

이 산출물이 "공통까지 동일, 이후 method-specific 분기"의 기준점(DESIGN §3, C2 대응).

실행 (scv-preprocess env):
  conda run -n scv-preprocess python pipeline/hspc-velocity-benchmark/scripts/p1_build.py

⚠️ 스캐폴딩: 핵심 흐름은 구현했으나 (a) QC 임계값(p1_config.QC), (b) loom↔ARC barcode
   매칭, (c) ATAC 정규화 방식은 raw 분포 확인 후 조정 필요(TODO 표시).
"""
from __future__ import annotations
import sys
import scanpy as sc
import numpy as np
import p1_config as cfg


def load_sample(name: str, info: dict):
    """CellRanger ARC matrix(GEX+Peaks) + velocyto loom 로드, GEX/Peaks 분리,
    spliced/unspliced 병합, timepoint 라벨 부여."""
    d = info["dir"]
    print(f"[{name}] load {d}")
    # sc.read_10x_mtx: matrix.mtx.gz + features.tsv.gz + barcodes.tsv.gz 필요.
    # 파일명이 그대로(barcodes/features/matrix)여야 함. gex_only=False로 Peaks도 로드.
    adata = sc.read_10x_mtx(d, gex_only=False, cache=False)
    adata.var_names_make_unique()
    ft = adata.var["feature_types"].astype(str)
    rna = adata[:, ft == "Gene Expression"].copy()
    atac = adata[:, ft == "Peaks"].copy()
    for a in (rna, atac):
        a.obs["sample"] = name
        a.obs["timepoint"] = info["timepoint"]
        a.obs_names = [f"{name}_{bc}" for bc in a.obs_names]   # sample prefix로 충돌 방지
    print(f"  RNA {rna.shape}, ATAC {atac.shape}")

    # spliced/unspliced 병합 (velocyto loom)
    try:
        import scvelo as scv
        loom = d / "gex.loom"
        if not loom.exists():
            # .gz면 먼저 gunzip 필요 — README 참고
            print(f"  ⚠ {loom} 없음 (gex.loom.gz 압축 해제 필요). spliced/unspliced 생략.")
        else:
            ldata = scv.read(str(loom), cache=False)
            ldata.var_names_make_unique()
            # scvelo merge가 barcode 정리(접두/접미 제거) 후 spliced/unspliced layer 이식.
            # TODO: barcode 형식이 안 맞으면 scv.utils.clean_obs_names로 양쪽 정규화.
            rna = scv.utils.merge(rna, ldata)
            print(f"  spliced/unspliced 병합 후 RNA {rna.shape}, layers={list(rna.layers)}")
    except Exception as e:
        print(f"  ⚠ loom 병합 실패({e}). P1에서 barcode 매칭 수동 확인 필요.")
    return rna, atac


def qc_sample(rna, atac, name: str):
    """per-sample QC + doublet (merge 전에 sample 단위로)."""
    q = cfg.QC
    sc.pp.calculate_qc_metrics(rna, inplace=True, percent_top=None)
    rna.var["mito"] = rna.var_names.str.upper().str.startswith("MT-")
    if rna.var["mito"].any():
        rna.obs["pct_mito"] = (
            np.asarray(rna[:, rna.var["mito"]].X.sum(1)).ravel()
            / np.asarray(rna.X.sum(1)).ravel() * 100
        )
    else:
        rna.obs["pct_mito"] = 0.0
    n0 = rna.n_obs
    sc.pp.filter_cells(rna, min_genes=q["min_genes_per_cell"])
    rna = rna[(rna.obs["n_genes_by_counts"] <= q["max_genes_per_cell"])
              & (rna.obs["pct_mito"] <= q["max_pct_mito"])].copy()
    print(f"[{name}] RNA QC: {n0} → {rna.n_obs} cells")

    # doublet (scrublet) — per sample
    if q["doublet_method"] == "scrublet":
        try:
            sc.pp.scrublet(rna)   # adds obs['predicted_doublet']
            rna = rna[~rna.obs["predicted_doublet"]].copy()
            print(f"[{name}] doublet 제거 후 {rna.n_obs} cells")
        except Exception as e:
            print(f"  ⚠ scrublet 실패({e}) — 건너뜀, 추후 확인")

    # ATAC를 RNA의 통과 cell로 맞춤
    atac = atac[atac.obs_names.isin(rna.obs_names)].copy()
    return rna, atac


def build():
    cfg.OUT.mkdir(parents=True, exist_ok=True)
    sc.settings.verbosity = 1
    rnas, atacs = [], []
    for name, info in cfg.SAMPLES.items():
        rna, atac = load_sample(name, info)
        rna, atac = qc_sample(rna, atac, name)
        rnas.append(rna); atacs.append(atac)

    # 두 timepoint 결합 (per-cell timepoint 라벨 보존)
    rna = sc.concat(rnas, join="inner", label="batch", keys=list(cfg.SAMPLES))
    atac = sc.concat(atacs, join="inner", label="batch", keys=list(cfg.SAMPLES))
    rna.obs_names_make_unique(); atac.obs_names_make_unique()
    print(f"결합: RNA {rna.shape}, ATAC {atac.shape}  (목표 ~11,605 cells 근처)")

    # 공통 RNA 정규화 + HVG + neighbor graph (shared-graph ablation 기준)
    rna.layers["counts"] = rna.X.copy()
    sc.pp.normalize_total(rna, target_sum=1e4)
    sc.pp.log1p(rna)
    sc.pp.highly_variable_genes(rna, n_top_genes=cfg.N_HVG)
    sc.pp.pca(rna, n_comps=cfg.N_PCS, random_state=cfg.RANDOM_SEED)
    sc.pp.neighbors(rna, n_neighbors=cfg.N_NEIGHBORS, random_state=cfg.RANDOM_SEED)

    # method-agnostic annotation (DESIGN §3: velocity 실행 전 freeze)
    sc.tl.leiden(rna, resolution=cfg.LEIDEN_RES, random_state=cfg.RANDOM_SEED, key_added="leiden")
    # TODO: marker 기반 lineage 라벨(erythroid/myeloid/lymphoid/MK) 매핑 → rna.obs['lineage']
    #       (HSPC marker: GATA1/KLF1 erythroid, SPI1/MPO myeloid, etc.) — 별도 annotate 단계.
    print(f"Leiden clusters: {rna.obs['leiden'].nunique()}")

    # ATAC: 정규화 (TODO: TF-IDF/LSI vs normalize_total — method 요구에 맞춰 결정)
    sc.pp.normalize_total(atac, target_sum=1e4)
    sc.pp.log1p(atac)

    # 저장
    rna.write_h5ad(cfg.OUT_RNA)
    atac.write_h5ad(cfg.OUT_ATAC)
    try:
        import mudata as md
        mdata = md.MuData({"rna": rna, "atac": atac})
        mdata.write(str(cfg.OUT_MUDATA))
        print(f"✓ saved MuData → {cfg.OUT_MUDATA}")
    except Exception as e:
        print(f"⚠ MuData 저장 실패({e}); rna/atac h5ad는 저장됨.")
    print(f"✓ RNA → {cfg.OUT_RNA}\n✓ ATAC → {cfg.OUT_ATAC}")
    print("다음: check_data.py 로 검증 → method-specific 실행(P2)")


if __name__ == "__main__":
    sys.exit(build())
