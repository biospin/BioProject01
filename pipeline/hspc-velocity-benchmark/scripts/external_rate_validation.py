#!/usr/bin/env python
"""External construct-validation of fitted kinetic rates vs experimentally measured rates.

PART A: fitted gamma (degradation) vs measured mRNA half-life t_half (hours).
  Relationship: t_half = ln2 / gamma_true  ->  Spearman(gamma, t_half) expected NEGATIVE
  (high gamma = fast decay = short t_half). We ALSO report Spearman(gamma, k_deg) with
  k_deg = ln2/t_half, which by rank equals -Spearman(gamma, t_half) and reads POSITIVE when
  gamma recovers measured decay (so the "recovers" direction matches Part B's positive framing).

  Verdict rule (per method x cell-line): a method's gamma RECOVERS measured decay iff its
  bootstrap 95% CI on rho(gamma, k_deg) excludes 0 on the POSITIVE side
  (equivalently rho(gamma, t_half) CI entirely < 0).

Rank-based only (absolute rates not identifiable / cross-context). Every rho ships a
paired-gene percentile bootstrap 95% CI (B=10000). HK vs non-HK stratified; headline = non-HK.
"""
import numpy as np, pandas as pd
from scipy import stats
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"
DATA = ROOT / "data"
RNG = np.random.default_rng(20260707)
B = 10000

# fitted gamma per method (HSPC)
METHODS = {
    "rna_only":     (RES / "rna_only_dynamical_genes.csv", "fit_gamma"),
    "multivelo":    (RES / "multivelo_genes.csv",          "fit_gamma"),
    "multivelovae": (RES / "multivelovae_genes.csv",       "vae_gamma"),
}
# measured half-life panels (gene, t_half_h in hours)
CELLLINES = {
    "K562_todorovski":  DATA / "todorovski_k562_halflife.csv",   # same-study SLAM-seq, 24h cap
    "THP1_todorovski":  DATA / "halflife_thp1.csv",              # same-study SLAM-seq, 24h cap
    "MOLM13_rnadecay":  DATA / "halflife_molm13.csv",            # cross-study, EZbakR (cleanest, likely uncensored)
}

HK = set(l.strip() for l in (DATA / "housekeeping.txt").read_text().splitlines() if l.strip())


def load_gamma(path, col):
    df = pd.read_csv(path)
    s = df.set_index("gene")[col].dropna()
    s = s[s > 0]  # gamma must be positive; degenerate/zero fits dropped
    return s[~s.index.duplicated()]


def load_thalf(path):
    df = pd.read_csv(path)
    s = df.set_index("gene")["t_half_h"].dropna()
    s = s[s > 0]
    return s.groupby(level=0).median()


def boot_ci_rho(x, y, b=B):
    """paired-gene percentile bootstrap 95% CI for Spearman rho(x, y)."""
    n = len(x)
    rho0 = stats.spearmanr(x, y).statistic
    rhos = np.empty(b)
    idx = np.arange(n)
    for i in range(b):
        s = RNG.choice(idx, n, replace=True)
        rhos[i] = stats.spearmanr(x[s], y[s]).statistic
    lo, hi = np.nanpercentile(rhos, [2.5, 97.5])
    return float(rho0), float(lo), float(hi)


def run_cell(gamma, thalf, censor_frac, subset_idx=None, tag=""):
    g = gamma.copy(); t = thalf.copy()
    common = g.index.intersection(t.index)
    if subset_idx is not None:
        common = common.intersection(subset_idx)
    g = g.loc[common].values.astype(float)
    t = t.loc[common].values.astype(float)
    kdeg = np.log(2) / t  # measured degradation rate; rank-equivalent to -t_half
    rho_t, lo_t, hi_t = boot_ci_rho(g, t)      # expected NEGATIVE if recovering
    # rho(gamma, kdeg) == -rho(gamma, t) exactly under rank; recompute for reporting w/ its own CI
    rho_k, lo_k, hi_k = boot_ci_rho(g, kdeg)   # expected POSITIVE if recovering
    p_t = stats.spearmanr(g, t).pvalue
    # verdict: CI on rho(gamma, kdeg) excludes 0 on positive side
    recovers = lo_k > 0
    return dict(tag=tag, n=int(len(common)), censor_frac=censor_frac,
                rho_gamma_thalf=round(rho_t, 3), ci_thalf=[round(lo_t, 3), round(hi_t, 3)],
                rho_gamma_kdeg=round(rho_k, 3), ci_kdeg=[round(lo_k, 3), round(hi_k, 3)],
                p_thalf=float(p_t), recovers=bool(recovers))


results = {}
summary_rows = []
for cname, cpath in CELLLINES.items():
    thalf = load_thalf(cpath)
    cap = thalf.max()
    censor_frac = float((thalf >= cap - 1e-6).mean())
    uncensored_idx = thalf[thalf < cap - 1e-6].index
    for mname, (mpath, mcol) in METHODS.items():
        gamma = load_gamma(mpath, mcol)
        # ALL genes (primary)
        r_all = run_cell(gamma, thalf, censor_frac, tag="all")
        # non-HK (headline)
        nonhk = gamma.index.difference(HK)
        r_nonhk = run_cell(gamma, thalf, censor_frac, subset_idx=nonhk, tag="non_HK")
        # HK
        r_hk = run_cell(gamma, thalf, censor_frac, subset_idx=set(HK), tag="HK")
        # sensitivity: drop censored (t_half at cap)
        r_uncens = run_cell(gamma, thalf, censor_frac, subset_idx=uncensored_idx, tag="uncensored")
        key = f"{mname}__{cname}"
        results[key] = dict(all=r_all, non_HK=r_nonhk, HK=r_hk, uncensored=r_uncens)
        for r in (r_all, r_nonhk, r_hk, r_uncens):
            summary_rows.append(dict(method=mname, cellline=cname, stratum=r["tag"],
                                     n=r["n"], censor_frac=round(censor_frac, 4),
                                     rho_gamma_thalf=r["rho_gamma_thalf"],
                                     ci_thalf_lo=r["ci_thalf"][0], ci_thalf_hi=r["ci_thalf"][1],
                                     rho_gamma_kdeg=r["rho_gamma_kdeg"],
                                     ci_kdeg_lo=r["ci_kdeg"][0], ci_kdeg_hi=r["ci_kdeg"][1],
                                     p_thalf=r["p_thalf"], recovers=r["recovers"]))

df = pd.DataFrame(summary_rows)
df.to_csv(RES / "external_rate_validation_gamma.csv", index=False)
(RES / "external_rate_validation_gamma.json").write_text(json.dumps(results, indent=2))
print(df.to_string(index=False))
print("\nWrote:", RES / "external_rate_validation_gamma.csv")
