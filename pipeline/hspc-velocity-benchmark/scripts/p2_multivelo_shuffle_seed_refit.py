#!/usr/bin/env python3
"""P2 — 셔플 draw 변동(shuffle-seed 반복) refit.

남은 구멍: `velocity_matrix_paired_shuffle.md` 의 짝 Δ(A−B)는 b 마다 **셔플 추출 1회**에만 기댄다.
`velocity_matrix_runtorun_null.md` 가 적합이 결정론임을 실측했으므로, 같은 S_b·같은 셔플 규약에서
**셔플 seed 만 바꿔** 재적합하면 seed 간 Δ 변동은 전부 **셔플 draw 변동**이다(fit 잡음 성분 없음).

  A_b   = data/velocity/multivelo_bootstrap/refit_<b>.h5ad          (읽기 전용, 재적합 불필요=결정론)
  B_b,s = 이 스크립트 (같은 S_b, ATAC within-lineage 셔플, 셔플 seed = s)

fit 경로는 `p2_multivelo_paired_shuffle_refit.fit_once_shuffled` 를 **그대로 import** 한다(재구현 금지).
셔플 규약도 그 경로가 쓰는 `p2_multivelo_scrambled.scramble_within_lineage` 그대로이고, seed 만 바뀐다.

seed 설계(결과 보기 전 고정): b 별 [b(기존 draw), 101+b, 202+b, 303+b].
  · 기존 draw(seed=b)는 이미 `results/bootstrap_refit_shuffled/refit_shuf_<b>.csv` 로 있으므로 재적합하지 않는다.
  · 이 스크립트는 신규 3 draw 만 적합한다.

실행 (velo-mv env, CPU):
  TMPDIR=/tmp/mvs0 /opt/envs/velo-mv/bin/python -u \
      scripts/p2_multivelo_shuffle_seed_refit.py --boots 0 --njobs 12
출력: data/velocity/multivelo_shuffle_seeds/refit_shufseed_b<b>_s<seed>.h5ad (gitignore)
      results/bootstrap_refit_shuffled_seeds/refit_shufseed_b<b>_s<seed>.csv (tracked)
기존 multivelo_bootstrap/*, multivelo_bootstrap_shuffled/*, multivelo_runtorun/*,
     velocity_matrix_* , FINDINGS.md, draft* 는 전부 **읽기 전용** — 건드리지 않는다.
"""
from __future__ import annotations
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys
import scanpy as sc
import scvelo as scv
try:
    import torch; torch.set_num_threads(1)
except Exception:
    pass
import p1_config as p1
import p2_config as cfg
from p2_util import peak_mem_mb, log_runtime
import p2_multivelo_paired_shuffle_refit as psr
from p2_multivelo_paired_shuffle_refit import fit_once_shuffled, ref_obs
from p2_multivelo_bootstrap_refit import canonical_genes, SEED0

METHOD = "multivelo_shuffle_seed"
FRAC = 0.70          # bootstrap refit / paired shuffle 과 동일
NEW_SEED_OFFSETS = (101, 202, 303)   # 기존 draw(seed=b) 에 더할 신규 셔플 seed 오프셋


def seeds_for(b):
    """b 의 셔플 seed 목록 (첫 항목 = 기존 draw)."""
    return [b] + [off + b for off in NEW_SEED_OFFSETS]


def main(boots, njobs, n_genes_smoke=0):
    psr.N_JOBS = njobs           # fit_once_shuffled 가 참조하는 모듈 전역 주입
    out_velo = cfg.OUT_VELO / "multivelo_shuffle_seeds"
    out_res = cfg.RESULTS / "bootstrap_refit_shuffled_seeds"
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
        for shuf_seed in seeds_for(b)[1:]:      # 기존 draw 는 재적합하지 않는다
            stem = f"refit_shufseed_b{b}_s{shuf_seed}{tag}"
            out_csv = out_res / f"{stem}.csv"
            if out_csv.exists() and not n_genes_smoke:
                print(f"⏭  {stem} 이미 존재 → skip (resume)", flush=True)
                continue
            seed = SEED0 + b
            try:
                genes, adata, n_cells, sec = fit_once_shuffled(
                    rna_full, atac_full, keep_genes, FRAC, seed, shuf_seed,
                    ref_obs_names=ref_obs(b), n_genes_smoke=n_genes_smoke)
            except Exception as e:
                print(f"✗ {stem} 실패: {type(e).__name__}: {e}", flush=True)
                continue
            genes.to_csv(out_csv)
            adata.write_h5ad(out_velo / f"{stem}.h5ad")
            print(f"✓ {stem} gene {genes.shape} → {out_csv.name} ({sec/60:.1f}min)", flush=True)
            log_runtime(cfg.RUNTIME_CSV, method=METHOD,
                        arm=f"shuffle_seed_refit:b{b}_s{shuf_seed}{'_SMOKE' if n_genes_smoke else ''}",
                        n_cells=n_cells, n_genes=genes.shape[0], wall_sec=sec,
                        peak_mb=peak_mem_mb(),
                        note=f"{'SMOKE ' if n_genes_smoke else ''}shuffle-draw variability; "
                             f"subsample seed={seed} shuf_seed={shuf_seed}; njobs={njobs}")
    print("다음: p10f_shuffle_seed_variability_audit.py", flush=True)
    return 0


if __name__ == "__main__":
    bs = [0, 1, 2]; nj = int(os.environ.get("MV_BOOT_NJOBS", "12")); ng = 0
    if "--boots" in sys.argv:
        bs = [int(x) for x in sys.argv[sys.argv.index("--boots") + 1].split(",")]
    if "--njobs" in sys.argv:
        nj = int(sys.argv[sys.argv.index("--njobs") + 1])
    if "--genes" in sys.argv:
        ng = int(sys.argv[sys.argv.index("--genes") + 1])
    sys.exit(main(bs, nj, n_genes_smoke=ng))
