#!/usr/bin/env python3
"""P2 음성대조 — MoFlow scrambled-chromatin null (Track C / novelty_strategy §4.2).

p2_moflow.py 와 **동일 substrate·동일 fit**, 단 ATAC를 **within-lineage cell 셔플**한 뒤 재smooth
→ chromatin↔RNA 의 cell 수준 결합만 파괴(per-gene chromatin marginal·lineage 구성은 보존).
MultiVelo 음성대조(p2_multivelo_scrambled.py)와 apples-to-apples:
  - 동일 scramble_within_lineage() + 동일 RANDOM_SEED (raw ATAC 행 permute)
  - 동일 smooth_chrom()(knn_smooth_chrom 등가, dl_prep과 동일) 재smooth → Mc
  - 나머지 MoFlow fit 설정은 원본 full run과 동일 (default epoch/patience/…)

원본 moflow_genes.csv 는 절대 덮어쓰지 않음. 출력은 별도 파일.
GPU: **CUDA_VISIBLE_DEVICES=1 로 실행** (BIOP01 전용 cuda:1; MoFlow는 device 지정 시 devices="-1"
     = 보이는 GPU 전부를 잡으므로, 물리 GPU1만 보이게 하는 것이 격리·충돌방지에 필수).

실행:
  CUDA_VISIBLE_DEVICES=1 PYTHONPATH=<repo>/vendor/MoFlow/src \
    conda run --no-capture-output -n velo-torch python -u scripts/p2_moflow_scrambled.py --gpu
출력: results/moflow_scrambled_genes.csv, data/velocity/moflow_scrambled.h5ad, runtime.csv(append)
"""
from __future__ import annotations
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import sys
import numpy as np
import scipy.sparse as sp
import scanpy as sc
import pandas as pd
import p2_config as cfg
from p2_util import timer, peak_mem_mb, log_runtime

# apples-to-apples: MultiVelo 음성대조와 동일 셔플 + dl_prep과 동일 smoothing
from p2_multivelo_scrambled import scramble_within_lineage
from p2_dl_prep import smooth_chrom

from MoFlow.moflow import MOFlow            # PYTHONPATH=vendor/MoFlow/src
from MoFlow.eval_dtw import get_dtw

METHOD = "moflow_scrambled"


def main(n_genes=0, gpu=False, n_jobs=None):
    cfg.OUT_VELO.mkdir(parents=True, exist_ok=True); cfg.RESULTS.mkdir(parents=True, exist_ok=True)
    n_jobs = n_jobs or cfg.MV_NJOBS
    tag = ".smoke" if n_genes else ""

    rna = sc.read_h5ad(cfg.OUT_VELO / "dl_input_rna.h5ad")
    atac = sc.read_h5ad(cfg.OUT_VELO / "dl_input_atac.h5ad")
    if "lineage" not in rna.obs.columns:
        print("✗ lineage 라벨 없음 — scramble 불가"); return 1
    if "connectivities" not in rna.obsp:
        print("✗ rna.obsp['connectivities'] 없음 — smoothing 불가"); return 1
    if n_genes:
        g = list(rna.var_names[:n_genes]); rna = rna[:, g].copy(); atac = atac[:, g].copy()
    print(f"MoFlow-scrambled: {rna.n_vars} genes, {rna.n_obs} cells, gpu={gpu}", flush=True)

    # ── 음성대조 핵심 ─────────────────────────────────────────────────────────
    # 1) raw ATAC(X) 만 남긴 fresh AnnData 로 within-lineage 셔플 (Mc 재계산할 것이므로 제외)
    atac_raw = sc.AnnData(
        X=atac.X.copy(),
        obs=atac.obs.copy(),
        var=atac.var.copy(),
    )
    atac_raw.obs_names = atac.obs_names
    atac_raw.var_names = atac.var_names
    # 2) MultiVelo 음성대조와 동일 함수·동일 seed 로 raw ATAC 행 셔플
    scrambled = scramble_within_lineage(atac_raw, rna.obs["lineage"].values, cfg.RANDOM_SEED)
    # 3) dl_prep 과 동일 smoothing(knn_smooth_chrom 등가) 으로 재smooth → Mc
    scrambled = smooth_chrom(scrambled, rna.obsp["connectivities"])
    # sanity: 원본 Mc 와 셔플 Mc 는 달라야 하고, marginal(gene별 총합)은 근사 보존
    Mc0 = atac.layers["Mc"]; Mc1 = scrambled.layers["Mc"]
    Mc0d = Mc0.toarray() if sp.issparse(Mc0) else np.asarray(Mc0)
    Mc1d = Mc1.toarray() if sp.issparse(Mc1) else np.asarray(Mc1)
    print(f"  Mc identical? {np.allclose(Mc0d, Mc1d)} | "
          f"per-gene mean 상관(원본 vs 셔플)={np.corrcoef(Mc0d.mean(0), Mc1d.mean(0))[0,1]:.4f}",
          flush=True)
    # ─────────────────────────────────────────────────────────────────────────

    import scvelo as scv
    with timer() as t:
        m = MOFlow(rna, scrambled, embed="X_umap",
                   device=("cuda" if gpu else None))
        result = m.velocity(rna, n_jobs=n_jobs,
                            save_path=str(cfg.OUT_VELO / f"moflow_scrambled{tag}_out"))
        pt_ok = True
        try:
            scv.tl.velocity_graph(result, vkey="velo_s")
            scv.tl.velocity_pseudotime(result, vkey="velo_s")
        except Exception as e:
            pt_ok = False
            print(f"  ⚠ pseudotime 계산 실패: {str(e)[:60]} → c-s lag 생략", flush=True)
    print(f"학습 done in {t.sec}s", flush=True)

    # gene별 c-s lag(time_lag_c_s) + chromatin 채널 fit-quality 요약
    def _dense(x):
        return x.toarray() if sp.issparse(x) else np.asarray(x)
    alpha_c = _dense(result.layers["alpha_c"]) if "alpha_c" in result.layers else None
    velo_c = _dense(result.layers["velo_c"]) if "velo_c" in result.layers else None
    var_loss = result.var["loss"] if "loss" in result.var.columns else None

    rows = {}
    for gi, gene in enumerate(result.var_names):
        d = {}
        try:
            if not pt_ok:
                raise RuntimeError("pseudotime 없음")
            *_, time_lag_c_s, _ = get_dtw(result, gene)
            arr = np.asarray(time_lag_c_s, float)
            d["cs_lag_mean"] = np.nanmean(arr); d["cs_lag_median"] = np.nanmedian(arr)
        except Exception as e:
            d["cs_lag_mean"] = np.nan; d["cs_lag_median"] = np.nan; d["err"] = str(e)[:40]
        if alpha_c is not None:
            d["alpha_c_mean_abs"] = float(np.nanmean(np.abs(alpha_c[:, gi])))
        if velo_c is not None:
            d["velo_c_mean_abs"] = float(np.nanmean(np.abs(velo_c[:, gi])))
        if var_loss is not None:
            d["loss"] = float(var_loss.iloc[gi])
        rows[gene] = d

    genes = pd.DataFrame(rows).T; genes.index.name = "gene"
    out_csv = cfg.RESULTS / f"moflow_scrambled_genes{tag}.csv"; genes.to_csv(out_csv)
    n_ok = int(genes["cs_lag_median"].notna().sum())
    print(f"✓ scrambled c-s lag {genes.shape}, 산출 gene {n_ok} → {out_csv.name}", flush=True)

    result.write_h5ad(cfg.OUT_VELO / f"moflow_scrambled{tag}.h5ad")
    log_runtime(cfg.RUNTIME_CSV, method=METHOD, arm="scrambled_chromatin_null",
                n_cells=result.n_obs, n_genes=result.n_vars, wall_sec=t.sec, peak_mb=peak_mem_mb(),
                note=f"within-lineage ATAC shuffle→resmooth; DTW c-s lag; gpu={gpu}; smoke n={n_genes}"
                     if n_genes else f"within-lineage ATAC shuffle→resmooth; DTW c-s lag; gpu={gpu}")
    print("다음: results/scrambled_null_moflow.md — 원본 moflow lag/fit-quality 대비 검정", flush=True)
    return 0


if __name__ == "__main__":
    n = int(sys.argv[sys.argv.index("--genes") + 1]) if "--genes" in sys.argv else 0
    nj = int(sys.argv[sys.argv.index("--n-jobs") + 1]) if "--n-jobs" in sys.argv else None
    sys.exit(main(n_genes=n, gpu=("--gpu" in sys.argv), n_jobs=nj))
