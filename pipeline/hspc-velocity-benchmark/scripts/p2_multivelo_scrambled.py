#!/usr/bin/env python3
"""P2 음성대조 — scrambled-chromatin null (DESIGN §43/§75, REQUIRED).

p2_multivelo.py 와 **동일 substrate·동일 fit**, 단 ATAC를 **within-lineage cell 셔플**한 뒤 fit.
→ chromatin↔RNA 의 cell 수준 결합만 파괴(per-gene chromatin marginal·lineage 구성은 보존).
원본 대비 lag 분포가 붕괴/무의미해지면 chromatin 채널이 실제 신호, 거의 안 변하면 '장식'.

셔플: 각 lineage 내부에서 ATAC 행(cell)을 permute. seed 고정(RANDOM_SEED).
실행 (mv env, CPU — GPU 미사용 → cisTopic과 병렬 가능):
  conda run --no-capture-output -n velo-mv python -u scripts/p2_multivelo_scrambled.py        # full(~7h)
  ... --genes 20    # smoke
출력: results/scrambled_genes.csv, data/velocity/multivelo_scrambled.h5ad, runtime.csv(append)
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
import p2_config as cfg
from p2_util import timer, peak_mem_mb, log_runtime

METHOD = "multivelo_scrambled"


def scramble_within_lineage(atac, lineage, seed):
    """각 lineage 내부에서 ATAC 행(cell) permute → chromatin↔RNA cell 결합 파괴."""
    rng = np.random.default_rng(seed)
    lin = np.asarray(lineage)
    perm = np.arange(atac.n_obs)
    for L in np.unique(lin):
        idx = np.where(lin == L)[0]
        perm[idx] = rng.permutation(idx)
    names = atac.obs_names.to_numpy()
    out = atac[perm].copy()
    out.obs_names = names          # 위치(graph 인덱스)는 원본 cell, X만 같은 lineage 내 swap
    moved = float((perm != np.arange(atac.n_obs)).mean())
    print(f"  scramble: {len(np.unique(lin))} lineage, 이동 cell 비율 {moved:.1%}", flush=True)
    return out


def main(n_genes_smoke=0):
    cfg.OUT_VELO.mkdir(parents=True, exist_ok=True)
    cfg.RESULTS.mkdir(parents=True, exist_ok=True)
    scv.settings.verbosity = 1
    arm = "scrambled_chromatin_null"
    tag = ".smoke" if n_genes_smoke else ""

    rna = sc.read_h5ad(cfg.IN_RNA)
    atac = sc.read_h5ad(cfg.IN_ATAC)
    print(f"load RNA {rna.shape} | ATAC {atac.shape}")
    if "spliced" not in rna.layers:
        print("✗ spliced/unspliced 없음 — P1 점검"); return 1
    if "lineage" not in rna.obs.columns:
        print("✗ lineage 라벨 없음 — scramble 불가"); return 1

    if "counts" in rna.layers:
        rna.X = rna.layers["counts"].copy()
    with timer() as t:
        scv.pp.filter_and_normalize(rna, min_shared_counts=cfg.MIN_SHARED_COUNTS)
        if "highly_variable" not in rna.var.columns:
            sc.pp.highly_variable_genes(rna, n_top_genes=cfg.N_TOP_GENES)
        rna = rna[:, rna.var["highly_variable"]].copy()
        scv.pp.moments(rna, n_pcs=cfg.N_PCS, n_neighbors=cfg.N_NEIGHBORS)
        if "X_umap" not in rna.obsm:
            sc.tl.umap(rna, random_state=cfg.RANDOM_SEED)

        shared = [g for g in rna.var_names if g in set(atac.var_names)]
        if n_genes_smoke:
            shared = shared[:n_genes_smoke]
        rna = rna[:, shared].copy()
        atac = atac[rna.obs_names, shared].copy()      # cell/gene 정렬 (원본과 동일)
        print(f"shared gene set: {len(shared)}, cells {rna.n_obs}")

        # ★ 음성대조 핵심: ATAC를 within-lineage 셔플 (원본 p2_multivelo와 유일한 차이)
        atac = scramble_within_lineage(atac, rna.obs["lineage"].values, cfg.RANDOM_SEED)

        mv.knn_smooth_chrom(atac, conn=rna.obsp["connectivities"])

        nj = cfg.MV_NJOBS if cfg.MV_PARALLEL else None
        chunk = max(1, cfg.MV_CHUNK)
        parts, _t0 = [], _time.perf_counter()
        for i in range(0, len(shared), chunk):
            sub = shared[i:i + chunk]
            res = mv.recover_dynamics_chrom(
                rna[:, sub].copy(), atac[:, sub].copy(),
                max_iter=5, device="cpu", parallel=cfg.MV_PARALLEL, n_jobs=nj)
            parts.append(res)
            done = min(i + chunk, len(shared)); el = _time.perf_counter() - _t0
            eta = el / done * (len(shared) - done)
            print(f"  [scrambled] {done}/{len(shared)} genes | {el/60:.1f}min, ETA ~{eta/60:.0f}min", flush=True)
        adata_result = ad.concat(parts, axis=1, merge="first") if len(parts) > 1 else parts[0]
    print(f"done in {t.sec}s")

    keep = [c for c in adata_result.var.columns if c.startswith("fit_")]
    genes = adata_result.var[keep].copy(); genes.index.name = "gene"
    out_csv = cfg.RESULTS / f"scrambled_genes{tag}.csv"
    genes.to_csv(out_csv)
    print(f"✓ gene fit {genes.shape} → {out_csv.name}")

    adata_result.write_h5ad(cfg.OUT_VELO / f"multivelo_scrambled{tag}.h5ad")
    log_runtime(cfg.RUNTIME_CSV, method=METHOD, arm=arm,
                n_cells=rna.n_obs, n_genes=rna.n_vars, wall_sec=t.sec,
                peak_mb=peak_mem_mb(),
                note=f"within-lineage ATAC shuffle; smoke n={n_genes_smoke}" if n_genes_smoke
                     else "within-lineage ATAC shuffle (null)")
    print("다음: results/scrambled_null.md — 원본 multivelo lag 분포 대비 검정")
    return 0


if __name__ == "__main__":
    n = 0
    if "--genes" in sys.argv:
        n = int(sys.argv[sys.argv.index("--genes") + 1])
    sys.exit(main(n_genes_smoke=n))
