#!/usr/bin/env python
"""
p2_crakvelo_cistopic.py — CRAK-Velo ATAC smoothing (cisTopic torch LDA).

CRAK-Velo 저자 preprocessing.ipynb 충실 재현:
  filter_genes(min_counts=800) -> filter_cells(min_counts=1)
  cisTopic(T=30, alpha=50/T, beta=0.1).fit(batch_size=500, n_samples=3000, n_burnin=10, cuda)
  theta/phi 의 burn-in 후([50:]) 평균·정규화 -> obsm['cisTopic'] = theta_mean @ phi_mean (cell×region)

입력 : data/velocity/crakvelo_atac_prepro.h5ad   (cell × consensus-peak, var 좌표)
산출 : data/velocity/crakvelo_atac_postpro.h5ad  (+ obsm['cisTopic'])

GPU: BIOP01 전용 cuda:1 핀 (CUDA_VISIBLE_DEVICES=1 로 실행 → 내부적으로 'cuda'=물리 1번).
"""
import os
import sys
import time
from pathlib import Path
import numpy as np
import torch
import scanpy as sc
import anndata as ad

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "vendor" / "cisTopic"))
from cisTopic import cisTopic  # noqa: E402

ATAC_IN = HERE / "data" / "velocity" / "crakvelo_atac_prepro.h5ad"
ATAC_OUT = HERE / "data" / "velocity" / "crakvelo_atac_postpro.h5ad"

T = 30
ALPHA = 50 / T
BETA = 0.1
N_SAMPLES = int(os.environ.get("CIS_N_SAMPLES", 3000))
N_BURNIN = int(os.environ.get("CIS_N_BURNIN", 10))
BATCH_SIZE = int(os.environ.get("CIS_BATCH", 500))
KEEP_FROM = int(os.environ.get("CIS_KEEP_FROM", 50))   # burn-in: 저장 샘플 [50:] (저자 노트북 default)
SMOKE = os.environ.get("CIS_SMOKE", "0") == "1"


def log(m):
    print(f"[cistopic] {time.strftime('%H:%M:%S')} {m}", flush=True)


def main():
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    log(f"device={dev}  CUDA_VISIBLE_DEVICES={os.environ.get('CUDA_VISIBLE_DEVICES','?')}")

    a = ad.read_h5ad(ATAC_IN)
    log(f"loaded {a.shape}")
    sc.pp.filter_genes(a, min_counts=800)
    sc.pp.filter_cells(a, min_counts=1)
    log(f"after filter: {a.shape}  nnz={int(a.X.nnz)}")

    cis = cisTopic(a, T, ALPHA, BETA)
    log(f"fit start: T={T} n_samples={N_SAMPLES} burnin={N_BURNIN} batch={BATCH_SIZE}")
    theta, phi = cis.fit(BATCH_SIZE, N_SAMPLES, N_BURNIN, dev=dev, save_data=False)
    log(f"fit done. theta{tuple(theta.shape)} phi{tuple(phi.shape)}")

    # burn-in 후 평균 + row 정규화 (notebook cell 7-8)
    m = theta[KEEP_FROM:, :, :].mean(axis=0)
    m = m / m.sum(axis=1)[:, None]
    m_psi = phi[KEEP_FROM:, :, :].mean(axis=0)
    m_psi = m_psi / m_psi.sum(axis=1)[:, None]
    recon = torch.matmul(m, m_psi)          # cell × region
    a.obsm["cisTopic"] = recon.cpu().numpy().astype(np.float32)
    log(f"obsm['cisTopic'] = {a.obsm['cisTopic'].shape}")

    a.write_h5ad(ATAC_OUT)
    log(f"wrote {ATAC_OUT}")
    log("DONE")


if __name__ == "__main__":
    main()
