"""BIOP01-42 Phase-1 전처리 — GSE162170 human brain multiome → MultiVelo용 h5ad.
RNA(spliced/unspliced/counts) + ATAC gene activities + metadata → adata_rna, adata_atac.
velo-mv env(CPU). target=α (lag 아님)."""
import scanpy as sc
import anndata as ad
import numpy as np
import pandas as pd
from scipy import sparse
import gzip, os

DIR = "/workspace/data/cache/biop01/human_brain_GSE162170"
P = lambda f: os.path.join(DIR, f"GSE162170_{f}")

def read_gc(fname, label):
    """gene×cell dense TSV.gz → cells×genes sparse DataFrame(index=cell, col=gene)."""
    print(f"  loading {label} ...", flush=True)
    df = pd.read_csv(P(fname), sep="\t", index_col=0)
    print(f"    raw shape (gene×cell) = {df.shape}", flush=True)
    return df.T  # cells × genes

# --- RNA ---
spliced = read_gc("multiome_spliced_rna_counts.tsv.gz", "spliced"); spliced = spliced.loc[:, ~spliced.columns.duplicated()]
unspliced = read_gc("multiome_unspliced_rna_counts.tsv.gz", "unspliced"); unspliced = unspliced.loc[:, ~unspliced.columns.duplicated()]
# counts 파일은 Ensembl ID라 심볼 공간(spliced/unspliced/atac)과 불일치 → 제외. X=spliced.
cells = spliced.index.intersection(unspliced.index)
genes = spliced.columns.intersection(unspliced.columns)
print(f"RNA 공통(spliced∩unspliced): cells={len(cells)} genes={len(genes)}", flush=True)
spliced, unspliced = [m.loc[cells, genes] for m in (spliced, unspliced)]

adata = ad.AnnData(
    X=sparse.csr_matrix(spliced.values.astype(np.float32)),
    obs=pd.DataFrame(index=cells.astype(str)),
    var=pd.DataFrame(index=genes.astype(str)),
)
adata.layers["spliced"] = sparse.csr_matrix(spliced.values.astype(np.float32))
adata.layers["unspliced"] = sparse.csr_matrix(unspliced.values.astype(np.float32))

# --- metadata ---
meta = pd.read_csv(P("multiome_cell_metadata.txt.gz"), sep="\t", index_col=0)
meta = meta.reindex(adata.obs_names)
for c in ["Sample.ID", "Sample.Age", "Sample.Batch", "RNA.Counts", "percentMT"]:
    if c in meta.columns:
        adata.obs[c] = meta[c].values
print(f"metadata 부착: {[c for c in adata.obs.columns]}", flush=True)
print(f"  donor(Sample.ID) {adata.obs['Sample.ID'].nunique()}종 · batch {adata.obs['Sample.Batch'].nunique()}종 · age {sorted(adata.obs['Sample.Age'].dropna().unique())}", flush=True)

# --- ATAC gene activities ---
atac = read_gc("multiome_atac_gene_activities.tsv.gz", "atac_gene_activity"); atac = atac.loc[:, ~atac.columns.duplicated()]
# 공통 cell·gene로 정렬 (RNA와 교집)
acells = adata.obs_names.intersection(atac.index)
agenes = adata.var_names.intersection(atac.columns)
print(f"RNA∩ATAC: cells={len(acells)} genes={len(agenes)}", flush=True)
atac = atac.loc[acells, agenes]
adata_atac = ad.AnnData(
    X=sparse.csr_matrix(atac.values.astype(np.float32)),
    obs=adata.obs.loc[acells].copy(),
    var=pd.DataFrame(index=agenes.astype(str)),
)
# RNA를 공통 cell로 맞춤(MultiVelo는 같은 cell·gene 필요)
adata = adata[acells, agenes].copy()

# --- 기본 QC ---
sc.pp.filter_genes(adata, min_cells=10)
common_g = adata.var_names.intersection(adata_atac.var_names)
adata = adata[:, common_g].copy()
adata_atac = adata_atac[:, common_g].copy()

adata.write(os.path.join(DIR, "brain_rna.h5ad"))
adata_atac.write(os.path.join(DIR, "brain_atac.h5ad"))
print("\n=== 저장 완료 ===")
print(f"  brain_rna.h5ad : {adata.shape} (X=counts, layers: spliced/unspliced)")
print(f"  brain_atac.h5ad: {adata_atac.shape} (gene activities)")
print(f"  spliced nnz frac: {adata.layers['spliced'].nnz/(adata.shape[0]*adata.shape[1]):.4f}")
