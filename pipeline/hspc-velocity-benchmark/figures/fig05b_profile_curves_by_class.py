#!/usr/bin/env python3
"""fig05b — representative profile-likelihood curves, one gene per lag class (ML4H rebuttal).

Reviewer vjwq asked for representative profile curves. One gene is drawn per lag class
(interior / boundary-pinned / degenerate, as classified in p3_profile_likelihood.py), each
with its alpha profile (top) and lag profile (bottom), on MultiVelo's own objective.

Selection rule (fixed, no hand-picking):
  interior         -> stiffness ratio closest to the class median (same gene as fig05 panel D)
  boundary-pinned  -> per-cell alpha curvature closest to the class median
  degenerate       -> per-cell alpha curvature closest to the class median
  ties broken by more retained cells (nkeep).

Curves are drawn as Delta LL = LL(theta) - LL(theta_hat) per cell, i.e. relative to the
fitted value, not to the scan maximum, so a curve rising above 0 would show the fit is not
the profile maximum.

Input : results/profile_likelihood_identifiability.csv, data/velocity/multivelo.h5ad
        (the fit that produced the CSV; check: TLE1 lag0 = 1.784)
Output: figures/fig05b_profile_curves_by_class.png
Run   : python figures/fig05b_profile_curves_by_class.py   (env with multivelo + scanpy)
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
sys.path.insert(0, str(ROOT / "scripts"))
from p3_profile_likelihood import load, prep, LL, TOTAL_H  # noqa: E402

df = pd.read_csv(ROOT / "results" / "profile_likelihood_identifiability.csv")
a, C, U, S, conn = load()
V = a.var
genes = list(a.var_names)

# the h5ad must be the fit the CSV came from
row = df.set_index("gene").loc["TLE1"]
v = V.loc["TLE1"]
assert abs((v.fit_t_sw2 - v.fit_t_sw1) - row.lag0) < 1e-6, "h5ad is not the fit behind the CSV"


def pick(cls):
    d = df[df.lag_cls == cls].copy()
    if cls == "interior":
        d = d[d.ratio.notna()]
        d["d"] = (d.ratio - d.ratio.median()).abs()
    else:
        d = d[d.kappa_alpha_pc.notna() & np.isfinite(d.kappa_alpha_pc)]
        d["d"] = (d.kappa_alpha_pc - d.kappa_alpha_pc.median()).abs()
    return d.sort_values(["d", "nkeep"], ascending=[True, False]).iloc[0].gene


CLASSES = [("interior", "Interior lag"), ("boundary_pinned", "Boundary-pinned lag"),
           ("degenerate", "Degenerate lag")]
xs = np.linspace(-1.2, 1.2, 25)
RED, BLUE = "#C44E52", "#4C72B0"
fig, ax = plt.subplots(2, 3, figsize=(13, 7.2), sharex=True)

for j, (cls, label) in enumerate(CLASSES):
    gname = pick(cls)
    r = V.loc[gname]
    g = prep(C, U, S, genes.index(gname))
    ac, al, be, ga = r.fit_alpha_c, r.fit_alpha, r.fit_beta, r.fit_gamma
    t1, t2, t3 = r.fit_t_sw1, r.fit_t_sw2, r.fit_t_sw3
    gap, lag0, nk = t3 - t2, t2 - t1, g["nkeep"]
    rc, ru, scc = r.fit_rescale_c, r.fit_rescale_u, r.fit_scale_cc
    model, direc = int(r.fit_model), str(r.fit_direction)

    def ll_alpha(x):
        return LL(g, conn, ac, al * np.exp(x), be, ga, np.array([t1, t2, t3]),
                  rc, ru, scc, model, direc)

    def ll_lag(x):
        lg = lag0 * np.exp(x)
        # past the pseudotime horizon the lag cannot grow; the fitted point itself is kept
        # (boundary-pinned fits sit at or just past the horizon by construction)
        if x > 0 and t1 + lg > TOTAL_H:
            return np.nan
        return LL(g, conn, ac, al, be, ga, np.array([t1, t1 + lg, t1 + lg + gap]),
                  rc, ru, scc, model, direc)

    la = np.array([ll_alpha(x) for x in xs]) / nk
    ll = np.array([ll_lag(x) for x in xs]) / nk
    la -= ll_alpha(0.0) / nk
    l0 = ll_lag(0.0)
    ll = ll - l0 / nk if np.isfinite(l0) else ll * np.nan

    for i, (y, col, nm) in enumerate([(la, RED, r"$\alpha$"), (ll, BLUE, "lag")]):
        axx = ax[i, j]
        axx.plot(xs, y, "-o", ms=3, color=col)
        axx.axhline(0, color="k", lw=0.6)
        axx.axvline(0, color="0.6", lw=0.6, ls=":")
        fin = y[np.isfinite(y)]
        if fin.size:
            axx.set_ylim(max(-3.0, fin.min() * 1.05 - 0.05), max(0.2, fin.max() * 1.1 + 0.05))
        if i == 1:
            past = xs[(xs > 0) & (t1 + lag0 * np.exp(xs) > TOTAL_H)]
            if past.size:
                axx.axvspan(past.min() - 0.05, xs.max() + 0.05, color="0.92", zorder=0)
                axx.text(past.min(), 0.97, " past pseudotime\n horizon", fontsize=8,
                         va="top", ha="left", color="0.35", transform=axx.get_xaxis_transform())
            miss = xs[~np.isfinite(y) & ~((xs > 0) & (t1 + lag0 * np.exp(xs) > TOTAL_H))]
            if miss.size:
                print(f"  {gname}: likelihood not evaluable at x =", np.round(miss, 2))
            axx.set_xlabel(r"log-perturbation $\ln(\theta/\hat\theta)$")
        if j == 0:
            axx.set_ylabel(f"{nm}: $\\Delta$ log-likelihood per cell")
    ax[0, j].set_title(f"{label}: {gname}\n(fitted lag {lag0:.2f}, {nk} cells)", fontsize=10.5)
    print(f"{cls:16s} {gname:10s} lag0={lag0:.3f} t_sw1={t1:.3f} nkeep={nk} "
          f"alpha_min={np.nanmin(la):.3f} lag_min={np.nanmin(ll) if np.isfinite(ll).any() else float('nan'):.3f} "
          f"lag_max={np.nanmax(ll) if np.isfinite(ll).any() else float('nan'):.3f}")

fig.tight_layout()
out = Path(__file__).resolve().parent / "fig05b_profile_curves_by_class.png"
fig.savefig(out, dpi=150, bbox_inches="tight")
print("saved", out.name)
