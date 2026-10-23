#!/usr/bin/env python3
"""P5 — ATAC 셔플·MultiVelo 재적합 안정성을 priming 정의(t_sw1)로 다시 계산한다.

ML4H Submission 294 반박문(2026-10-13)에서 MultiVelo lag의 주 정의를 coupled-on 길이
(fit_t_sw2 − fit_t_sw1)에서 priming interval(fit_t_sw1)로 바꿨다(p17 R5). 그때 coupled-on
정의로만 남아 있던 두 수치를 같은 입력으로 priming 정의에서 다시 낸다.

  S  ATAC within-lineage 셔플 (p3_scrambled_null.py 와 같은 입력·같은 통계)
     results/multivelo_genes.csv vs results/scrambled_genes.csv
  B  MultiVelo 재적합 안정성 (p3_bootstrap_refit.py 와 같은 정의)
     results/bootstrap_refit/refit_*.csv  (gitignore — HPC에만 있으면 이 절은 건너뛴다)

계약 검사: coupled-on 정의로 다시 낸 값이 기존 보고값(셔플 ρ 0.721, MW p 0.196, KS p 0.507,
재적합 lag +0.624)과 다르면 멈춘다. 입력이 바뀌지 않았음을 보장하기 위해서다.

실행: ~/miniforge3/envs/scv-preprocess/bin/python scripts/p18_priming_recompute.py [--refit-dir DIR]
출력: results/priming_recompute.gen.md, results/priming_recompute.csv
"""
from __future__ import annotations

import argparse
import itertools
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

HERE = Path(__file__).resolve().parent.parent
RES = HERE / "results"
B = 10000
SEED = 20261023

LAGS = {
    "coupled_on": lambda d: d["fit_t_sw2"] - d["fit_t_sw1"],
    "priming": lambda d: d["fit_t_sw1"],
}


def load(name):
    d = pd.read_csv(RES / name, index_col=0) if not isinstance(name, Path) else pd.read_csv(name, index_col=0)
    if "fit_likelihood" in d.columns:
        d = d[d["fit_likelihood"].notna()]
    return d[~d.index.duplicated()]


def boot_spearman(a, b, rng, b_n=B):
    a, b = np.asarray(a), np.asarray(b)
    n = len(a)
    ra, rb = stats.rankdata(a), stats.rankdata(b)
    pt = float(np.corrcoef(ra, rb)[0, 1])
    draws = np.empty(b_n)
    for i in range(b_n):
        idx = rng.integers(0, n, n)
        draws[i] = np.corrcoef(stats.rankdata(a[idx]), stats.rankdata(b[idx]))[0, 1]
    lo, hi = np.nanpercentile(draws, [2.5, 97.5])
    return pt, float(lo), float(hi)


def shuffle_block(rng, rows, L):
    o, s = load("multivelo_genes.csv"), load("scrambled_genes.csv")
    sh = o.index.intersection(s.index)
    o, s = o.loc[sh], s.loc[sh]
    L += ["## S. ATAC within-lineage 셔플: 원본 vs 셔플 재적합", "",
          f"> 입력: results/multivelo_genes.csv, results/scrambled_genes.csv (공통 유전자 n={len(sh)}). "
          f"ρ의 95% CI는 유전자 bootstrap {B:,}회.", "",
          "| 정의 | n | per-gene Spearman ρ [95% CI] | MW p | KS p | Wilcoxon p | median 원본 → 셔플 | 상대변화 median | 0인 유전자(원본/셔플) |",
          "|---|---|---|---|---|---|---|---|---|"]
    out = {}
    for name, f in LAGS.items():
        p = pd.DataFrame({"orig": f(o), "scram": f(s)}).dropna()
        rho, lo, hi = boot_spearman(p.orig.values, p.scram.values, rng)
        mw = stats.mannwhitneyu(p.orig, p.scram, alternative="two-sided").pvalue
        ks = stats.ks_2samp(p.orig, p.scram).pvalue
        wil = stats.wilcoxon(p.orig, p.scram).pvalue
        rel = float((np.abs(p.scram - p.orig) / p.orig.abs().clip(1e-6)).median())
        z = (int((p.orig == 0).sum()), int((p.scram == 0).sum()))
        out[name] = dict(rho=rho, mw=mw, ks=ks)
        L.append(f"| {name} | {len(p)} | {rho:+.3f} [{lo:+.3f}, {hi:+.3f}] | {mw:.3f} | {ks:.3f} | {wil:.2g} | "
                 f"{p.orig.median():.3f} → {p.scram.median():.3f} | {rel:.1%} | {z[0]}/{z[1]} |")
        rows.append(dict(block="shuffle", definition=name, n=len(p), rho=rho, ci_lo=lo, ci_hi=hi,
                         mw_p=mw, ks_p=ks, wilcoxon_p=wil, rel_change_median=rel))
    c = out["coupled_on"]
    assert abs(c["rho"] - 0.721) < 5e-4 and abs(c["mw"] - 0.196) < 5e-4 and abs(c["ks"] - 0.507) < 5e-4, c
    L += ["", "계약 검사 통과: coupled-on 정의 값이 scrambled_null.md(ρ 0.721, MW p 0.196, KS p 0.507)와 같다.", ""]


def refit_block(refit_dir: Path | None, rows, L):
    L += ["## B. MultiVelo 재적합 안정성 (12 × 70% 부분표본)", ""]
    files = sorted(refit_dir.glob("refit_*.csv")) if refit_dir and refit_dir.is_dir() else []
    files = [f for f in files if "shuf" not in f.name]
    if not files:
        L += [f"재적합 표가 없어 건너뛰었다(찾은 위치: `{refit_dir}`). 이 표는 `.gitignore` 대상이라 "
              "HPC의 `results/bootstrap_refit/`에만 있다. 그곳에서 `--refit-dir`를 주고 다시 실행한다.", ""]
        return
    tabs = [load(f) for f in files]
    common = sorted(set.intersection(*[set(t.index) for t in tabs]))
    L += [f"> 재적합 {len(tabs)}회, 공통 유전자 n={len(common)}. 평균 pairwise Spearman과 유전자별 CV의 median.", "",
          "| 값 | mean pairwise ρ | median CV |", "|---|---|---|"]
    res = {}
    defs = {"alpha": lambda d: d["fit_alpha"], "alpha_c": lambda d: d["fit_alpha_c"], **LAGS}
    for name, f in defs.items():
        M = np.column_stack([f(t.loc[common]).values for t in tabs])
        rhos = [stats.spearmanr(M[:, i], M[:, j]).statistic for i, j in itertools.combinations(range(M.shape[1]), 2)]
        cv = np.nanmedian(np.nanstd(M, axis=1, ddof=1) / np.abs(np.nanmean(M, axis=1)).clip(1e-9))
        res[name] = float(np.mean(rhos))
        L.append(f"| {name} | {np.mean(rhos):+.3f} | {cv:.2f} |")
        rows.append(dict(block="refit", definition=name, n=len(common), rho=float(np.mean(rhos)), cv_median=float(cv)))
    assert abs(res["coupled_on"] - 0.624) < 5e-4 and abs(res["alpha"] - 0.949) < 5e-4, res
    L += ["", "계약 검사 통과: coupled-on +0.624, α +0.949가 bootstrap_refit.md와 같다.", ""]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refit-dir", type=Path, default=RES / "bootstrap_refit")
    args = ap.parse_args()
    rng = np.random.default_rng(SEED)
    rows, L = [], ["# priming 정의(t_sw1) 재계산: ATAC 셔플·MultiVelo 재적합 (machine output, do not edit)", "",
                   f"> scripts/p18_priming_recompute.py. B={B:,}, seed={SEED}. 기존 입력 파일만 사용, 재적합 없음.", ""]
    shuffle_block(rng, rows, L)
    refit_block(args.refit_dir, rows, L)
    (RES / "priming_recompute.gen.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    pd.DataFrame(rows).to_csv(RES / "priming_recompute.csv", index=False)
    print("\n".join(L))


if __name__ == "__main__":
    main()
