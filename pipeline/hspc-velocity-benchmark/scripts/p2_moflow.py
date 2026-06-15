#!/usr/bin/env python3
"""P2 — MoFlow (chromatin-aware, latent time-free relay velocity). DESIGN §2. H1 한 축.

DL arm: **GPU 머신에서 실행 권장** (CPU full run은 수일 — env/GPU-SETUP.md §런타임).
입력 = p2_dl_prep.py 산출(dl_input_rna: Ms/Mu/X_umap, dl_input_atac: Mc).

lag = MoFlow DTW **c-s lag**(chromatin→spliced), get_dtw()의 time_lag_c_s gene별 요약.
sign이 가변이라 DESIGN §4B의 진짜 directional sign check 대상 (MultiVelo sw2-sw1과 달리).

실행:
  PYTHONPATH=pipeline/hspc-velocity-benchmark/vendor/MoFlow/src \
    conda run -n torch python pipeline/hspc-velocity-benchmark/scripts/p2_moflow.py [--genes N] [--gpu]
출력: results/moflow_genes.csv, data/velocity/moflow.h5ad, runtime.csv
"""
from __future__ import annotations
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")    # macOS loky fork-safe (Linux GPU선 무관)
import sys
import numpy as np
import scanpy as sc
import p2_config as cfg
from p2_util import timer, peak_mem_mb, log_runtime

from MoFlow.moflow import MOFlow            # PYTHONPATH=vendor/MoFlow/src
from MoFlow.eval_dtw import get_dtw

METHOD = "moflow"


def main(n_genes=0, gpu=False):
    cfg.OUT_VELO.mkdir(parents=True, exist_ok=True); cfg.RESULTS.mkdir(parents=True, exist_ok=True)
    tag = ".smoke" if n_genes else ""
    rna = sc.read_h5ad(cfg.OUT_VELO / "dl_input_rna.h5ad")
    atac = sc.read_h5ad(cfg.OUT_VELO / "dl_input_atac.h5ad")
    if n_genes:
        g = list(rna.var_names[:n_genes]); rna = rna[:, g].copy(); atac = atac[:, g].copy()
    print(f"MoFlow: {rna.n_vars} genes, {rna.n_obs} cells, gpu={gpu}")

    import scvelo as scv
    with timer() as t:
        m = MOFlow(rna, atac, embed="X_umap",
                   device=("cuda" if gpu else None))    # device=None → CPU accelerator
        # velocity()는 fit gene subset + velo layer를 담은 새 adata를 *반환*.
        result = m.velocity(rna, n_jobs=cfg.MV_NJOBS, save_path=str(cfg.OUT_VELO / f"moflow{tag}_out"))
        # get_dtw(timekey='velo_s_pseudotime') 위해 pseudotime 계산
        scv.tl.velocity_graph(result, vkey="velo_s")
        scv.tl.velocity_pseudotime(result, vkey="velo_s")   # → obs['velo_s_pseudotime']
    print(f"학습 done in {t.sec}s")

    # gene별 c-s lag(time_lag_c_s) 요약 → DESIGN §4B lag-specific (sign 가변)
    rows = {}
    for gene in result.var_names:
        try:
            *_, time_lag_c_s, _ = get_dtw(result, gene)
            arr = np.asarray(time_lag_c_s, float)
            rows[gene] = dict(cs_lag_mean=np.nanmean(arr), cs_lag_median=np.nanmedian(arr))
        except Exception as e:
            rows[gene] = dict(cs_lag_mean=np.nan, cs_lag_median=np.nan, err=str(e)[:40])
    import pandas as pd
    genes = pd.DataFrame(rows).T; genes.index.name = "gene"
    out_csv = cfg.RESULTS / f"moflow_genes{tag}.csv"; genes.to_csv(out_csv)
    n_ok = int(genes["cs_lag_median"].notna().sum())
    print(f"✓ c-s lag {genes.shape}, 산출 gene {n_ok} → {out_csv.name}")

    result.write_h5ad(cfg.OUT_VELO / f"moflow{tag}.h5ad")
    log_runtime(cfg.RUNTIME_CSV, method=METHOD, arm="chromatin_aware",
                n_cells=result.n_obs, n_genes=result.n_vars, wall_sec=t.sec, peak_mb=peak_mem_mb(),
                note=f"DTW c-s lag; gpu={gpu}; smoke n={n_genes}" if n_genes else f"DTW c-s lag; gpu={gpu}")
    return 0


if __name__ == "__main__":
    n = int(sys.argv[sys.argv.index("--genes") + 1]) if "--genes" in sys.argv else 0
    sys.exit(main(n_genes=n, gpu=("--gpu" in sys.argv)))
