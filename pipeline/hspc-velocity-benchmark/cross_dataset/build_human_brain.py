#!/usr/bin/env python3
"""GSE162170 (human fetal cortex multiome, Trevino 2021) tsv → processed h5ad.

cross-dataset 재현 1번 데이터셋. RUNBOOK option B(processed 직접 공유) 경로 —
GEO supplement가 spliced/unspliced counts를 직접 제공하므로 P1(CellRanger ARC + velocyto)
전처리를 건너뛰고 P2가 소비하는 객체를 직접 만든다.

산출 (config_human_brain.OUT = data/processed_human_brain):
  - rna_spliced_unspliced.h5ad : cells×genes, X=spliced+unspliced total, layers {spliced, unspliced}, symbol 축
  - atac_peaks.h5ad            : cells×peaks (sparse), var=consensus peak 좌표

축 결정:
  - RNA는 spliced/unspliced(둘 다 gene SYMBOL 인덱스)를 쓴다. rna_counts는 ENSG라 HSPC(symbol 축)와
    안 겹치므로 사용하지 않는다. HSPC var_names=symbol이라 concordance/marker가 symbol 축에서 정합.
  - ATAC는 headerless peaks×cells 행렬. 행=consensus_peaks 순서, 열=cell_metadata 순서(positional).

주의: peak→gene 집계는 여기서 하지 않는다(별도 단계). GSE162170은 10x peak_annotation/feature_linkage를
제공하지 않아 mv.aggregate_peaks_10x 불가 → gencode v44 기반 genomic proximity 집계를 후속 스크립트에서.
"""
from __future__ import annotations
import gzip
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.sparse as sp
import scipy.io
import anndata as ad

HERE = Path(__file__).resolve().parent
RAW = HERE.parent / "data" / "human_brain"
OUT = HERE.parent / "data" / "processed_human_brain"
OUT.mkdir(parents=True, exist_ok=True)

RNA_SPLICED = RAW / "GSE162170_multiome_spliced_rna_counts.tsv.gz"
RNA_UNSPL = RAW / "GSE162170_multiome_unspliced_rna_counts.tsv.gz"
ATAC = RAW / "GSE162170_multiome_atac_counts.tsv.gz"
PEAKS = RAW / "GSE162170_multiome_atac_consensus_peaks.txt.gz"
META = RAW / "GSE162170_multiome_cell_metadata.txt.gz"
CLUST = RAW / "GSE162170_multiome_cluster_names.txt.gz"


def read_gene_by_cell(path: Path) -> tuple[np.ndarray, np.ndarray, sp.csr_matrix]:
    """`gene`-headed genes×cells tsv → (genes, cells, sparse cells×genes).

    chunk 단위로 읽어 sparse 누적(메모리 절약)."""
    print(f"  reading {path.name} ...", flush=True)
    header = pd.read_csv(path, sep="\t", nrows=0)
    cells = np.array(header.columns[1:])  # 첫 컬럼 = 'gene'
    genes, blocks = [], []
    reader = pd.read_csv(path, sep="\t", chunksize=4000, index_col=0)
    n = 0
    for chunk in reader:
        genes.append(chunk.index.to_numpy())
        blocks.append(sp.csr_matrix(chunk.to_numpy(dtype=np.float32)))
        n += chunk.shape[0]
        print(f"    {n} genes", flush=True)
    genes = np.concatenate(genes)
    mat = sp.vstack(blocks).tocsr()  # genes×cells
    return genes, cells, mat.T.tocsr()  # cells×genes


def read_headerless_peak_by_cell(path: Path, n_cells_expected: int) -> sp.csr_matrix:
    """headerless peaks×cells 숫자 tsv → sparse cells×peaks."""
    print(f"  reading {path.name} (headerless, streaming) ...", flush=True)
    blocks = []
    n = 0
    for chunk in pd.read_csv(path, sep="\t", header=None, chunksize=20000, dtype=np.float32):
        assert chunk.shape[1] == n_cells_expected, f"col mismatch {chunk.shape[1]} != {n_cells_expected}"
        blocks.append(sp.csr_matrix(chunk.to_numpy()))
        n += chunk.shape[0]
        print(f"    {n} peaks", flush=True)
    mat = sp.vstack(blocks).tocsr()  # peaks×cells
    return mat.T.tocsr()  # cells×peaks


def main():
    meta = pd.read_csv(META, sep="\t", index_col=0)
    print(f"cell_metadata: {meta.shape}, index[0]={meta.index[0]}", flush=True)
    clust = pd.read_csv(CLUST, sep="\t")
    # RNA cluster name 매핑 (seurat_clusters cN → Cluster.Name)
    rna_clust = clust[clust["Assay"].str.contains("RNA")].set_index("Cluster.ID")["Cluster.Name"]

    # ── RNA ──
    print("[RNA] spliced", flush=True)
    g_s, c_s, m_s = read_gene_by_cell(RNA_SPLICED)
    print("[RNA] unspliced", flush=True)
    g_u, c_u, m_u = read_gene_by_cell(RNA_UNSPL)
    assert np.array_equal(g_s, g_u), "spliced/unspliced gene axis 불일치"
    assert np.array_equal(c_s, c_u), "spliced/unspliced cell axis 불일치"
    # cell 축을 cell_metadata 순서로 정렬(positional 정합 보장)
    assert set(c_s) == set(meta.index), "RNA cell != metadata cell"
    order = pd.Index(c_s).get_indexer(meta.index)
    m_s, m_u = m_s[order], m_u[order]
    rna = ad.AnnData(
        X=(m_s + m_u).tocsr(),
        obs=meta.copy(),
        var=pd.DataFrame(index=g_s),
    )
    rna.layers["spliced"] = m_s
    rna.layers["unspliced"] = m_u
    # cluster name annotation
    if "seurat_clusters" in rna.obs:
        rna.obs["cluster_name"] = rna.obs["seurat_clusters"].map(rna_clust).astype("category")
    rna.obs["dataset"] = "human_brain"
    rna.write_h5ad(OUT / "rna_spliced_unspliced.h5ad")
    print(f"[RNA] wrote {rna.shape} → rna_spliced_unspliced.h5ad", flush=True)
    print(f"      spliced nnz frac={m_s.nnz/np.prod(m_s.shape):.4f}, unspliced={m_u.nnz/np.prod(m_u.shape):.4f}", flush=True)

    # ── ATAC (peak-level; gene 집계는 후속) ──
    peaks = pd.read_csv(PEAKS, sep="\t")
    print(f"[ATAC] consensus_peaks: {peaks.shape}", flush=True)
    atac_m = read_headerless_peak_by_cell(ATAC, n_cells_expected=len(meta))
    assert atac_m.shape[0] == len(meta), f"ATAC cells {atac_m.shape[0]} != {len(meta)}"
    assert atac_m.shape[1] == len(peaks), f"ATAC peaks {atac_m.shape[1]} != {len(peaks)}"
    peak_names = peaks["name"].astype(str).to_numpy() if "name" in peaks else np.array(
        [f"{r.seqnames}:{r.start}-{r.end}" for r in peaks.itertuples()])
    var = pd.DataFrame({
        "seqnames": peaks["seqnames"].to_numpy(),
        "start": peaks["start"].to_numpy(),
        "end": peaks["end"].to_numpy(),
    }, index=peak_names)
    atac = ad.AnnData(X=atac_m, obs=meta.copy(), var=var)
    atac.obs["dataset"] = "human_brain"
    atac.write_h5ad(OUT / "atac_peaks.h5ad")
    print(f"[ATAC] wrote {atac.shape} → atac_peaks.h5ad (peak-level)", flush=True)

    # ── 정합 검증 ──
    same = np.array_equal(rna.obs_names.to_numpy(), atac.obs_names.to_numpy())
    print(f"[VERIFY] RNA↔ATAC obs_names identical: {same}", flush=True)
    print(f"[VERIFY] RNA finite: {np.isfinite(rna.X.data).all()}, ATAC finite: {np.isfinite(atac.X.data).all()}", flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
