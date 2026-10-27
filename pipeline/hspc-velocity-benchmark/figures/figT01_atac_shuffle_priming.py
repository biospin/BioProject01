"""GIW 2026 talk figure — within-lineage ATAC shuffle, MultiVelo priming interval (t_sw1).

Slide-sized replot of the S block of results/priming_recompute.gen.md (scripts/p18_priming_recompute.py).
Same inputs and gene set: results/multivelo_genes.csv vs results/scrambled_genes.csv, genes with a
fit_likelihood in both files. Hard gate: point estimates recomputed here must match the gen.md table
(rho, MW p, KS p, medians) or the script exits without saving.

Output: figures/figT01_atac_shuffle_priming.png (png is gitignored; the script is the record).
"""
from pathlib import Path
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
import pandas as pd
from scipy import stats

HERE = Path(__file__).resolve().parent
RES = HERE.parent / "results"
OUT = HERE / "figT01_atac_shuffle_priming.png"

for f in font_manager.findSystemFonts():
    if "Pretendard" in Path(f).name:
        font_manager.fontManager.addfont(f)
if any("Pretendard" in f.name for f in font_manager.fontManager.ttflist):
    plt.rcParams["font.family"] = "Pretendard"
plt.rcParams.update({"font.size": 17, "axes.spines.top": False, "axes.spines.right": False})

ORIG_C, SHUF_C = "#2457C5", "#9AA5B4"


def load(name):
    d = pd.read_csv(RES / name, index_col=0)
    return d[d["fit_likelihood"].notna()] if "fit_likelihood" in d.columns else d


def expected():
    """Parse the priming row of the S table in priming_recompute.gen.md."""
    txt = (RES / "priming_recompute.gen.md").read_text(encoding="utf-8")
    row = next(l for l in txt.splitlines() if l.startswith("| priming |"))
    c = [x.strip() for x in row.strip("|").split("|")]
    rho, lo, hi = map(float, re.findall(r"[+-]?\d+\.\d+", c[2]))
    med = list(map(float, re.findall(r"\d+\.\d+", c[6])))
    return dict(n=int(c[1]), rho=rho, lo=lo, hi=hi, mw=float(c[3]), ks=float(c[4]), med_o=med[0], med_s=med[1])


def main():
    o, s = load("multivelo_genes.csv"), load("scrambled_genes.csv")
    sh = o.index.intersection(s.index)
    p = pd.DataFrame({"orig": o.loc[sh, "fit_t_sw1"], "scram": s.loc[sh, "fit_t_sw1"]}).dropna()
    got = dict(n=len(p), rho=stats.spearmanr(p.orig, p.scram)[0],
               mw=stats.mannwhitneyu(p.orig, p.scram, alternative="two-sided").pvalue,
               ks=stats.ks_2samp(p.orig, p.scram).pvalue,
               med_o=p.orig.median(), med_s=p.scram.median())
    exp = expected()
    checks = [("n", got["n"] == exp["n"]), ("rho", round(got["rho"], 3) == exp["rho"]),
              ("mw", round(got["mw"], 3) == exp["mw"]), ("ks", round(got["ks"], 3) == exp["ks"]),
              ("med_o", round(got["med_o"], 3) == exp["med_o"]), ("med_s", round(got["med_s"], 3) == exp["med_s"])]
    bad = [k for k, ok in checks if not ok]
    if bad:
        sys.exit(f"[gate] mismatch with priming_recompute.gen.md: {bad} got={got} expected={exp}")

    fig, (a, b) = plt.subplots(1, 2, figsize=(13.0, 5.4), gridspec_kw={"width_ratios": [1.15, 1]})
    hi = float(np.nanmax(np.r_[p.orig, p.scram])) * 1.02
    bins = np.linspace(0, hi, 40)
    a.hist(p.orig, bins=bins, color=ORIG_C, alpha=0.75, label=f"Observed ATAC (median {exp['med_o']:.2f})")
    a.hist(p.scram, bins=bins, histtype="step", lw=2.6, color="#4A5566",
           label=f"ATAC shuffled within lineage (median {exp['med_s']:.2f})")
    a.set_xlabel("Priming interval per gene (pseudotime units)")
    a.set_ylabel("Genes")
    a.set_title(f"A  Distribution: Mann–Whitney p = {exp['mw']:.2f}, KS p = {exp['ks']:.2f}", loc="left", fontsize=17)
    a.legend(frameon=False, fontsize=14.5, loc="upper right")

    b.scatter(p.orig, p.scram, s=14, alpha=0.45, color=ORIG_C, edgecolor="none")
    lim = [0, hi]
    b.plot(lim, lim, color="#4A5566", lw=1.4, ls="--")
    b.set_xlim(lim); b.set_ylim(lim)
    b.set_xlabel("Observed ATAC")
    b.set_ylabel("Shuffled ATAC")
    b.set_title(f"B  Per gene: Spearman ρ = {exp['rho']:.3f} [{exp['lo']:.3f}, {exp['hi']:.3f}]",
                loc="left", fontsize=17)
    b.text(0.97, 0.04, f"n = {exp['n']} genes", transform=b.transAxes, ha="right", fontsize=15, color="#4A5566")
    fig.tight_layout()
    fig.savefig(OUT, dpi=220)
    print(f"saved {OUT}  (gate passed: {', '.join(k for k, _ in checks)})")


if __name__ == "__main__":
    main()
