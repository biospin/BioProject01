#!/usr/bin/env python3
"""P2 — RNA-only floor (scVelo dynamical). DESIGN §2(REQUIRED baseline), §4.

chromatin-aware method가 RNA-only 대비 *얼마나* 개선하는지의 floor.
입력 = P1 공통 RNA(spliced/unspliced + leiden + lineage). velocity는 전역 계산,
lag/지표의 within-lineage 분석은 P3에서.

출력:
  - data/velocity/rna_only_dynamical.h5ad         (전체 adata, gitignore)
  - results/rna_only_dynamical_genes.csv          (gene별 fit 파라미터 요약, tracked)
  - results/runtime.csv                           (runtime/peak-mem append, tracked)

실행:
  conda run --no-capture-output -n scv-preprocess python -u \
      pipeline/hspc-velocity-benchmark/scripts/p2_rna_only.py
"""
from __future__ import annotations
import sys
import numpy as np
import scanpy as sc
import scvelo as scv
import pandas as pd
import p2_config as cfg
from p2_util import timer, peak_mem_mb, log_runtime

METHOD, ARM = "scvelo_dynamical", "rna_only"


def main():
    cfg.OUT_VELO.mkdir(parents=True, exist_ok=True)
    cfg.RESULTS.mkdir(parents=True, exist_ok=True)
    scv.settings.verbosity = 1

    adata = sc.read_h5ad(cfg.IN_RNA)
    print(f"load {cfg.IN_RNA.name}: {adata.shape}, layers={list(adata.layers)}")
    if "spliced" not in adata.layers or "unspliced" not in adata.layers:
        print("✗ spliced/unspliced 없음 — P1 점검 필요"); return 1

    # scVelo 표준 recipe는 raw counts에서 시작 → X를 counts로 되돌림 (P1에서 X=log-norm)
    if "counts" in adata.layers:
        adata.X = adata.layers["counts"].copy()

    with timer() as t:
        # scVelo 0.3.4: filter_and_normalize에 n_top_genes 인자 없음(→kwargs 오류),
        #   filter_genes_dispersion 미노출 → gene subset은 별도로. spliced/unspliced 정규화만 위임.
        scv.pp.filter_and_normalize(adata, min_shared_counts=cfg.MIN_SHARED_COUNTS)
        # velocity gene set = HVG (P1 flag 재사용; 없으면 재계산)
        if "highly_variable" not in adata.var.columns:
            sc.pp.highly_variable_genes(adata, n_top_genes=cfg.N_TOP_GENES)
        adata = adata[:, adata.var["highly_variable"]].copy()
        scv.pp.moments(adata, n_pcs=cfg.N_PCS, n_neighbors=cfg.N_NEIGHBORS)
        print(f"velocity gene set: {adata.n_vars} genes, {adata.n_obs} cells")
        if adata.n_vars < 100:
            print(f"  ⚠ velocity gene {adata.n_vars}개 — 비정상. HVG/spliced 점검 필요.")
        scv.tl.recover_dynamics(adata, n_jobs=cfg.N_JOBS)        # 병목(dynamical fit)
        scv.tl.velocity(adata, mode="dynamical")
        scv.tl.velocity_graph(adata, n_jobs=cfg.N_JOBS)
        scv.tl.latent_time(adata)
    print(f"done in {t.sec}s")

    # gene별 dynamical 파라미터 = lag/rate proxy (switch time fit_t_, rates alpha/beta/gamma)
    keep = [c for c in ["fit_t_", "fit_alpha", "fit_beta", "fit_gamma", "fit_scaling",
                        "fit_likelihood", "fit_r2", "velocity_genes"] if c in adata.var]
    genes = adata.var[keep].copy()
    genes.index.name = "gene"
    out_csv = cfg.RESULTS / "rna_only_dynamical_genes.csv"
    genes.to_csv(out_csv)
    print(f"✓ gene 파라미터 {genes.shape} → {out_csv.name} "
          f"(velocity_genes={int(adata.var.get('velocity_genes', pd.Series()).sum())})")

    out_h5 = cfg.OUT_VELO / "rna_only_dynamical.h5ad"
    adata.write_h5ad(out_h5)
    print(f"✓ adata → {out_h5}")

    log_runtime(cfg.RUNTIME_CSV, method=METHOD, arm=ARM,
                n_cells=adata.n_obs, n_genes=adata.n_vars,
                wall_sec=t.sec, peak_mb=peak_mem_mb(),
                note="scVelo dynamical floor (전역 velocity; within-lineage 분석은 P3)")
    print("다음: MultiVelo(mv env) chromatin-aware arm → P3 within-lineage 지표")
    return 0


if __name__ == "__main__":
    sys.exit(main())
