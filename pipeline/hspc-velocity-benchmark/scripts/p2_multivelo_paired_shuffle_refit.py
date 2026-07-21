#!/usr/bin/env python3
"""P2 — 짝맞춘(paired) ATAC-shuffle refit (critic MAJOR-2 해소).

문제: results/velocity_matrix_audit.md §4의 인과 비교가 **서로 다른 세포집합**을 견준다.
  - 재현성 천장 = bootstrap refit(재표본 15,315 cell) vs 원본 → 중심화 코사인 +0.872
  - ATAC 셔플   = 전량 21,878 cell vs 원본 → +0.838
같은 자가 아니다. 이 스크립트는 **bootstrap refit이 쓴 바로 그 재표본 세포집합 S_b** 위에서
ATAC만 셔플해 재적합한다 → 같은 세포·같은 하이퍼파라미터·같은 gene set, 유일한 차이는 ATAC 셔플.

설계(결과 보기 전 고정)
  - 세포 재표본: p2_multivelo_bootstrap_refit.fit_once 와 **동일 RNG**(seed = SEED0 + b, frac=0.70,
    비복원). 산출 h5ad의 obs_names 가 refit_b.h5ad 와 정확히 같은지 **assert** 로 증명한다.
  - 셔플 규약: p2_multivelo_scrambled.scramble_within_lineage 를 **그대로 import** (재구현 금지)
    → 기존 전량 셔플 arm과 같은 규약. 셔플 seed = RANDOM_SEED + b (b마다 다른 셔플 추출).
  - 나머지 전처리·fit 은 fit_once 와 동일(canonical gene ∩ HVG ∩ atac, max_iter=5, CPU).

실행 (velo-mv env, CPU):
  TMPDIR=/tmp/mvsh conda run --no-capture-output -n velo-mv \
      python -u scripts/p2_multivelo_paired_shuffle_refit.py --boots 0,1,2
출력: data/velocity/multivelo_bootstrap_shuffled/refit_shuf_<b>.h5ad (gitignore)
      results/bootstrap_refit_shuffled/refit_shuf_<b>.csv (tracked)
기존 results/bootstrap_refit/*, data/velocity/multivelo_scrambled.h5ad 는 **읽기 전용** — 건드리지 않는다.
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
from p2_multivelo_bootstrap_refit import canonical_genes, SEED0
from p2_multivelo_scrambled import scramble_within_lineage   # ★ 같은 셔플 규약 재사용

METHOD = "multivelo_paired_shuffle"
N_JOBS = int(os.environ.get("MV_BOOT_NJOBS", "12"))   # BIOP02 GPU job과 공존 → 12
FRAC = 0.70                                            # bootstrap refit과 동일


def fit_once_shuffled(rna_full, atac_full, keep_genes, frac, seed, shuf_seed,
                      ref_obs_names=None, n_genes_smoke=0):
    """fit_once 와 동일. 유일한 차이 = knn_smooth_chrom 직전 ATAC within-lineage 셔플."""
    rng = np.random.default_rng(seed)
    n = rna_full.n_obs
    take = rng.choice(n, size=int(round(frac * n)), replace=False)
    take.sort()
    rna = rna_full[take].copy()
    atac = atac_full[rna.obs_names].copy()
    if ref_obs_names is not None:
        assert np.array_equal(np.asarray(rna.obs_names), np.asarray(ref_obs_names)), \
            "재표본 세포집합이 refit_b 와 다르다 — paired 대조 성립 안 함"
        print(f"  [b seed={seed}] ✓ 세포집합 S_b 가 refit h5ad와 정확히 일치 ({rna.n_obs} cells)", flush=True)
    print(f"  [b seed={seed}] subsample {rna.n_obs}/{n} cell (frac={frac})", flush=True)

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
        shared = [g for g in keep_genes if g in set(rna.var_names) and g in set(atac.var_names)]
        if n_genes_smoke:
            shared = shared[:n_genes_smoke]
        rna = rna[:, shared].copy()
        atac = atac[rna.obs_names, shared].copy()
        print(f"  [b seed={seed}] gene {len(shared)} (canonical∩HVG∩atac), moments+umap ok", flush=True)

        # ★ 유일한 차이: ATAC within-lineage 셔플 (원본 scrambled arm과 동일 함수)
        if "lineage" not in rna.obs.columns:
            raise RuntimeError("lineage 라벨 없음 — within-lineage 셔플 불가")
        atac = scramble_within_lineage(atac, rna.obs["lineage"].values, shuf_seed)

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
            print(f"  [b={seed} shuf] {done}/{len(shared)} | {el/60:.1f}min ETA~{eta/60:.0f}min", flush=True)
        adata = ad.concat(parts, axis=1, merge="first") if len(parts) > 1 else parts[0]

    keep = [c for c in adata.var.columns if c.startswith("fit_")]
    genes = adata.var[keep].copy(); genes.index.name = "gene"
    if {"fit_t_sw2", "fit_t_sw1"}.issubset(genes.columns):
        genes["lag"] = genes["fit_t_sw2"] - genes["fit_t_sw1"]
    return genes, adata, rna.n_obs, t.sec


def ref_obs(b):
    """짝이 되는 기존 refit_b.h5ad 의 obs_names (읽기 전용)."""
    import h5py
    p = cfg.OUT_VELO / "multivelo_bootstrap" / f"refit_{b}.h5ad"
    if not p.exists():
        return None
    with h5py.File(p, "r") as f:
        g = f["obs"]; idx = g.attrs.get("_index", "_index"); d = g[idx][:]
    return np.array([x.decode() if isinstance(x, bytes) else x for x in d])


def main(boots, n_genes_smoke=0):
    out_velo = cfg.OUT_VELO / "multivelo_bootstrap_shuffled"
    out_res = cfg.RESULTS / "bootstrap_refit_shuffled"
    out_velo.mkdir(parents=True, exist_ok=True)
    out_res.mkdir(parents=True, exist_ok=True)
    scv.settings.verbosity = 1
    tag = ".smoke" if n_genes_smoke else ""

    rna_full = sc.read_h5ad(p1.OUT_RNA)
    atac_full = sc.read_h5ad(cfg.IN_ATAC)
    print(f"load RNA {rna_full.shape} | ATAC {atac_full.shape} | boots={boots} njobs={N_JOBS}", flush=True)
    if "spliced" not in rna_full.layers:
        print("✗ spliced/unspliced 없음 — P1 점검"); return 1
    keep_genes = canonical_genes()
    print(f"canonical gene {len(keep_genes)}", flush=True)

    for b in boots:
        out_csv = out_res / f"refit_shuf_{b}{tag}.csv"
        if out_csv.exists() and not n_genes_smoke:
            print(f"⏭  paired-shuffle refit {b} 이미 존재 → skip (resume)", flush=True)
            continue
        seed = SEED0 + b
        shuf_seed = cfg.RANDOM_SEED + b
        try:
            genes, adata, n_cells, sec = fit_once_shuffled(
                rna_full, atac_full, keep_genes, FRAC, seed, shuf_seed,
                ref_obs_names=ref_obs(b), n_genes_smoke=n_genes_smoke)
        except Exception as e:
            print(f"✗ paired-shuffle refit {b} 실패: {type(e).__name__}: {e}", flush=True)
            continue
        genes.to_csv(out_csv)
        adata.write_h5ad(out_velo / f"refit_shuf_{b}{tag}.h5ad")
        print(f"✓ paired-shuffle refit {b} gene {genes.shape} → {out_csv.name} ({sec/60:.1f}min)", flush=True)
        log_runtime(cfg.RUNTIME_CSV, method=METHOD, arm=f"paired_shuffle_refit:b{b}",
                    n_cells=n_cells, n_genes=genes.shape[0], wall_sec=sec,
                    peak_mb=peak_mem_mb(),
                    note=f"paired ATAC within-lineage shuffle; subsample seed={seed} shuf_seed={shuf_seed}")
    print("다음: p10d_paired_shuffle_audit.py", flush=True)
    return 0


if __name__ == "__main__":
    bs = [0, 1, 2]; ng = 0
    if "--boots" in sys.argv:
        bs = [int(x) for x in sys.argv[sys.argv.index("--boots") + 1].split(",")]
    if "--genes" in sys.argv:
        ng = int(sys.argv[sys.argv.index("--genes") + 1])
    sys.exit(main(bs, n_genes_smoke=ng))
