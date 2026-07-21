#!/usr/bin/env python3
"""fig05 — Profile-likelihood practical identifiability (NOVELTY-EXTENSIONS §2).

Demonstrates, on MultiVelo's OWN objective, that the transcription rate alpha is the
STIFF (locally identifiable) direction while the chromatin->transcription lag is
systematically SLOPPIER and frequently boundary-pinned/degenerate. Honest framing:
this is RELATIVE / practical non-identifiability, NOT a flat likelihood valley.

Input : results/profile_likelihood_identifiability.csv (+ profile_likelihood_freed.csv)
Output: figures/fig05_profile_likelihood.png  (English labels only; image gitignored)

Run (mv env, needs multivelo for panel D recompute):
  conda run --no-capture-output -n velo-mv python figures/fig05_profile_likelihood.py
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
sys.path.insert(0, str(ROOT / "scripts"))

df = pd.read_csv(RES / "profile_likelihood_identifiability.csv")
freed = None
fp = RES / "profile_likelihood_freed.csv"
if fp.exists():
    freed = pd.read_csv(fp)

BLUE, RED, GREY = "#4C72B0", "#C44E52", "#8C8C8C"
fig, ax = plt.subplots(2, 2, figsize=(11.5, 9))

# ---- A. paired per-cell log-curvature: alpha stiff vs lag sloppy ----
ka = df["kappa_alpha_pc"].replace([np.inf, -np.inf], np.nan).dropna()
kl = df["kappa_lag_pc"].replace([np.inf, -np.inf], np.nan).dropna()
ka = ka[ka > 0]; kl = kl[kl > 0]
parts = ax[0, 0].violinplot([np.log10(ka), np.log10(kl)], showmedians=True)
for i, pc in enumerate(parts["bodies"]):
    pc.set_facecolor([RED, BLUE][i]); pc.set_alpha(0.55)
ax[0, 0].set_xticks([1, 2]); ax[0, 0].set_xticklabels(
    [f"alpha\nmed {ka.median():.2f}/cell", f"lag\nmed {kl.median():.2f}/cell"])
ax[0, 0].set_ylabel("log10 curvature  -d2 LL / d(ln theta)2  per cell")
ax[0, 0].set_title(f"A. alpha is the stiff direction, lag the sloppy one (n={len(df)})")

# ---- B. per-gene stiffness ratio kappa_alpha / kappa_lag ----
ratio = df["ratio"].replace([np.inf, -np.inf], np.nan).dropna()
ratio = ratio[ratio > 0]
ax[0, 1].hist(np.log10(ratio), bins=30, color=BLUE, edgecolor="white")
ax[0, 1].axvline(0, color="k", ls="-", lw=1, label="equal (ratio=1)")
ax[0, 1].axvline(np.log10(ratio.median()), color=RED, ls="--",
                 label=f"median {ratio.median():.2f}x")
ax[0, 1].set_xlabel("log10( kappa_alpha / kappa_lag )")
ax[0, 1].set_ylabel("genes (interior, both curvatures > 0)")
ax[0, 1].set_title(f"B. alpha stiffer than lag in {(ratio>1).mean():.0%} of genes")
ax[0, 1].legend()

# ---- C. honest population trichotomy of the lag profile ----
order = ["interior", "boundary_pinned", "degenerate"]
cnt = df["lag_cls"].value_counts()
vals = [int(cnt.get(k, 0)) for k in order]
cols = [BLUE, "#DD8452", GREY]
bars = ax[1, 0].bar(range(3), vals, color=cols, edgecolor="white")
ax[1, 0].set_xticks(range(3))
ax[1, 0].set_xticklabels(["interior\n(sloppy but scannable)",
                          "boundary-pinned\n(t_sw2 ~ 20)", "degenerate"])
for b, v in zip(bars, vals):
    ax[1, 0].text(b.get_x() + b.get_width() / 2, v, f"{v}\n{v/len(df):.0%}",
                  ha="center", va="bottom", fontsize=9)
ax[1, 0].set_ylabel("genes")
ax[1, 0].set_ylim(0, max(vals) * 1.25)
ax[1, 0].set_title("C. lag population: a large share is boundary-limited")

# ---- D. representative overlaid profiles (recompute, same objective) ----
try:
    import scanpy as sc
    from p3_profile_likelihood import load, prep, LL, TOTAL_H
    a, C, U, S, conn = load()
    V = a.var; genes = list(a.var_names)
    interior = df[(df.lag_cls == "interior") & df.ratio.notna()].copy()
    # representative: ratio closest to median, decent cell count
    interior["d"] = (interior.ratio - ratio.median()).abs()
    g_name = interior.sort_values(["d", "nkeep"], ascending=[True, False]).iloc[0].gene
    gi = genes.index(g_name); r = V.iloc[gi]; g = prep(C, U, S, gi)
    ac, al, be, ga = r.fit_alpha_c, r.fit_alpha, r.fit_beta, r.fit_gamma
    t1, t2, t3 = r.fit_t_sw1, r.fit_t_sw2, r.fit_t_sw3; gap = t3 - t2
    model, direc = int(r.fit_model), str(r.fit_direction)
    rc, ru, scc = r.fit_rescale_c, r.fit_rescale_u, r.fit_scale_cc
    lag0 = t2 - t1; nk = g["nkeep"]
    xs = np.linspace(-1.2, 1.2, 25)            # standardized log-perturbation
    fa = lambda x: LL(g, conn, ac, al * np.exp(x), be, ga, np.array([t1, t2, t3]), rc, ru, scc, model, direc)
    def fl(x):
        lg = lag0 * np.exp(x)
        if t1 + lg > TOTAL_H:
            return np.nan
        return LL(g, conn, ac, al, be, ga, np.array([t1, t1 + lg, t1 + lg + gap]), rc, ru, scc, model, direc)
    la = np.array([fa(x) for x in xs]) / nk
    ll = np.array([fl(x) for x in xs]) / nk
    la -= np.nanmax(la); ll -= np.nanmax(ll)
    ax[1, 1].plot(xs, la, "-o", ms=3, color=RED, label="alpha (stiff)")
    ax[1, 1].plot(xs, ll, "-s", ms=3, color=BLUE, label="lag (sloppy)")
    ax[1, 1].axhline(0, color="k", lw=0.6)
    ax[1, 1].set_ylim(bottom=max(-3.0, np.nanmin([np.nanmin(la), np.nanmin(ll)]) * 1.05))
    ax[1, 1].set_xlabel("standardized log-perturbation  ln(theta / MLE)")
    ax[1, 1].set_ylabel("per-cell log-likelihood drop (nats/cell)")
    ax[1, 1].set_title(f"D. profiles for {g_name} (lag0={lag0:.1f} pt): alpha narrow, lag shallow")
    ax[1, 1].legend()
except Exception as e:  # figure still useful without panel D
    ax[1, 1].text(0.5, 0.5, f"panel D recompute skipped:\n{e}", ha="center",
                  va="center", wrap=True, fontsize=8)
    ax[1, 1].set_axis_off()

sub = ""
# freed-nuisance gate CSV is only a partial/stale smoke (main 538-gene fixed-nuisance
# result carries the claim); do not surface a misleading tiny-n number in the figure.
fig.suptitle("Profile-likelihood: transcription rate alpha is locally identifiable; the chromatin->transcription "
             "lag is sloppier + boundary-limited\n(MultiVelo objective, latent time re-optimized; RELATIVE practical "
             "non-identifiability, not a flat valley)" + ("\n" + sub if sub else ""),
             fontsize=10.5, y=1.0)
fig.tight_layout(rect=[0, 0, 1, 0.96])
out = Path(__file__).resolve().parent / "fig05_profile_likelihood.png"
fig.savefig(out, dpi=130, bbox_inches="tight")
print(f"saved {out.name}  ratio med {ratio.median():.2f}x  alpha stiffer {(ratio>1).mean():.0%}")
