#!/usr/bin/env python3
"""P2 — MoFlow run-to-run null 재적합 (세포·ATAC 모두 고정, 독립 재실행만 반복). MAJOR-1 해소용.

문제: 층② 세포x유전자 velocity 행렬 감사(`velocity_matrix_audit.md`)에서 MoFlow가 낀 세 쌍
     (MV×MoFlow -0.012, MoFlow×CRAK +0.003, MoFlow×VAE +0.003)은 전부 0 근처인데, MoFlow는
     같은 설정 재실행 대조가 한 번도 없어 이 값이 method 간 실제 불일치인지 MoFlow 한 arm의
     내부 불안정인지 구분되지 않는다(REVIEW-GB-2026-07-19b MAJOR-1 (1)). MoFlow 원본×ATAC-shuffle
     값(+0.113, `velocity_matrix_audit.md` §6)도 같은 이유로 해석 불가로 남아 있다.
해결: MultiVelo에 이미 있는 run-to-run null(`p2_multivelo_runtorun_refit.py` / `p10e_...`)을
     그대로 미러링한다. 단 MoFlow는 세포 bootstrap이 아니라 **전체 세포 단일 fit**이므로 "b" 축이
     없다. 대신 **동일 입력(전체 세포, ATAC 온전)으로 독립 재실행을 반복**해 MoFlow 학습 자체의
     확률성(weight init·optimizer 등)이 만드는 잡음 바닥을 잰다.

  A (기존, 읽기전용)  = data/velocity/moflow.h5ad   (원본, 층② 표에 쓰인 그 fit)
  A2_run<N> (신규)   = 이 스크립트 — 같은 dl_input, ATAC 온전, run 번호만 다름

fit 경로는 `p2_moflow.fit_once` 를 그대로 import 해서 쓴다(재구현 금지).

GPU: MoFlow 계열 스크립트 관례대로 CUDA_VISIBLE_DEVICES=1(BIOP01 전용 cuda:1)로 실행.
실행 (velo-torch env, GPU):
  CUDA_VISIBLE_DEVICES=1 PYTHONPATH=<repo>/vendor/MoFlow/src \
    conda run --no-capture-output -n velo-torch python -u scripts/p2_moflow_runtorun_refit.py --runs 2 --gpu
출력: data/velocity/moflow_runtorun/moflow_rr_run<N>.h5ad (gitignore)
      results/moflow_runtorun_refit/moflow_rr_run<N>_genes.csv (tracked)
기존 moflow.h5ad / moflow_scrambled.h5ad / velocity_matrix_* 는 읽기 전용.
"""
from __future__ import annotations
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import sys
import numpy as np
import scanpy as sc
import p2_config as cfg
from p2_util import peak_mem_mb, log_runtime
from p2_moflow import fit_once   # 재구현 금지 — 원본 fit 경로 재사용

METHOD = "moflow_runtorun"


def main(n_runs=2, gpu=False, n_jobs=None, n_genes_smoke=0):
    n_jobs = n_jobs or cfg.MV_NJOBS
    out_velo = cfg.OUT_VELO / "moflow_runtorun"
    out_res = cfg.RESULTS / "moflow_runtorun_refit"
    out_velo.mkdir(parents=True, exist_ok=True)
    out_res.mkdir(parents=True, exist_ok=True)
    tag = ".smoke" if n_genes_smoke else ""

    rna = sc.read_h5ad(cfg.OUT_VELO / f"dl_input_rna{cfg.SUFFIX}.h5ad")
    atac = sc.read_h5ad(cfg.OUT_VELO / f"dl_input_atac{cfg.SUFFIX}.h5ad")
    if n_genes_smoke:
        g = list(rna.var_names[:n_genes_smoke]); rna = rna[:, g].copy(); atac = atac[:, g].copy()
    print(f"MoFlow run-to-run: {rna.n_vars} genes, {rna.n_obs} cells, gpu={gpu}, runs={n_runs}", flush=True)

    legacy_path = cfg.OUT_VELO / f"moflow{cfg.SUFFIX}.h5ad"
    ref_obs = None
    if legacy_path.exists():
        ref_obs = np.asarray(sc.read_h5ad(legacy_path, backed="r").obs_names)
    else:
        print(f"  ⚠ legacy {legacy_path.name} 없음 — 세포집합 대조 skip", flush=True)

    for run in range(1, n_runs + 1):
        stem = f"moflow_rr_run{run}{tag}"
        out_csv = out_res / f"{stem}_genes.csv"
        if out_csv.exists() and not n_genes_smoke:
            print(f"⏭  run-to-run refit run={run} 이미 존재 → skip (resume)", flush=True)
            continue
        try:
            genes, result, sec = fit_once(rna, atac, gpu, n_jobs, save_tag=stem)
        except Exception as e:
            print(f"✗ run-to-run refit run={run} 실패: {type(e).__name__}: {e}", flush=True)
            continue
        if ref_obs is not None:
            same = np.array_equal(np.asarray(result.obs_names), ref_obs)
            print(f"  [run={run}] 세포집합 == legacy moflow.h5ad: {same} ({result.n_obs} cells)", flush=True)
            assert same, f"run={run}: 세포집합이 legacy moflow.h5ad 와 다르다 — run-to-run null 성립 안 함"
        genes.to_csv(out_csv)
        result.write_h5ad(out_velo / f"{stem}.h5ad")
        n_ok = int(genes["cs_lag_median"].notna().sum())
        print(f"✓ run-to-run refit run={run} gene {genes.shape} ok={n_ok} → {out_csv.name} ({sec/60:.1f}min)",
              flush=True)
        log_runtime(cfg.RUNTIME_CSV, method=METHOD, arm=f"runtorun_refit:run{run}",
                    n_cells=result.n_obs, n_genes=result.n_vars, wall_sec=sec, peak_mb=peak_mem_mb(),
                    note=f"ATAC intact independent re-run; gpu={gpu}; smoke n={n_genes_smoke}"
                         if n_genes_smoke else f"ATAC intact independent re-run; gpu={gpu}")
    print("다음: p10g_moflow_runtorun_null_audit.py", flush=True)
    return 0


if __name__ == "__main__":
    nr = 2; ng = 0; nj = None
    if "--runs" in sys.argv:
        nr = int(sys.argv[sys.argv.index("--runs") + 1])
    if "--genes" in sys.argv:
        ng = int(sys.argv[sys.argv.index("--genes") + 1])
    if "--n-jobs" in sys.argv:
        nj = int(sys.argv[sys.argv.index("--n-jobs") + 1])
    sys.exit(main(n_runs=nr, gpu=("--gpu" in sys.argv), n_jobs=nj, n_genes_smoke=ng))
