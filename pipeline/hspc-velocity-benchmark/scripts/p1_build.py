#!/usr/bin/env python3
"""P1 통일 전처리 — 공통 branch (DESIGN §3), MultiVelo 표준 multiome 전처리 기반.

raw 2 sample(CellRanger ARC: GEX+Peaks matrix + velocyto loom)
  → GEX/Peaks 분리
  → RNA: velocyto loom의 spliced/unspliced 이식 (anndata.read_loom + barcode 매칭)
  → ATAC: multivelo.aggregate_peaks_10x 로 peak→**gene-level** 집계
          (peak_annotation + feature_linkage 사용; sample 간 gene 축 공통 → 결합 가능)
  → per-sample QC(+doublet) → 두 timepoint 결합(day0/day7 라벨)
  → 공통 정규화/HVG/neighbor graph → method-agnostic Leiden → 통합 MuData 저장.

실행 (scv-preprocess env; multivelo 필요):
  conda run -n scv-preprocess pip install multivelo   # 최초 1회
  conda run -n scv-preprocess python pipeline/hspc-velocity-benchmark/scripts/p1_build.py

⚠️ 이전 버그 수정본: (1) scvelo.read → anndata.read_loom, (2) ATAC raw-peak inner-join(62 peak로
   붕괴) → gene-level 집계로 교체. barcode/파일 형식에 따라 1회 iteration 필요할 수 있음(로그 확인).
"""
from __future__ import annotations
import sys
import numpy as np
import scanpy as sc
import anndata as ad
import p1_config as cfg


def _core_barcodes(names):
    """velocyto/ARC barcode를 16bp core로 정규화. 'prefix:AAAC...x' 또는 'AAAC...-1' → 'AAAC...'."""
    out = []
    for b in map(str, names):
        b = b.split(":")[-1]          # velocyto prefix 제거
        if b.endswith("x"):
            b = b[:-1]                # velocyto 'x' 제거
        b = b.split("-")[0]           # '-1' suffix 제거
        out.append(b)
    return out


def merge_loom(rna, loom_path, name):
    """spliced/unspliced를 rna에 이식 (core-barcode + gene 교집합 매칭)."""
    if not loom_path.exists():
        print(f"  ⚠ {loom_path} 없음 → spliced/unspliced 생략 (velocity 불가). gex.loom.gz 압축 해제 필요.")
        return rna
    ldata = ad.read_loom(str(loom_path))
    ldata.var_names_make_unique()
    ldata.obs_names = _core_barcodes(ldata.obs_names)
    ldata = ldata[~ldata.obs_names.duplicated()].copy()
    # set을 루프 밖으로 hoist (안에 두면 매 iteration마다 재구축 → O(n²)).
    lvar, lobs = set(ldata.var_names), set(ldata.obs_names)
    gshared = [g for g in rna.var_names if g in lvar]
    cshared = [c for c in rna.obs_names if c in lobs]
    if not cshared or not gshared:
        print(f"  ⚠ loom 매칭 0 (cells {len(cshared)}, genes {len(gshared)}) → spliced/unspliced 생략")
        return rna
    rna = rna[cshared, gshared].copy()
    ldata = ldata[cshared, gshared].copy()
    for lyr in ("spliced", "unspliced"):
        if lyr in ldata.layers:
            rna.layers[lyr] = ldata.layers[lyr].copy()
    print(f"  loom merge: RNA {rna.shape}, layers={list(rna.layers)} (cells {len(cshared)}, genes {len(gshared)})")
    return rna


def aggregate_atac(atac, d, name):
    """multivelo.aggregate_peaks_10x로 peak→gene 집계 → sample 간 공통 gene 축."""
    try:
        import multivelo as mv
        # multivelo 0.1.5 시그니처: (adata_atac, peak_annot_file, linkage_file,
        #   peak_dist=10000, min_corr=0.5, gene_body=False, return_dict=False, parallel=False, n_jobs=1)
        # 'verbose' 인자 없음 — 넘기면 TypeError.
        agg = mv.aggregate_peaks_10x(
            atac,
            str(d / "peak_annotation.tsv.gz"),
            str(d / "feature_linkage.bedpe.gz"),
        )
        print(f"  ATAC peak→gene: {atac.shape} → {agg.shape}")
        return agg
    except Exception as e:
        print(f"  ⚠ ATAC 집계 실패({e}). multivelo 설치 + peak_annotation/feature_linkage(.gz) 확인 필요.")
        print(f"     (raw peak 유지 시 sample 간 peak 불일치로 결합 불가 — 집계 성공해야 함)")
        return atac


def load_sample(name, info):
    d = info["dir"]
    print(f"[{name}] load {d}")
    adata = sc.read_10x_mtx(d, gex_only=False, cache=False)
    adata.var_names_make_unique()
    ft = adata.var["feature_types"].astype(str)
    rna = adata[:, ft == "Gene Expression"].copy()
    atac = adata[:, ft == "Peaks"].copy()
    # obs_names를 core barcode로 통일 (rna/atac/loom 매칭 일관성)
    rna.obs_names = _core_barcodes(rna.obs_names)
    atac.obs_names = _core_barcodes(atac.obs_names)
    rna = rna[~rna.obs_names.duplicated()].copy()
    atac = atac[~atac.obs_names.duplicated()].copy()
    print(f"  RNA {rna.shape}, ATAC(peaks) {atac.shape}")
    rna = merge_loom(rna, d / "gex.loom", name)
    atac = aggregate_atac(atac, d, name)
    for a in (rna, atac):
        a.obs["sample"] = name
        a.obs["timepoint"] = info["timepoint"]
        a.obs_names = [f"{name}_{bc}" for bc in a.obs_names]
    return rna, atac


def qc_sample(rna, atac, name):
    q = cfg.QC
    sc.pp.calculate_qc_metrics(rna, inplace=True, percent_top=None)
    rna.var["mito"] = rna.var_names.str.upper().str.startswith("MT-")
    if rna.var["mito"].any():
        rna.obs["pct_mito"] = (np.asarray(rna[:, rna.var["mito"]].X.sum(1)).ravel()
                               / np.asarray(rna.X.sum(1)).ravel() * 100)
    else:
        rna.obs["pct_mito"] = 0.0
    n0 = rna.n_obs
    sc.pp.filter_cells(rna, min_genes=q["min_genes_per_cell"])
    rna = rna[(rna.obs["n_genes_by_counts"] <= q["max_genes_per_cell"])
              & (rna.obs["pct_mito"] <= q["max_pct_mito"])].copy()
    print(f"[{name}] RNA QC: {n0} → {rna.n_obs} cells")
    if q["doublet_method"] == "scrublet":
        try:
            sc.pp.scrublet(rna)
            rna = rna[~rna.obs["predicted_doublet"]].copy()
            print(f"[{name}] doublet 제거 후 {rna.n_obs} cells")
        except Exception as e:
            print(f"  ⚠ scrublet 실패({e}) — 건너뜀")
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

    # 결합: RNA/ATAC 모두 gene 축 inner-join (ATAC도 이제 gene-level → 공통 gene 다수)
    rna = sc.concat(rnas, join="inner", label="batch", keys=list(cfg.SAMPLES))
    atac = sc.concat(atacs, join="inner", label="batch", keys=list(cfg.SAMPLES))
    rna.obs_names_make_unique(); atac.obs_names_make_unique()
    print(f"결합: RNA {rna.shape}, ATAC(gene-level) {atac.shape}")
    if "spliced" not in rna.layers:
        print("  ⚠ 경고: spliced/unspliced layer 없음 → velocity(P2) 불가. loom 매칭 점검 필요.")
    if atac.n_vars < 100:
        print(f"  ⚠ 경고: ATAC gene 수 {atac.n_vars} 비정상 — 집계 실패 가능. P2 전 점검.")

    # 공통 RNA 정규화 + HVG + neighbor graph (counts/spliced/unspliced layer 보존)
    rna.layers["counts"] = rna.X.copy()
    sc.pp.normalize_total(rna, target_sum=1e4)
    sc.pp.log1p(rna)
    sc.pp.highly_variable_genes(rna, n_top_genes=cfg.N_HVG)
    sc.pp.pca(rna, n_comps=cfg.N_PCS, random_state=cfg.RANDOM_SEED)
    sc.pp.neighbors(rna, n_neighbors=cfg.N_NEIGHBORS, random_state=cfg.RANDOM_SEED)
    sc.tl.leiden(rna, resolution=cfg.LEIDEN_RES, random_state=cfg.RANDOM_SEED, key_added="leiden")
    print(f"Leiden clusters: {rna.obs['leiden'].nunique()}")
    # TODO: marker 기반 lineage 라벨(GATA1/KLF1 erythroid, SPI1/MPO myeloid 등) → rna.obs['lineage']

    # ATAC(gene-level) 정규화 (TODO: multivelo tfidf_norm vs normalize — method 요구 확인)
    sc.pp.normalize_total(atac, target_sum=1e4)
    sc.pp.log1p(atac)

    rna.write_h5ad(cfg.OUT_RNA)
    atac.write_h5ad(cfg.OUT_ATAC)
    try:
        import mudata as md
        md.MuData({"rna": rna, "atac": atac}).write(str(cfg.OUT_MUDATA))
        print(f"✓ saved MuData → {cfg.OUT_MUDATA}")
    except Exception as e:
        print(f"⚠ MuData 저장 실패({e}); rna/atac h5ad는 저장됨.")
    print(f"✓ RNA → {cfg.OUT_RNA}\n✓ ATAC → {cfg.OUT_ATAC}")
    print("다음: check_data.py 로 검증 (spliced/unspliced layer + ATAC gene 수 확인) → P2")


if __name__ == "__main__":
    sys.exit(build())
