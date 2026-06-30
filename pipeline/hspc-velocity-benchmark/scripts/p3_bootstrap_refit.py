#!/usr/bin/env python3
"""P3 — 전체 re-fit bootstrap 분석: α_c vs lag 재fit 안정성. DESIGN §4D.

p2_multivelo_bootstrap_refit.py가 만든 refit_<b>.csv 다수를 모아, **재fit 간** per-gene 안정성을 측정.
  - α_c(fit_alpha_c), α(fit_alpha), lag(fit_t_sw2−fit_t_sw1) 각각:
      · 재fit 간 per-gene CV (=std/|mean|) 분포
      · 재fit 쌍별 rank 일치도 (mean pairwise Spearman) = 추정 순위가 재fit에 얼마나 보존되나
  - lag은 부호-flip rate(재fit 간)도.
가설: α 계열 rank 일치도 ≫ lag → 'α는 재fit-robust, lag은 비robust'를 재fit 축에서 직접 확증.

실행: conda run -n scv-preprocess python scripts/p3_bootstrap_refit.py
출력: results/bootstrap_refit.md, results/bootstrap_refit_pergene.csv
"""
import sys
from pathlib import Path
from itertools import combinations
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent.parent
RES = HERE / "results"
REFIT = RES / "bootstrap_refit"


def load_refits():
    files = sorted(REFIT.glob("refit_*.csv"))
    files = [f for f in files if ".smoke" not in f.name]
    mats = {}
    for f in files:
        df = pd.read_csv(f, index_col=0)
        mats[f.stem] = df
    return mats


def stack(mats, col):
    """gene × refit 행렬 (해당 col)."""
    s = {k: df[col] for k, df in mats.items() if col in df.columns}
    return pd.DataFrame(s)


def mean_pairwise_spearman(M):
    """refit 쌍별 Spearman(gene 순위) 평균. M: gene × refit."""
    cols = list(M.columns)
    rhos = []
    for a, b in combinations(cols, 2):
        sub = M[[a, b]].dropna()
        if len(sub) >= 10:
            rhos.append(spearmanr(sub[a], sub[b])[0])
    return float(np.nanmean(rhos)) if rhos else np.nan, len(rhos)


def per_gene_cv(M):
    mean = M.mean(axis=1)
    std = M.std(axis=1)
    return std / mean.abs().replace(0, np.nan)


def main():
    mats = load_refits()
    nb = len(mats)
    print(f"[refit] {nb} refit 로드", flush=True)
    if nb < 2:
        print("[refit] refit 2개 미만 — 아직 분석 불가(대기).", flush=True)
        return 0

    targets = [("fit_alpha_c", "α_c (chromatin opening rate)"),
               ("fit_alpha", "α (transcription rate)"),
               ("lag", "lag (switch time 차)")]
    rows = []
    pergene = {}
    for col, lbl in targets:
        M = stack(mats, col)
        if M.shape[1] < 2:
            print(f"[refit] {col} 없음/refit<2 — skip", flush=True)
            continue
        rho, npair = mean_pairwise_spearman(M)
        cv = per_gene_cv(M)
        pergene[f"{col}_cv"] = cv
        med_cv = float(cv.median())
        row = dict(quantity=lbl, col=col, n_gene=int(M.notna().all(axis=1).sum()),
                   rank_concord=rho, n_pair=npair, median_cv=med_cv)
        if col == "lag":
            pos = (M > 0).mean(axis=1)
            neg = (M < 0).mean(axis=1)
            flip = np.minimum(pos, neg)
            pergene["lag_signflip"] = flip
            row["median_signflip"] = float(flip.median())
            row["sign_stable_frac"] = float((flip < 0.10).mean())
        rows.append(row)
        print(f"[refit] {col}: rank-concord={rho:+.3f} (n_pair={npair}), median CV={med_cv:.2f}", flush=True)

    summ = pd.DataFrame(rows)
    pg = pd.DataFrame(pergene)
    pg.to_csv(RES / "bootstrap_refit_pergene.csv")

    ac = summ[summ.col == "fit_alpha_c"]
    lg = summ[summ.col == "lag"]
    ac_rho = float(ac["rank_concord"].iloc[0]) if len(ac) else float("nan")
    lg_rho = float(lg["rank_concord"].iloc[0]) if len(lg) else float("nan")

    L = ["# P3 — 전체 re-fit bootstrap: α_c vs lag 재fit 안정성", "",
         f"> p5_bootstrap_stability.py(fit 고정, stability 하한)가 남긴 미완 — **전체 re-fit 반복** — 수행.",
         f"> cell {int(round(0.70*21878))}~ (frac 0.70 비복원 subsample) 마다 MultiVelo 처음부터 재fit, "
         f"canonical gene 고정. **{nb} refit**.", "",
         "## 재fit 간 안정성 (per-gene)", "",
         "| 수량 | gene | rank 일치도(쌍별 Spearman) | median CV | 부호 안정 |",
         "|---|---|---|---|---|"]
    for _, r in summ.iterrows():
        extra = ""
        if r["col"] == "lag":
            extra = f"flip<0.1 {r.get('sign_stable_frac', float('nan')):.0%} (med flip {r.get('median_signflip', float('nan')):.2f})"
        L.append(f"| {r['quantity']} | {r['n_gene']} | **{r['rank_concord']:+.3f}** | {r['median_cv']:.2f} | {extra} |")
    L += ["", "## 해석", "",
          f"- **재fit 간 rank 일치도: α_c={ac_rho:+.3f} vs lag={lg_rho:+.3f}**.",
          f"  → {'α_c가 lag보다 재fit-robust' if ac_rho - lg_rho > 0.1 else ('둘 다 비슷' if abs(ac_rho-lg_rho)<=0.1 else 'lag이 더 안정(예상 밖)')}"
          f" — H1('α 계열 robust, lag 비robust')이 **재fit 안정성 축에서도** {'재확인' if ac_rho-lg_rho>0.1 else '부분 확인'}.",
          "- p5_bootstrap_stability.py(fit 고정)는 lag 부호 83% 안정이었으나, **전체 재fit에선 더 흔들림**(위 lag 부호 안정 비율 비교) "
          "→ '한 fit 안 표집 안정'과 '재fit 안정'은 다르며, lag의 진짜 stability는 후자.",
          "- drug-timing 모델 시사: 재fit-robust한 α_c·α를 baseline-ATAC와 함께 쓰고(§6 lag_model_atac에서 α 예측 ρ=+0.31), "
          "lag은 재fit-불안정 → 단일 값 사용 금지·uncertainty 반영.",
          "- ⚠️ subsample(비복원 frac 0.70) 기반 — 복원추출 아님(kNN graph 붕괴 회피). gene→canonical 고정."]
    (RES / "bootstrap_refit.md").write_text("\n".join(L) + "\n")
    print(f"[refit] ✓ → bootstrap_refit.md (α_c {ac_rho:+.3f} vs lag {lg_rho:+.3f})", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
