#!/usr/bin/env python3
"""p2_crakvelo_lag.py — CRAK-Velo fit 산출에서 gene별 DTW c-s lag 추출.

MoFlow get_dtw는 MoFlow 전용 구조라 재사용 불가 → CRAK-Velo 출력에 **동일 정신**의
chromatin→spliced DTW lag을 적용한다(apples-to-apples는 아니고 '동형 정의').

입력(크레이크-벨로 fit save_dir):
  adata_rna_fit.h5ad   : layers['Ms'](spliced moments), obs['latent_time'], var['velocity_genes']
  adata_atac_fit.h5ad  : obsm['cisTopic'] (cell × region, 사용된 region으로 subset된 smoothed accessibility)
  B.txt                : (region × gene) binary — region이 어느 velocity gene에 연결됐나

방법(gene g, velocity_genes만):
  gene chromatin = cisTopic[:, B[:,g]==1].mean(axis=1)   # cell별 gene 주변 region 접근성 평균
  cells를 latent_time 오름차순 정렬 → chromatin c(t), spliced s(t)를 N_BIN으로 평균 binning → z-정규화
  DTW(c, s) warping path에서 lag = mean(j_s − i_c)   # ★convention: 양수 = chromatin 선행(접근성 상승이 발현 상승보다 먼저)

산출: results/crakvelo_genes.csv  (gene, cs_lag_mean, cs_lag_median)  # moflow_genes.csv와 동일 스키마
      + stdout marker sanity (Myeloid AZU1/ELANE/MPO는 chromatin 선행=양수 기대 → sign 검증용)

⚠️ sign convention은 marker로 검증 후 FINDINGS canonical 반영. (이 스크립트는 staging까지만.)
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import anndata as ad

HERE = Path(__file__).resolve().parent.parent
RES = HERE / "results"
N_BIN = 100
MARKERS_POS = ["AZU1", "ELANE", "MPO", "LYZ", "CSF1R"]   # Myeloid: MoFlow서 chromatin 선행 → 양수 기대


def find_fit_dir():
    base = HERE / "data" / "velocity" / "crakvelo_fit"
    hits = sorted(base.rglob("adata_rna_fit.h5ad"))
    if not hits:
        raise FileNotFoundError(f"adata_rna_fit.h5ad 없음 under {base}")
    return hits[-1].parent   # 가장 최근(경로 정렬상 마지막)


def zbin(x, order, nbin):
    """x를 order(정렬 인덱스)대로 재배열 후 nbin 구간 평균 → z-정규화."""
    xs = np.asarray(x, float)[order]
    idx = np.linspace(0, len(xs), nbin + 1).astype(int)
    b = np.array([np.nanmean(xs[idx[k]:idx[k + 1]]) if idx[k + 1] > idx[k] else np.nan
                  for k in range(nbin)])
    b = pd.Series(b).interpolate(limit_direction="both").to_numpy()
    sd = b.std()
    return (b - b.mean()) / sd if sd > 1e-9 else b - b.mean()


def dtw_lag(c, s):
    """DTW warping path 기반 c(chromatin) vs s(spliced) 시간차. 양수=chromatin 선행.

    ★ sign convention (2026-07-01 검증, scripts/p3_crakvelo_sign_check.py):
      이 manual DP backtrack의 path 방향이 MoFlow의 fastdtw와 **반대**라,
      naive `j − i`는 chromatin-leading 입력에 음수를 돌려줬다(검증: 합성 switch
      신호에서 fastdtw=+30 vs j−i=−72). MoFlow(eval_dtw.get_dtw)와 부호를
      통일하기 위해 `i − j`로 부호를 맞춘다 → 양수 = chromatin 선행.
    """
    n, m = len(c), len(s)
    D = np.full((n + 1, m + 1), np.inf)
    D[0, 0] = 0.0
    for i in range(1, n + 1):
        ci = c[i - 1]
        for j in range(1, m + 1):
            cost = (ci - s[j - 1]) ** 2
            D[i, j] = cost + min(D[i - 1, j], D[i, j - 1], D[i - 1, j - 1])
    # backtrack
    i, j, offs = n, m, []
    while i > 0 and j > 0:
        offs.append(i - j)            # i(chromatin idx) − j(spliced idx): 양수 = chromatin 선행 (MoFlow fastdtw와 부호 통일)
        step = np.argmin([D[i - 1, j - 1], D[i - 1, j], D[i, j - 1]])
        if step == 0:
            i, j = i - 1, j - 1
        elif step == 1:
            i -= 1
        else:
            j -= 1
    return float(np.mean(offs)), float(np.median(offs))


def main():
    fit = find_fit_dir()
    print(f"[crak-lag] fit dir: {fit}", flush=True)
    R = ad.read_h5ad(fit / "adata_rna_fit.h5ad")
    A = ad.read_h5ad(fit / "adata_atac_fit.h5ad")
    B = np.loadtxt(fit / "B.txt", delimiter=",")
    if B.ndim == 1:
        B = B.reshape(-1, R.n_vars)
    print(f"[crak-lag] R{R.shape} A{A.shape} B{B.shape}", flush=True)

    if "latent_time" not in R.obs:
        raise KeyError("obs['latent_time'] 없음 — fit 출력 확인")
    lt = np.asarray(R.obs["latent_time"], float)
    order = np.argsort(lt)

    Ms = R.layers["Ms"] if "Ms" in R.layers else (R.layers.get("spliced", R.X))
    Ms = np.asarray(Ms.todense()) if hasattr(Ms, "todense") else np.asarray(Ms)
    cisT = A.obsm["cisTopic"]
    cisT = np.asarray(cisT.todense()) if hasattr(cisT, "todense") else np.asarray(cisT)
    # gene별 연결 region 평균 접근성: (cell × region) @ (region × gene) / region수
    reg_per_gene = B.sum(axis=0)                       # gene별 연결 region 수
    gene_chrom = cisT @ B                              # (cell × gene)
    with np.errstate(invalid="ignore", divide="ignore"):
        gene_chrom = gene_chrom / np.where(reg_per_gene > 0, reg_per_gene, np.nan)

    vgenes = (np.asarray(R.var["velocity_genes"], bool)
              if "velocity_genes" in R.var else np.ones(R.n_vars, bool))
    rows = {}
    names = list(R.var_names)
    for gi, g in enumerate(names):
        if not vgenes[gi] or reg_per_gene[gi] == 0:
            continue
        c = gene_chrom[:, gi]
        s = Ms[:, gi]
        if np.nanstd(c) < 1e-9 or np.nanstd(s) < 1e-9:
            continue
        cb, sb = zbin(c, order, N_BIN), zbin(s, order, N_BIN)
        mean_l, med_l = dtw_lag(cb, sb)
        rows[g] = dict(cs_lag_mean=mean_l, cs_lag_median=med_l)

    genes = pd.DataFrame.from_dict(rows, orient="index")
    genes.index.name = "gene"
    out = RES / "crakvelo_genes.csv"
    genes.to_csv(out)
    print(f"[crak-lag] ✓ {genes.shape} → {out.name}", flush=True)
    lag = genes["cs_lag_median"]
    print(f"[crak-lag] lag median={lag.median():.3f} mean={lag.mean():.3f} "
          f"chromatin-leads(>0)={(lag>0).mean():.1%}", flush=True)
    print("[crak-lag] marker sanity (Myeloid → 양수 기대; sign 검증):", flush=True)
    for mk in MARKERS_POS:
        if mk in genes.index:
            print(f"    {mk}: cs_lag_median={genes.loc[mk,'cs_lag_median']:+.3f}", flush=True)
    print("[crak-lag] DONE", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
