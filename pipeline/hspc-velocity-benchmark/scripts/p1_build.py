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
  conda run --no-capture-output -n scv-preprocess python -u \
      pipeline/hspc-velocity-benchmark/scripts/p1_build.py          # 기본=resume
  # resume: data/processed/_ckpt/{sample}_rna|atac.h5ad 가 있으면 그 sample(load/loom/ATAC/QC)을
  #         건너뛰고 이어함. 전부 다시 하려면 끝에 --fresh.
  # --no-capture-output -u : 단계 로그 실시간 출력 (conda run 버퍼링 방지).

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


def _plain(path_gz):
    """multivelo는 annotation을 plain open()으로 읽음(.gz 미지원) → 필요 시 압축 해제한 경로 반환."""
    import gzip, shutil
    from pathlib import Path
    path_gz = Path(path_gz)
    if not str(path_gz).endswith(".gz"):
        return str(path_gz)
    plain = path_gz.with_suffix("")          # .tsv.gz → .tsv, .bedpe.gz → .bedpe
    if not plain.exists():
        with gzip.open(path_gz, "rb") as fi, open(plain, "wb") as fo:
            shutil.copyfileobj(fi, fo)
        print(f"  decompress {path_gz.name} → {plain.name}")
    return str(plain)


def aggregate_atac(atac, d, name):
    """multivelo.aggregate_peaks_10x로 peak→gene 집계 → sample 간 공통 gene 축."""
    try:
        import multivelo as mv
        # multivelo 0.1.5 시그니처: (adata_atac, peak_annot_file, linkage_file,
        #   peak_dist=10000, min_corr=0.5, gene_body=False, return_dict=False, parallel=False, n_jobs=1)
        # 'verbose' 인자 없음; annotation은 .gz 미지원 → _plain()으로 해제 경로 전달.
        agg = mv.aggregate_peaks_10x(
            atac,
            _plain(d / "peak_annotation.tsv.gz"),
            _plain(d / "feature_linkage.bedpe.gz"),
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


def annotate_lineage(rna):
    """marker score_genes → Leiden cluster 단위 argmax 할당 (method-agnostic lineage).

    per-cell이 아니라 cluster 단위로 할당해 노이즈에 강함. log-normalized X 전제(build 순서상 충족).
    var_names에 있는 marker만 사용; rare lineage는 obs['lineage_rare']로 표시.
    """
    import pandas as pd
    used, missing = {}, {}
    for lin, genes in cfg.LINEAGE_MARKERS.items():
        present = [g for g in genes if g in rna.var_names]
        if present:
            sc.tl.score_genes(rna, present, score_name=f"sig_{lin}", ctrl_size=50,
                              random_state=cfg.RANDOM_SEED)
            used[lin] = present
        miss = [g for g in genes if g not in rna.var_names]
        if miss:
            missing[lin] = miss
    if not used:
        print("  ⚠ lineage marker가 var_names에 하나도 없음 → lineage 할당 생략")
        return rna
    score_cols = [f"sig_{lin}" for lin in used]
    means = rna.obs.groupby("leiden", observed=True)[score_cols].mean()
    cl2lin = means.idxmax(axis=1).str.replace("sig_", "", regex=False)
    rna.obs["lineage"] = rna.obs["leiden"].map(cl2lin).astype("category")
    rna.obs["lineage_rare"] = rna.obs["lineage"].isin(cfg.RARE_LINEAGES)
    print(f"  lineage marker 누락(var_names에 없음): {missing or '없음'}")
    print("  cluster→lineage:\n    " + cl2lin.to_string().replace("\n", "\n    "))
    print("  lineage 분포:\n    " + rna.obs["lineage"].value_counts().to_string().replace("\n", "\n    "))
    return rna


def _ckpt_paths(name):
    """per-sample 체크포인트 경로 (load+loom+ATAC+QC 까지 끝난 상태)."""
    cd = cfg.OUT / "_ckpt"
    return cd / f"{name}_rna.h5ad", cd / f"{name}_atac.h5ad"


def build(fresh=False):
    """fresh=True면 체크포인트 무시하고 전부 재계산. 기본은 완료된 sample 이어하기(resume)."""
    cfg.OUT.mkdir(parents=True, exist_ok=True)
    (cfg.OUT / "_ckpt").mkdir(exist_ok=True)
    sc.settings.verbosity = 1
    rnas, atacs = [], []
    for name, info in cfg.SAMPLES.items():
        rp, ap = _ckpt_paths(name)
        if not fresh and rp.exists() and ap.exists():
            print(f"[{name}] ✓ checkpoint 재사용 (load/loom/ATAC/QC 스킵) → {rp.name}, {ap.name}")
            rna, atac = sc.read_h5ad(rp), sc.read_h5ad(ap)
        else:
            rna, atac = load_sample(name, info)
            rna, atac = qc_sample(rna, atac, name)
            rna.write_h5ad(rp); atac.write_h5ad(ap)
            print(f"[{name}] ✓ checkpoint 저장 → {rp.name}, {ap.name}")
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

    # marker 기반 lineage 라벨 (method-agnostic) — 모든 P3/P4 지표가 within-lineage라 P2 선행 게이트
    rna = annotate_lineage(rna)

    # lineage/timepoint를 ATAC에도 전달 (within-lineage 지표는 양 modality 필요; 동일 cell 집합)
    import pandas as pd
    if "lineage" in rna.obs:
        lin_map = pd.Series(rna.obs["lineage"].astype(str).values, index=rna.obs_names)
        atac.obs["lineage"] = pd.Categorical(pd.Index(atac.obs_names).map(lin_map))
        atac.obs["lineage_rare"] = atac.obs["lineage"].isin(cfg.RARE_LINEAGES)
    atac.obs["leiden"] = pd.Categorical(
        pd.Index(atac.obs_names).map(pd.Series(rna.obs["leiden"].astype(str).values, index=rna.obs_names)))

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
    # 기본: resume(완료 sample 스킵). --fresh: 체크포인트 무시하고 전부 재계산.
    sys.exit(build(fresh="--fresh" in sys.argv))
