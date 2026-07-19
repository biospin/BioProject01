#!/usr/bin/env python3
"""figS05 — stiffness-tertile ladder for alpha and gamma (Additional file 11, panel 5).

Question: within a parameter, across genes, does higher per-gene profile-likelihood
curvature (stiffness) predict better agreement with an external measured rate?
Genes are split into curvature tertiles and Spearman(fit rate, measured rate) is
computed inside each tertile, with bootstrap 95% CI.

The answer is NOT supportive. Every value on this figure is read verbatim from
results/curvature_tertile_validation.csv -- nothing is recomputed here:
  alpha leg: monotone in the predicted direction (+0.116 -> +0.153 -> +0.302), only the
             top tertile excludes 0; the decisive high-minus-low contrast is
             +0.186, 95% CI [-0.149, +0.504] -> UNSUPPORTED (underpowered, n=70/tertile).
  gamma leg: flat, no tertile excludes 0; high-minus-low +0.092 [-0.279, +0.440]
             -> UNSUPPORTED.
  reference: the headline "reversed gamma" (-0.224) comes from a DIFFERENT method
             (scVelo), whose per-gene curvature was never measured -> no tertiles.

Input : results/curvature_tertile_validation.csv (+ .md for the verdicts)
Output: figures/figS05_stiffness_tertile_ladder.png   (English labels only)

Run: ~/miniconda3/envs/scv-preprocess/bin/python figures/figS05_stiffness_tertile_ladder.py
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
BLUE, RED, GREY = "#4C72B0", "#C44E52", "#8C8C8C"

t = pd.read_csv(RES / "curvature_tertile_validation.csv")
legs = [
    ("ALPHA (MultiVelo α vs K562 synth | bin=kap_alpha)",
     "A. alpha leg -- MultiVelo fit_alpha vs K562 TT-seq synthesis rate\n"
     "binned by per-gene curvature kappa_alpha",
     BLUE),
    ("GAMMA (MultiVelo γ vs MOLM13 k_deg | bin=kap_gamma)",
     "B. gamma leg -- MultiVelo fit_gamma vs MOLM13 measured degradation rate k_deg\n"
     "binned by per-gene curvature kappa_gamma",
     RED),
]
ORDER = ["low", "mid", "high"]

fig, ax = plt.subplots(1, 2, figsize=(12.6, 6.0), sharey=True)

for k, (leg, title, col) in enumerate(legs):
    sub = t[t["leg"] == leg].set_index("bin")
    xs = np.arange(3)
    rho = [sub.loc[b, "rho"] for b in ORDER]
    lo = [sub.loc[b, "rho"] - sub.loc[b, "ci_lo"] for b in ORDER]
    hi = [sub.loc[b, "ci_hi"] - sub.loc[b, "rho"] for b in ORDER]
    ax[k].errorbar(xs, rho, yerr=[lo, hi], fmt="o", ms=8, capsize=6, lw=1.6, color=col)
    for i, b in enumerate(ORDER):
        r = sub.loc[b]
        excl = (r["ci_lo"] > 0) or (r["ci_hi"] < 0)
        ax[k].annotate(f"{r['rho']:+.3f} ({'CI excludes 0' if excl else 'CI includes 0'})",
                       (xs[i], r["ci_lo"]), textcoords="offset points", xytext=(0, -14),
                       ha="center", fontsize=8.5,
                       color="black" if excl else GREY)
    ov = sub.loc["overall"]
    ax[k].axhline(ov["rho"], color=GREY, ls="--", lw=1)
    ax[k].axhline(0, color="k", lw=0.9)
    hml = sub.loc["high_minus_low"]
    ax[k].set_xticks(xs)
    ax[k].set_xticklabels([f"{b}\nkappa median {sub.loc[b, 'kap_med']:.2f}\nn={int(sub.loc[b, 'n'])}"
                           for b in ORDER], fontsize=9)
    ax[k].set_title(title, fontsize=9.5)
    ax[k].text(0.02, 0.97,
               f"overall rho {ov['rho']:+.3f} [{ov['ci_lo']:+.3f}, {ov['ci_hi']:+.3f}] "
               f"(n={int(ov['n'])}, dashed line)\n"
               f"decisive contrast  rho(high) - rho(low) = {hml['rho']:+.3f}\n"
               f"95% CI [{hml['ci_lo']:+.3f}, {hml['ci_hi']:+.3f}], "
               f"P(diff>0)={hml['frac_gt0']:.3f}\n-> UNSUPPORTED (CI includes 0)",
               transform=ax[k].transAxes, ha="left", va="top", fontsize=9,
               bbox=dict(boxstyle="round,pad=0.35", fc="#F2F2F2", ec=GREY, lw=0.8))
    ax[k].set_xlabel("per-gene curvature (stiffness) tertile")
    ax[k].set_ylim(-0.52, 0.72)
    ax[k].set_xlim(-0.55, 2.55)
    ax[k].spines[["top", "right"]].set_visible(False)

ax[0].set_ylabel("Spearman(fitted rate, measured rate)\nwithin tertile (bootstrap 95% CI)", fontsize=9.5)

ref = t[t["leg"] == "GAMMA_scVelo_ref"].iloc[0]
fig.suptitle("Stiffness-tertile ladder: curvature does NOT demonstrably predict external validation\n"
             "(results/curvature_tertile_validation.md; scripts/p6_curvature_tertile_validation.py)\n"
             "The alpha ladder is monotone in the predicted direction and its top tertile excludes 0, but the\n"
             "high-minus-low contrast is not separable at n=70 per tertile; the gamma ladder is flat.\n"
             f"Reference: the reversed gamma correlation ({ref['rho']:+.3f} "
             f"[{ref['ci_lo']:+.3f}, {ref['ci_hi']:+.3f}], n={int(ref['n'])}) comes from scVelo, a different\n"
             "method whose per-gene curvature was never measured -- it cannot be laddered.", fontsize=9.5)
fig.tight_layout(rect=[0, 0, 1, 0.85])
out = Path(__file__).resolve().parent / "figS05_stiffness_tertile_ladder.png"
fig.savefig(out, dpi=130, bbox_inches="tight")
print(f"saved {out.name}")
print(t.to_string(index=False))
