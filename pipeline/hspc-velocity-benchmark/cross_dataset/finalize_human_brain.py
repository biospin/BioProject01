#!/usr/bin/env python3
"""human_brain (GSE162170) P1-equivalent finalization (RUNBOOK option B).

build_human_brain.py가 만든 raw 객체(rna: counts X + spliced/unspliced, atac: peak-level)를
받아 HSPC p1_build.py의 공통 branch와 **동일한 스키마**로 마감한다. 목적: floor/MultiVelo가
HSPC와 같은 substrate·그래프·HVG·lineage를 쓰게 해 공정 비교 성립.

HSPC p1_build 마감 순서 복제:
  QC(filter cells, mito, doublet=provider DF_classification) →
  counts layer 보존 → normalize_total(1e4) → log1p → HVG(N_HVG) →
  PCA(N_PCS) → neighbors(N_NEIGHBORS) → leiden(LEIDEN_RES) → annotate_lineage(cortical marker).

추가: ATAC peak→gene 집계(GSE162170은 10x peak_annotation 미제공 → mv.aggregate_peaks_10x 불가).
  gencode v44 gene body ±PEAK_DIST 창에 겹치는 peak 합산 → gene-level accessibility.
  ⚠️ caveat: HSPC는 mv.aggregate_peaks_10x(peak_annotation+linkage)를 썼고 여기선 genomic-proximity
     집계라 구현이 다르다(문서화). 축(gene symbol)은 RNA와 정합.

산출:
  - data/processed_human_brain/rna_spliced_unspliced.h5ad  (finalized, 덮어씀)
  - data/processed_human_brain/atac_gene.h5ad              (gene-level; config OUT_ATAC를 여기로)
"""
from __future__ import annotations
import gzip
import re
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.sparse as sp
import scanpy as sc
import anndata as ad

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                                  # pipeline/hspc-velocity-benchmark
OUT = ROOT / "data" / "processed_human_brain"
GTF = ROOT / "data" / "ref" / "gencode.v44.basic.annotation.gtf.gz"

# HSPC와 동일 하이퍼파라미터 (공정 비교)
N_HVG, N_PCS, N_NEIGHBORS, LEIDEN_RES, SEED = 2000, 30, 30, 1.0, 0
PEAK_DIST = 10000   # gene body 양옆 확장(bp). multivelo aggregate_peaks_10x 기본 peak_dist=10000과 정합.

# cortical lineage marker (config_human_brain와 동일)
LINEAGE_MARKERS = {
    "RG": ["VIM","HES1","PAX6","SOX2","GLI3","HOPX","PTPRZ1","SLC1A3","TNC"],
    "Cycling": ["MKI67","TOP2A","CENPF","ASPM","CLSPN"],
    "nIPC": ["EOMES","PPP1R17","NEUROG1","NEUROG2","PENK"],
    "ExN": ["NEUROD2","NEUROD6","TBR1","SATB2","BCL11B","STMN2","SLC17A7","FEZF2"],
    "InN": ["DLX1","DLX2","DLX5","GAD1","GAD2","SLC32A1","LHX6","SP8"],
    "OPC": ["OLIG1","OLIG2","PDGFRA","SOX10","EGFR"],
    "Microglia": ["AIF1","C1QB","PTPRC","CX3CR1","P2RY12"],
}
RARE_LINEAGES = {"OPC", "Microglia"}
QC = dict(min_genes=500, max_genes=9000, max_pct_mito=15.0)


def annotate_lineage(rna):
    used = {}
    for lin, genes in LINEAGE_MARKERS.items():
        present = [g for g in genes if g in rna.var_names]
        if present:
            sc.tl.score_genes(rna, present, score_name=f"sig_{lin}", ctrl_size=50, random_state=SEED)
            used[lin] = present
    if not used:
        print("  ⚠ marker 없음 → lineage 생략"); return rna
    cols = [f"sig_{lin}" for lin in used]
    means = rna.obs.groupby("leiden", observed=True)[cols].mean()
    cl2lin = means.idxmax(axis=1).str.replace("sig_", "", regex=False)
    rna.obs["lineage"] = rna.obs["leiden"].map(cl2lin).astype("category")
    rna.obs["lineage_rare"] = rna.obs["lineage"].isin(RARE_LINEAGES)
    print("  cluster→lineage:\n    " + cl2lin.to_string().replace("\n", "\n    "))
    print("  lineage 분포:\n    " + rna.obs["lineage"].value_counts().to_string().replace("\n", "\n    "))
    return rna


def load_gencode_genes(path: Path) -> pd.DataFrame:
    """gencode gtf → gene별 (symbol, chrom, start, end). basic annotation의 gene feature만."""
    rows = []
    pat_name = re.compile(r'gene_name "([^"]+)"')
    with gzip.open(path, "rt") as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            f = line.rstrip("\n").split("\t")
            if len(f) < 9 or f[2] != "gene":
                continue
            m = pat_name.search(f[8])
            if not m:
                continue
            rows.append((m.group(1), f[0], int(f[3]), int(f[4])))
    df = pd.DataFrame(rows, columns=["symbol", "chrom", "start", "end"])
    # 같은 symbol 여러 좌표 → 최소 start~최대 end로 통합(가장 관대한 gene body)
    df = df.groupby(["symbol", "chrom"], as_index=False).agg(start=("start", "min"), end=("end", "max"))
    return df


def aggregate_peaks_to_genes(atac, genes_df, target_genes):
    """peak-level ATAC(cells×peaks, var seqnames/start/end) → gene-level(cells×genes).

    gene body ±PEAK_DIST 창에 겹치는 peak 합산. target_genes(=RNA var_names)에 있는 gene만."""
    peaks = atac.var
    P = atac.X.tocsc()                       # cells×peaks
    gsel = genes_df[genes_df["symbol"].isin(set(target_genes))].reset_index(drop=True)
    print(f"  gencode genes ∩ RNA: {gsel.shape[0]}")
    cols_gene, cols_peak = [], []
    peak_start = peaks["start"].to_numpy()
    peak_end = peaks["end"].to_numpy()
    peak_chrom = peaks["seqnames"].astype(str).to_numpy()
    # chromosome 별 인덱스 (peak start 정렬)
    by_chrom = {}
    for c in np.unique(peak_chrom):
        idx = np.where(peak_chrom == c)[0]
        order = idx[np.argsort(peak_start[idx])]
        by_chrom[c] = (order, peak_start[order], peak_end[order])
    for gi, row in enumerate(gsel.itertuples(index=False)):
        ch = row.chrom
        if ch not in by_chrom:
            continue
        order, ps, pe = by_chrom[ch]
        lo, hi = row.start - PEAK_DIST, row.end + PEAK_DIST
        # 겹침: peak.start <= hi AND peak.end >= lo. start 정렬 이용해 start<=hi 범위 자름.
        j = np.searchsorted(ps, hi, side="right")
        cand = order[:j]
        ce = pe[:j]
        keep = cand[ce >= lo]
        if keep.size:
            cols_gene.append(np.full(keep.size, gi, dtype=np.int32))
            cols_peak.append(keep.astype(np.int32))
    if not cols_gene:
        raise RuntimeError("peak→gene 겹침 0 — 좌표계(chr prefix) 불일치 의심")
    g_idx = np.concatenate(cols_gene)
    p_idx = np.concatenate(cols_peak)
    n_genes, n_peaks = gsel.shape[0], atac.n_vars
    M = sp.csr_matrix((np.ones(g_idx.size, np.float32), (g_idx, p_idx)), shape=(n_genes, n_peaks))
    gene_counts = (P @ M.T).tocsr()          # cells×genes
    npair = g_idx.size
    print(f"  peak→gene pairs: {npair}, genes with ≥1 peak: {(np.asarray((M.sum(1))).ravel()>0).sum()}")
    out = ad.AnnData(X=gene_counts, obs=atac.obs.copy(),
                     var=pd.DataFrame(index=gsel["symbol"].to_numpy()))
    out.var_names_make_unique()
    return out


def main():
    rna = sc.read_h5ad(OUT / "rna_spliced_unspliced.h5ad")
    print(f"[load] RNA {rna.shape} layers={list(rna.layers)}")
    # ── QC ──
    rna.var["mito"] = rna.var_names.str.upper().str.startswith("MT-")
    sc.pp.calculate_qc_metrics(rna, inplace=True, percent_top=None)
    if rna.var["mito"].any():
        rna.obs["pct_mito"] = (np.asarray(rna[:, rna.var["mito"]].X.sum(1)).ravel()
                               / np.asarray(rna.X.sum(1)).ravel() * 100)
    else:
        rna.obs["pct_mito"] = 0.0
    n0 = rna.n_obs
    sc.pp.filter_cells(rna, min_genes=QC["min_genes"])
    mask = (rna.obs["n_genes_by_counts"] <= QC["max_genes"]) & (rna.obs["pct_mito"] <= QC["max_pct_mito"])
    # provider doublet call(있으면) 사용
    if "DF_classification" in rna.obs:
        mask &= (rna.obs["DF_classification"].astype(str) == "Singlet")
    rna = rna[mask].copy()
    print(f"[QC] {n0} → {rna.n_obs} cells (mito≤{QC['max_pct_mito']}, genes {QC['min_genes']}~{QC['max_genes']}, Singlet)")

    # ── 정규화 + HVG + graph (HSPC 순서 복제) ──
    rna.layers["counts"] = rna.X.copy()
    sc.pp.normalize_total(rna, target_sum=1e4)
    sc.pp.log1p(rna)
    sc.pp.highly_variable_genes(rna, n_top_genes=N_HVG)
    sc.pp.pca(rna, n_comps=N_PCS, random_state=SEED)
    sc.pp.neighbors(rna, n_neighbors=N_NEIGHBORS, random_state=SEED)
    sc.tl.leiden(rna, resolution=LEIDEN_RES, random_state=SEED, key_added="leiden")  # HSPC와 동일(기본 flavor)
    print(f"[graph] leiden clusters: {rna.obs['leiden'].nunique()}, HVG: {int(rna.var['highly_variable'].sum())}")
    rna = annotate_lineage(rna)
    rna.write_h5ad(OUT / "rna_spliced_unspliced.h5ad")
    print(f"[RNA] finalized → rna_spliced_unspliced.h5ad {rna.shape}")

    # ── ATAC peak→gene ──
    atac = sc.read_h5ad(OUT / "atac_peaks.h5ad")
    print(f"[load] ATAC(peak) {atac.shape}")
    atac = atac[rna.obs_names].copy()                 # QC 통과 cell로 정렬
    genes_df = load_gencode_genes(GTF)
    print(f"[gencode] genes: {genes_df.shape[0]}")
    atac_gene = aggregate_peaks_to_genes(atac, genes_df, rna.var_names)
    atac_gene.write_h5ad(OUT / "atac_gene.h5ad")
    print(f"[ATAC] gene-level → atac_gene.h5ad {atac_gene.shape}")

    shared = sorted(set(rna.var_names) & set(atac_gene.var_names))
    print(f"[VERIFY] RNA∩ATAC(gene) common genes: {len(shared)}")
    print("DONE")


if __name__ == "__main__":
    main()
