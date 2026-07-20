#!/usr/bin/env python3
"""P2 — run-to-run null refit (세포·ATAC 모두 고정, 적합만 반복).

문제: `velocity_matrix_paired_shuffle.md` 의 짝지은 Δ(=중앙값 +0.063)는 세포 재표본은 걷어냈지만
MultiVelo **적합 자체의 확률성(fit noise)** 은 못 걷어냈다. 즉 Δ = 크로마틴 효과 + fit 잡음.

이 스크립트는 그 바닥(run-to-run null)을 잰다. bootstrap refit 이 쓴 **같은 재표본 세포집합 S_b** 위에서
**ATAC 온전** 상태로 MultiVelo 를 다시 적합한다. 세포·입력·하이퍼파라미터가 legacy refit_b 와 전부 같고,
달라지는 것은 실행 시점과 (선택적으로) 병렬 worker 수뿐이다.

  A_legacy_b = data/velocity/multivelo_bootstrap/refit_<b>.h5ad   (2026-07-01, n_jobs=16) ← 읽기 전용
  A2_b       = 신규 재적합 (이 스크립트), n_jobs = --njobs

  · --njobs 16 → legacy 와 worker 수까지 동일 → **적합 결정론 여부**의 직접 측정
  · --njobs 12 → 짝맞춘 shuffle arm(B, n_jobs=12) 과 동일 조건 → 짝 Δ 와 같은 nj 대비를 갖는 null

fit 경로는 `p2_multivelo_bootstrap_refit.fit_once` 를 **그대로 import** 해서 쓴다(재구현 금지).
N_JOBS 만 모듈 전역으로 주입한다.

실행 (velo-mv env, CPU):
  TMPDIR=/tmp/mvrr MV_BOOT_NJOBS=16 /opt/envs/velo-mv/bin/python -u \
      scripts/p2_multivelo_runtorun_refit.py --boots 0,2 --njobs 16
출력: data/velocity/multivelo_runtorun/refit_rr_b<b>_nj<N>.h5ad (gitignore)
      results/runtorun_refit/refit_rr_b<b>_nj<N>.csv (tracked)
기존 multivelo_bootstrap/*, multivelo_bootstrap_shuffled/*, velocity_matrix_* 는 **읽기 전용**.
"""
from __future__ import annotations
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys
import numpy as np
import scanpy as sc
import scvelo as scv
try:
    import torch; torch.set_num_threads(1)
except Exception:
    pass
import p1_config as p1
import p2_config as cfg
from p2_util import peak_mem_mb, log_runtime
import p2_multivelo_bootstrap_refit as boot
from p2_multivelo_bootstrap_refit import canonical_genes, fit_once, SEED0
from p2_multivelo_paired_shuffle_refit import ref_obs   # legacy refit_b 의 obs_names (읽기 전용)

METHOD = "multivelo_runtorun"
FRAC = 0.70   # bootstrap refit / paired shuffle 과 동일


def main(boots, njobs, n_genes_smoke=0):
    boot.N_JOBS = njobs          # fit_once 가 참조하는 모듈 전역을 주입
    out_velo = cfg.OUT_VELO / "multivelo_runtorun"
    out_res = cfg.RESULTS / "runtorun_refit"
    out_velo.mkdir(parents=True, exist_ok=True)
    out_res.mkdir(parents=True, exist_ok=True)
    scv.settings.verbosity = 1
    tag = ".smoke" if n_genes_smoke else ""

    rna_full = sc.read_h5ad(p1.OUT_RNA)
    atac_full = sc.read_h5ad(cfg.IN_ATAC)
    print(f"load RNA {rna_full.shape} | ATAC {atac_full.shape} | boots={boots} njobs={njobs}", flush=True)
    if "spliced" not in rna_full.layers:
        print("✗ spliced/unspliced 없음 — P1 점검"); return 1
    keep_genes = canonical_genes()
    print(f"canonical gene {len(keep_genes)}", flush=True)

    for b in boots:
        stem = f"refit_rr_b{b}_nj{njobs}{tag}"
        out_csv = out_res / f"{stem}.csv"
        if out_csv.exists() and not n_genes_smoke:
            print(f"⏭  run-to-run refit b={b} nj={njobs} 이미 존재 → skip (resume)", flush=True)
            continue
        seed = SEED0 + b
        try:
            genes, adata, n_cells, sec = fit_once(
                rna_full, atac_full, keep_genes, FRAC, seed, n_genes_smoke)
        except Exception as e:
            print(f"✗ run-to-run refit b={b} nj={njobs} 실패: {type(e).__name__}: {e}", flush=True)
            continue
        ref = ref_obs(b)
        if ref is not None:
            same = np.array_equal(np.asarray(adata.obs_names), np.asarray(ref))
            print(f"  [b={b}] 세포집합 S_b == legacy refit_{b}: {same} ({adata.n_obs} cells)", flush=True)
            assert same, f"b={b}: 세포집합이 legacy refit 과 다르다 — run-to-run null 성립 안 함"
        genes.to_csv(out_csv)
        adata.write_h5ad(out_velo / f"{stem}.h5ad")
        print(f"✓ run-to-run refit b={b} nj={njobs} gene {genes.shape} → {out_csv.name} ({sec/60:.1f}min)",
              flush=True)
        log_runtime(cfg.RUNTIME_CSV, method=METHOD, arm=f"runtorun_refit:b{b}:nj{njobs}",
                    n_cells=n_cells, n_genes=genes.shape[0], wall_sec=sec,
                    peak_mb=peak_mem_mb(),
                    note=f"ATAC intact re-fit on identical S_b; subsample seed={seed}; njobs={njobs}")
    print("다음: p10e_runtorun_null_audit.py", flush=True)
    return 0


if __name__ == "__main__":
    bs = [0, 2]; ng = 0; nj = int(os.environ.get("MV_BOOT_NJOBS", "16"))
    if "--boots" in sys.argv:
        bs = [int(x) for x in sys.argv[sys.argv.index("--boots") + 1].split(",")]
    if "--njobs" in sys.argv:
        nj = int(sys.argv[sys.argv.index("--njobs") + 1])
    if "--genes" in sys.argv:
        ng = int(sys.argv[sys.argv.index("--genes") + 1])
    sys.exit(main(bs, nj, n_genes_smoke=ng))
