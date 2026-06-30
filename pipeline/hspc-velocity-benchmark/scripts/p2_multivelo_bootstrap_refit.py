#!/usr/bin/env python3
"""P2 — MultiVelo 전체 re-fit bootstrap (α_c·lag 진짜 stability). DESIGN §4D.

p5_bootstrap_stability.py는 **fit 고정**(latent_time 고정) 하에 cell 표집만 봐서 'stability 하한'.
본 스크립트는 그게 명시적으로 남긴 미완 — **전체 re-fit 반복**(cell subsample마다 MultiVelo를 처음부터
다시 fit) — 을 수행해 α_c(chromatin opening rate)와 lag(switch time 차) 추정의 **진짜 안정성**을 측정한다.

핵심 가설(H1 정합): α 계열(α, α_c)은 method 간 robust(ρ=0.88/0.29)였다 → re-fit에도 안정해야 하고,
lag은 비robust → re-fit마다 크게 흔들려야 한다. 같은 데이터·같은 method 안에서 **재fit 안정성**으로
'α는 쓸 수 있고 lag은 못 쓴다'를 한 번 더 직접 검증.

설계
  - canonical gene set = results/multivelo_genes.csv (전역 fit 동일 gene) 으로 고정 → 깨끗한 per-gene 비교.
  - b회: 전체 cell의 fraction(기본 0.70)을 **비복원 subsample**(seed별) → p2_multivelo와 동일 substrate
    (filter_and_normalize→moments→knn_smooth_chrom) → recover_dynamics_chrom → fit param 추출.
    * 복원추출(replacement) 대신 subsample: 중복 cell이 kNN graph를 0거리로 붕괴시키는 것을 피함(refit-stability 표준).
  - 추출: fit_alpha_c, fit_alpha, lag=fit_t_sw2−fit_t_sw1. refit별 results/bootstrap_refit/refit_<b>.csv (incremental).

실행 (mv env):
  conda run --no-capture-output -n mv python -u scripts/p2_multivelo_bootstrap_refit.py            # full B=12
  ... --boot 4 --genes 12 --frac 0.5                                                               # 스모크
출력: data/velocity/multivelo_bootstrap/refit_<b>.h5ad (gitignore) + results/bootstrap_refit/refit_<b>.csv (tracked)
"""
from __future__ import annotations
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys
import time as _time
import numpy as np
import scanpy as sc
import scvelo as scv
import anndata as ad
import multivelo as mv
try:
    import torch; torch.set_num_threads(1)
except Exception:
    pass
import p1_config as p1
import p2_config as cfg
from p2_util import timer, peak_mem_mb, log_runtime

METHOD = "multivelo_bootstrap"
N_JOBS = int(os.environ.get("MV_BOOT_NJOBS", "16"))   # idle 32코어 → fit당 더 많은 gene 병렬
SEED0 = 20260701


def canonical_genes():
    import pandas as pd
    p = cfg.RESULTS / "multivelo_genes.csv"
    return list(pd.read_csv(p, index_col=0).index)


def fit_once(rna_full, atac_full, keep_genes, frac, seed, n_genes_smoke=0):
    """전체 cell의 frac을 비복원 subsample → MultiVelo 재fit → (genes_df, adata, n_cells, sec)."""
    rng = np.random.default_rng(seed)
    n = rna_full.n_obs
    take = rng.choice(n, size=int(round(frac * n)), replace=False)
    take.sort()
    rna = rna_full[take].copy()
    atac = atac_full[rna.obs_names].copy()
    print(f"  [b seed={seed}] subsample {rna.n_obs}/{n} cell (frac={frac})", flush=True)

    if "counts" in rna.layers:
        rna.X = rna.layers["counts"].copy()
    with timer() as t:
        # 전역 fit과 동일 substrate: HVG(2000)에서 moments/그래프/umap → 그 뒤 canonical gene으로 subset.
        # (moments·kNN graph·X_umap는 HVG 전체 기준이어야 전역 fit과 정합; recover_dynamics_chrom이 X_umap 요구.)
        scv.pp.filter_and_normalize(rna, min_shared_counts=cfg.MIN_SHARED_COUNTS)
        if "highly_variable" not in rna.var.columns:
            sc.pp.highly_variable_genes(rna, n_top_genes=cfg.N_TOP_GENES)
        rna = rna[:, rna.var["highly_variable"]].copy()
        scv.pp.moments(rna, n_pcs=cfg.N_PCS, n_neighbors=cfg.N_NEIGHBORS)
        if "X_umap" not in rna.obsm:
            sc.tl.umap(rna, random_state=cfg.RANDOM_SEED)
        # canonical gene set 고정 (HVG 변동 제거) ∩ atac ∩ 생존 gene
        shared = [g for g in keep_genes if g in set(rna.var_names) and g in set(atac.var_names)]
        if n_genes_smoke:
            shared = shared[:n_genes_smoke]
        rna = rna[:, shared].copy()
        atac = atac[rna.obs_names, shared].copy()
        print(f"  [b seed={seed}] gene {len(shared)} (canonical∩HVG∩atac), moments+umap ok", flush=True)

        mv.knn_smooth_chrom(atac, conn=rna.obsp["connectivities"])
        chunk = max(1, cfg.MV_CHUNK)
        parts, _t0 = [], _time.perf_counter()
        for i in range(0, len(shared), chunk):
            sub = shared[i:i + chunk]
            res = mv.recover_dynamics_chrom(
                rna[:, sub].copy(), atac[:, sub].copy(),
                max_iter=5, device="cpu", parallel=True, n_jobs=N_JOBS)
            parts.append(res)
            done = min(i + chunk, len(shared)); el = _time.perf_counter() - _t0
            eta = el / done * (len(shared) - done)
            print(f"  [b seed={seed}] {done}/{len(shared)} | {el/60:.1f}min ETA~{eta/60:.0f}min", flush=True)
        adata = ad.concat(parts, axis=1, merge="first") if len(parts) > 1 else parts[0]

    keep = [c for c in adata.var.columns if c.startswith("fit_")]
    genes = adata.var[keep].copy(); genes.index.name = "gene"
    if {"fit_t_sw2", "fit_t_sw1"}.issubset(genes.columns):
        genes["lag"] = genes["fit_t_sw2"] - genes["fit_t_sw1"]
    return genes, adata, rna.n_obs, t.sec


def main(n_boot=12, n_genes_smoke=0, frac=0.70):
    out_velo = cfg.OUT_VELO / "multivelo_bootstrap"
    out_res = cfg.RESULTS / "bootstrap_refit"
    out_velo.mkdir(parents=True, exist_ok=True)
    out_res.mkdir(parents=True, exist_ok=True)
    scv.settings.verbosity = 1
    tag = ".smoke" if n_genes_smoke else ""

    rna_full = sc.read_h5ad(p1.OUT_RNA)
    atac_full = sc.read_h5ad(cfg.IN_ATAC)
    print(f"load RNA {rna_full.shape} | ATAC {atac_full.shape} | B={n_boot} frac={frac} njobs={N_JOBS}", flush=True)
    if "spliced" not in rna_full.layers:
        print("✗ spliced/unspliced 없음 — P1 점검"); return 1
    keep_genes = canonical_genes()
    print(f"canonical gene {len(keep_genes)}", flush=True)

    for b in range(n_boot):
        out_csv = out_res / f"refit_{b}{tag}.csv"
        if out_csv.exists() and not n_genes_smoke:
            print(f"⏭  refit {b} 이미 존재 → skip (resume)", flush=True)
            continue
        seed = SEED0 + b
        try:
            genes, adata, n_cells, sec = fit_once(
                rna_full, atac_full, keep_genes, frac, seed, n_genes_smoke)
        except Exception as e:
            print(f"✗ refit {b} 실패: {type(e).__name__}: {e}", flush=True)
            continue
        genes.to_csv(out_csv)
        print(f"✓ refit {b} gene {genes.shape} → {out_csv.relative_to(cfg.ROOT)} ({sec/60:.1f}min)", flush=True)
        adata.write_h5ad(out_velo / f"refit_{b}{tag}.h5ad")
        log_runtime(cfg.RUNTIME_CSV, method=METHOD, arm=f"bootstrap_refit:b{b}",
                    n_cells=n_cells, n_genes=genes.shape[0], wall_sec=sec,
                    peak_mb=peak_mem_mb(), note=f"subsample frac={frac} seed={seed}")
    print("다음: p3_bootstrap_refit.py (α_c vs lag 재fit 안정성)", flush=True)
    return 0


if __name__ == "__main__":
    nb = 12; ng = 0; fr = 0.70
    if "--boot" in sys.argv:
        nb = int(sys.argv[sys.argv.index("--boot") + 1])
    if "--genes" in sys.argv:
        ng = int(sys.argv[sys.argv.index("--genes") + 1])
    if "--frac" in sys.argv:
        fr = float(sys.argv[sys.argv.index("--frac") + 1])
    sys.exit(main(n_boot=nb, n_genes_smoke=ng, frac=fr))
