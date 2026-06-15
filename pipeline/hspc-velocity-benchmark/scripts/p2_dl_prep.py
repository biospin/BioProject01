#!/usr/bin/env python3
"""P2 DL arm 공통 입력 prep (MultiVeloVAE / MoFlow). #2: GPU-ready 입력 사전 생성.

P1 substrate → MultiVelo와 *동일* substrate(공정성): counts→filter_normalize→HVG→moments(Ms/Mu)
→ UMAP → 공유 gene(RNA∩ATAC) → ATAC chromatin smoothing(Mc, P1 공유 그래프).
GPU 머신은 이 산출물만 복사하면 전처리 스킵하고 학습만.

출력: data/velocity/dl_input_rna.h5ad (Ms/Mu/spliced/unspliced/X_umap),
      data/velocity/dl_input_atac.h5ad (Mc)

실행(CPU 가능): conda run -n torch python pipeline/hspc-velocity-benchmark/scripts/p2_dl_prep.py
"""
from __future__ import annotations
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import sys
import numpy as np
import scipy.sparse as sp
import scanpy as sc
import scvelo as scv
import p2_config as cfg


def smooth_chrom(atac, conn):
    """multivelo.knn_smooth_chrom 등가: 공유 그래프(self-loop+row-norm)로 chromatin 평활 → Mc."""
    A = conn.copy().tocsr().astype(float)
    A = A + sp.eye(A.shape[0], format="csr")
    A = sp.diags(1.0 / np.asarray(A.sum(1)).ravel()) @ A
    X = atac.X.tocsr() if sp.issparse(atac.X) else atac.X
    Mc = A @ X
    atac.layers["Mc"] = Mc
    return atac


def main():
    cfg.OUT_VELO.mkdir(parents=True, exist_ok=True)
    rna = sc.read_h5ad(cfg.IN_RNA)
    atac = sc.read_h5ad(cfg.IN_ATAC)
    print(f"load RNA {rna.shape} | ATAC {atac.shape}")
    if "counts" in rna.layers:
        rna.X = rna.layers["counts"].copy()
    scv.pp.filter_and_normalize(rna, min_shared_counts=cfg.MIN_SHARED_COUNTS)
    if "highly_variable" not in rna.var.columns:
        sc.pp.highly_variable_genes(rna, n_top_genes=cfg.N_TOP_GENES)
    rna = rna[:, rna.var["highly_variable"]].copy()
    scv.pp.moments(rna, n_pcs=cfg.N_PCS, n_neighbors=cfg.N_NEIGHBORS)   # Ms/Mu
    sc.tl.umap(rna, random_state=cfg.RANDOM_SEED)                       # X_umap (MoFlow embed)

    shared = [g for g in rna.var_names if g in set(atac.var_names)]
    rna = rna[:, shared].copy()
    atac = atac[rna.obs_names, shared].copy()
    atac = smooth_chrom(atac, rna.obsp["connectivities"])               # Mc
    print(f"DL 입력: shared gene {len(shared)}, cells {rna.n_obs} | RNA layers {list(rna.layers)} | ATAC layers {list(atac.layers)}")

    # cross-env 호환(구 anndata) — uns None 제거
    for a in (rna, atac):
        a.uns.pop("log1p", None)
        for k in list(a.uns):
            if a.uns[k] is None:
                del a.uns[k]
    out_rna = cfg.OUT_VELO / "dl_input_rna.h5ad"
    out_atac = cfg.OUT_VELO / "dl_input_atac.h5ad"
    rna.write_h5ad(out_rna); atac.write_h5ad(out_atac)
    print(f"✓ {out_rna.name} + {out_atac.name} (GPU 머신으로 복사 → 학습만)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
