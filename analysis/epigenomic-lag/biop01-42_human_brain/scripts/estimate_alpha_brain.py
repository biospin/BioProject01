"""BIOP01-42 Phase-1 step2 — α(전사속도) 추정 (scVelo dynamical).
target=α (lag 아님). recover_dynamics의 fit_alpha가 gene별 α.
velo-mv env, CPU. 표준 scVelo 워크플로 + velocity gene 필터."""
import scanpy as sc
import scvelo as scv
import numpy as np
import os

DIR = "/workspace/data/cache/biop01/human_brain_GSE162170"
scv.settings.verbosity = 1
scv.settings.n_jobs = 16

adata = sc.read_h5ad(os.path.join(DIR, "brain_rna.h5ad"))
print(f"입력: {adata.shape} (cells×genes)", flush=True)

# 표준 전처리 (spliced/unspliced 기반) — filter_and_normalize kwarg 버그 우회로 분해
scv.pp.filter_genes(adata, min_shared_counts=20)
scv.pp.normalize_per_cell(adata)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2000)
adata = adata[:, adata.var["highly_variable"]].copy()
scv.pp.moments(adata, n_pcs=30, n_neighbors=30)
print(f"velocity gene 필터 후: {adata.shape}", flush=True)

# dynamical model → gene별 kinetic 파라미터 (fit_alpha = 전사속도 α)
scv.tl.recover_dynamics(adata, n_jobs=16)
scv.tl.velocity(adata, mode="dynamical")

# α 추출
alpha = adata.var["fit_alpha"].copy()
n_fit = alpha.notna().sum()
print(f"\nα 추정 완료: fit된 gene {n_fit}/{adata.n_vars}")
print(f"  α 분포: median={np.nanmedian(alpha):.4f} mean={np.nanmean(alpha):.4f} "
      f"[{np.nanmin(alpha):.4f}, {np.nanmax(alpha):.4f}]")

# 저장 (α + fit 파라미터 + processed adata)
adata.write(os.path.join(DIR, "brain_rna_dynamical.h5ad"))
alpha_df = adata.var[[c for c in adata.var.columns if c.startswith("fit_")]].copy()
alpha_df.to_csv(os.path.join(DIR, "brain_gene_alpha.csv"))
print(f"\nSaved: brain_rna_dynamical.h5ad + brain_gene_alpha.csv ({n_fit} genes with α)")
print("DONE_ALPHA", flush=True)
