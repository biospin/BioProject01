#!/usr/bin/env python3
"""E18 mouse brain 10x Multiome (MultiVelo tutorial dataset) → processed h5ad.

cross-dataset 재현 2번(Track D). human_brain의 build+finalize를 한 스크립트로 합침
(E18은 단일 sample이라 per-sample 결합 불필요). human_brain과 달리 이 데이터셋은
mv.aggregate_peaks_10x 입력(loom + filtered_feature_bc_matrix + peak_annotation + feature_linkage)을
모두 제공 → HSPC p1_build와 **동일한 ATAC gene-level 집계 경로**를 verbatim으로 쓴다.

산출 (config_e18_mouse_brain.OUT = data/processed_e18_mouse_brain), HSPC/human_brain 스키마와 동일:
  - rna_spliced_unspliced.h5ad : cells×genes, X=spliced+unspliced, layers {counts,spliced,unspliced},
                                 obs {celltype,lineage,leiden}, mouse gene SYMBOL 축, HVG/PCA/neighbors 완료
  - atac_gene.h5ad             : cells×genes, gene-level accessibility (mv.aggregate_peaks_10x)

⚠️ lineage: 제공된 cell_annotations.tsv를 직접 사용(human 조혈 marker 강제 안 함). concordance는
   전역 per-gene fit rank라 lineage는 load-bearing 아님(defensible default).

실행 (scv-preprocess env; multivelo 0.1.5 필요):
  conda run --no-capture-output -n scv-preprocess python -u cross_dataset/build_e18_mouse_brain.py
"""
from __future__ import annotations
from pathlib import Path

import numpy as np
import pandas as pd
import scanpy as sc
import anndata as ad
import multivelo as mv

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                                   # pipeline/hspc-velocity-benchmark
RAW = ROOT / "data" / "e18_mouse_brain"
OUT = ROOT / "data" / "processed_e18_mouse_brain"
OUT.mkdir(parents=True, exist_ok=True)

LOOM = RAW / "10X_multiome_mouse_brain.loom"
MTX_DIR = RAW / "filtered_feature_bc_matrix"
PEAK_ANNOT = RAW / "e18_atac_peak_annotation.tsv"
LINKAGE = RAW / "analysis" / "feature_linkage" / "feature_linkage.bedpe"
ANNOT = RAW / "cell_annotations.tsv"

# HSPC와 동일 하이퍼파라미터 (공정 비교)
N_HVG, N_PCS, N_NEIGHBORS, LEIDEN_RES, SEED = 2000, 30, 30, 1.0, 0
QC = dict(min_genes=500, max_genes=9000, max_pct_mito=15.0)
RARE = {"Microglia", "Cajal-Retzius"}


def core_barcodes(names):
    """velocyto/ARC barcode를 16bp core로 정규화. 'PREFIX:AAAC...x' 또는 'AAAC...-1' → 'AAAC...'."""
    out = []
    for b in map(str, names):
        b = b.split(":")[-1]
        if b.endswith("x"):
            b = b[:-1]
        b = b.split("-")[0]
        out.append(b)
    return out


def main():
    sc.settings.verbosity = 1

    # ── RNA (loom: spliced/unspliced 직접 제공) ──
    print(f"[RNA] read loom {LOOM.name}", flush=True)
    rna = ad.read_loom(str(LOOM))
    rna.var_names_make_unique()
    rna.obs_names = core_barcodes(rna.obs_names)
    rna = rna[~rna.obs_names.duplicated()].copy()
    for lyr in ("spliced", "unspliced"):
        assert lyr in rna.layers, f"loom에 {lyr} layer 없음"
    # X = spliced+unspliced total (human_brain 규약과 동일; floor/MV는 counts layer에서 시작)
    rna.X = (rna.layers["spliced"] + rna.layers["unspliced"]).copy()
    print(f"  RNA {rna.shape}, layers={list(rna.layers)}", flush=True)

    # ── cell annotation (제공된 celltype) ──
    ann = pd.read_csv(ANNOT, sep="\t", index_col=0)
    ann.index = core_barcodes(ann.index)
    ann = ann[~ann.index.duplicated()]
    ann_col = ann.columns[0]                          # 'celltype'
    shared_cells = [c for c in rna.obs_names if c in set(ann.index)]
    print(f"  RNA∩annotation cells: {len(shared_cells)} / RNA {rna.n_obs}", flush=True)
    rna = rna[shared_cells].copy()
    rna.obs["celltype"] = ann.loc[shared_cells, ann_col].astype(str).values
    rna.obs["dataset"] = "e18_mouse_brain"

    # ── ATAC (filtered_feature_bc_matrix Peaks → gene-level via aggregate_peaks_10x) ──
    print(f"[ATAC] read_10x_mtx {MTX_DIR}", flush=True)
    combined = sc.read_10x_mtx(str(MTX_DIR), gex_only=False, cache=False)
    combined.var_names_make_unique()
    ft = combined.var["feature_types"].astype(str)
    atac = combined[:, ft == "Peaks"].copy()
    atac.obs_names = core_barcodes(atac.obs_names)
    atac = atac[~atac.obs_names.duplicated()].copy()
    print(f"  ATAC(peaks) {atac.shape}", flush=True)
    print(f"[ATAC] aggregate_peaks_10x (peak→gene) ...", flush=True)
    atac_gene = mv.aggregate_peaks_10x(atac, str(PEAK_ANNOT), str(LINKAGE),
                                       peak_dist=10000, min_corr=0.5)
    print(f"  ATAC gene-level {atac_gene.shape}", flush=True)

    # ── QC on RNA ──
    rna.var["mito"] = rna.var_names.str.lower().str.startswith("mt-")
    sc.pp.calculate_qc_metrics(rna, inplace=True, percent_top=None)
    if rna.var["mito"].any():
        rna.obs["pct_mito"] = (np.asarray(rna[:, rna.var["mito"]].X.sum(1)).ravel()
                               / np.asarray(rna.X.sum(1)).ravel() * 100)
    else:
        rna.obs["pct_mito"] = 0.0
    n0 = rna.n_obs
    sc.pp.filter_cells(rna, min_genes=QC["min_genes"])
    rna = rna[(rna.obs["n_genes_by_counts"] <= QC["max_genes"])
              & (rna.obs["pct_mito"] <= QC["max_pct_mito"])].copy()
    print(f"[QC] {n0} → {rna.n_obs} cells (mito≤{QC['max_pct_mito']}, genes {QC['min_genes']}~{QC['max_genes']})",
          flush=True)

    # cell 교집합으로 ATAC 정렬
    common = [c for c in rna.obs_names if c in set(atac_gene.obs_names)]
    rna = rna[common].copy()
    atac_gene = atac_gene[common].copy()
    print(f"[align] RNA∩ATAC cells: {len(common)}", flush=True)

    # ── 정규화 + HVG + graph (HSPC p1_build 순서 복제) ──
    rna.layers["counts"] = rna.X.copy()
    sc.pp.normalize_total(rna, target_sum=1e4)
    sc.pp.log1p(rna)
    sc.pp.highly_variable_genes(rna, n_top_genes=N_HVG)
    sc.pp.pca(rna, n_comps=N_PCS, random_state=SEED)
    sc.pp.neighbors(rna, n_neighbors=N_NEIGHBORS, random_state=SEED)
    sc.tl.leiden(rna, resolution=LEIDEN_RES, random_state=SEED, key_added="leiden")
    print(f"[graph] leiden clusters: {rna.obs['leiden'].nunique()}, HVG: {int(rna.var['highly_variable'].sum())}",
          flush=True)

    # lineage = 제공 celltype (marker 강제 안 함)
    rna.obs["lineage"] = rna.obs["celltype"].astype("category")
    rna.obs["lineage_rare"] = rna.obs["lineage"].isin(RARE)
    print("  celltype 분포:\n    "
          + rna.obs["celltype"].value_counts().to_string().replace("\n", "\n    "), flush=True)

    # ATAC 정규화 (gene-level; HSPC p1_build과 동일)
    atac_gene.obs["dataset"] = "e18_mouse_brain"
    atac_gene.obs["lineage"] = pd.Categorical(
        pd.Index(atac_gene.obs_names).map(pd.Series(rna.obs["lineage"].astype(str).values, index=rna.obs_names)))
    atac_gene.obs["leiden"] = pd.Categorical(
        pd.Index(atac_gene.obs_names).map(pd.Series(rna.obs["leiden"].astype(str).values, index=rna.obs_names)))
    sc.pp.normalize_total(atac_gene, target_sum=1e4)
    sc.pp.log1p(atac_gene)

    # cross-env 호환: uns None 값 제거 (구 anndata가 못 읽음)
    def _portable(a):
        a.uns.pop("log1p", None)
        for k in list(a.uns):
            if a.uns[k] is None:
                del a.uns[k]
    _portable(rna); _portable(atac_gene)

    rna.write_h5ad(OUT / "rna_spliced_unspliced.h5ad")
    atac_gene.write_h5ad(OUT / "atac_gene.h5ad")
    print(f"[RNA] → rna_spliced_unspliced.h5ad {rna.shape}", flush=True)
    print(f"[ATAC] → atac_gene.h5ad {atac_gene.shape}", flush=True)

    shared_g = sorted(set(rna.var_names) & set(atac_gene.var_names))
    print(f"[VERIFY] RNA↔ATAC obs identical: "
          f"{np.array_equal(rna.obs_names.to_numpy(), atac_gene.obs_names.to_numpy())}", flush=True)
    print(f"[VERIFY] RNA∩ATAC(gene) common genes: {len(shared_g)}", flush=True)
    print(f"[VERIFY] spliced present: {'spliced' in rna.layers}, "
          f"RNA finite: {np.isfinite(rna.X.data).all() if hasattr(rna.X,'data') else np.isfinite(rna.X).all()}",
          flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
