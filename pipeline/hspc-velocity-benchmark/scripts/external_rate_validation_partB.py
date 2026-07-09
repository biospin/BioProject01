#!/usr/bin/env python
"""PART B: fitted alpha (transcription rate) vs measured TT-seq synthesis/production rate.

Source: GSE229305 (Todorovski 2024, NAR Cancer subseries "TTseq K562 production rates"),
file GSE229305_K562_TTseq_synthesis_measurements_rates.txt.gz, treatment=UT (untreated baseline).
-> per-gene K562 synthesis rate (synth_rate). Only K562 has a TT-seq production-rate subseries
(THP1 subseries are SLAM-seq decay only) -> Part B is K562-only.

Biophysical analog: scVelo/MultiVelo alpha == TT-seq production rate. Expect POSITIVE rank corr
if fitted alpha captures a gene-intrinsic synthesis ordering that generalizes across context.

Pre-registered ASYMMETRIC interpretation: positive rho validates alpha as a real synthesis-rate
proxy; a null does NOT prove alpha wrong (cross-context K562 leukemia != dynamic HSPC; absolute
alpha not identifiable -> rank only). K562 ~ erythroid/MK output lineages of HSPC.
Rank-based; paired-gene percentile bootstrap 95% CI (B=10000). HK vs non-HK; headline non-HK.
"""
import numpy as np, pandas as pd
from scipy import stats
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"; DATA = ROOT / "data"
RNG = np.random.default_rng(20260707); B = 10000

METHODS = {
    "rna_only":     (RES / "rna_only_dynamical_genes.csv", "fit_alpha"),
    "multivelo":    (RES / "multivelo_genes.csv",          "fit_alpha"),
    "multivelovae": (RES / "multivelovae_genes.csv",       "vae_alpha"),
}
HK = set(l.strip() for l in (DATA / "housekeeping.txt").read_text().splitlines() if l.strip())


def load_alpha(path, col):
    df = pd.read_csv(path)
    s = df.set_index("gene")[col].dropna()
    s = s[s > 0]
    return s[~s.index.duplicated()]


def load_synth():
    df = pd.read_csv(DATA / "k562_ttseq_synthrate.csv")
    s = df.set_index("gene")["synth_rate"].dropna()
    s = s[s > 0]
    return s.groupby(level=0).median()


def boot_ci_rho(x, y, b=B):
    n = len(x); rho0 = stats.spearmanr(x, y).statistic
    rhos = np.empty(b); idx = np.arange(n)
    for i in range(b):
        s = RNG.choice(idx, n, replace=True)
        rhos[i] = stats.spearmanr(x[s], y[s]).statistic
    lo, hi = np.nanpercentile(rhos, [2.5, 97.5])
    return float(rho0), float(lo), float(hi)


def run(alpha, synth, subset=None, tag=""):
    common = alpha.index.intersection(synth.index)
    if subset is not None:
        common = common.intersection(subset)
    a = alpha.loc[common].values.astype(float)
    s = synth.loc[common].values.astype(float)
    rho, lo, hi = boot_ci_rho(a, s)
    p = stats.spearmanr(a, s).pvalue
    return dict(tag=tag, n=int(len(common)), rho_alpha_synth=round(rho, 3),
                ci=[round(lo, 3), round(hi, 3)], p=float(p), validates=bool(lo > 0))


synth = load_synth()
results = {}; rows = []
for mname, (mpath, mcol) in METHODS.items():
    alpha = load_alpha(mpath, mcol)
    r_all = run(alpha, synth, tag="all")
    r_nonhk = run(alpha, synth, subset=alpha.index.difference(HK), tag="non_HK")
    r_hk = run(alpha, synth, subset=set(HK), tag="HK")
    results[mname] = dict(all=r_all, non_HK=r_nonhk, HK=r_hk)
    for r in (r_all, r_nonhk, r_hk):
        rows.append(dict(method=mname, cellline="K562_TTseq", stratum=r["tag"], n=r["n"],
                         rho_alpha_synth=r["rho_alpha_synth"], ci_lo=r["ci"][0], ci_hi=r["ci"][1],
                         p=r["p"], validates=r["validates"]))

df = pd.DataFrame(rows)
df.to_csv(RES / "external_rate_validation_alpha.csv", index=False)
(RES / "external_rate_validation_alpha.json").write_text(json.dumps(results, indent=2))
print(df.to_string(index=False))
print("\nWrote:", RES / "external_rate_validation_alpha.csv")
