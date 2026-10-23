#!/usr/bin/env python3
"""fig01 v2 — Figure 1 of the GIW long abstract — cross-method agreement of α versus the per-gene lag in HSPC.

Replaces fig01_p2_concordance (floor vs MultiVelo; MultiVelo lag = t_sw2 − t_sw1 only) with the
harmonized comparison promised in the ML4H Submission 294 rebuttal (2026-10-13):
one method pair (MultiVelo × MultiVeloVAE), one gene set (538 shared genes), every lag
definition side by side, MultiVelo's priming interval (t_sw1) as the primary lag.

  A  α scatter, MultiVelo vs MultiVeloVAE (log10), Spearman ρ.
  B  Spearman ρ with 95% CI for α, α_c and every lag definition; Δρ = ρ_α − ρ_output.

Point estimates are recomputed from the per-gene tables with the p17 definitions and asserted
equal to post_review_robustness.gen.md; CIs and Δρ are read from that machine output
(B=10,000 paired bootstrap, seed 20261010), not re-bootstrapped here.

Run:
  conda run -n scv-preprocess python pipeline/hspc-velocity-benchmark/figures/fig01_concordance_v2.py
"""
from __future__ import annotations

import re
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
RES = HERE.parent / "results"
GEN = (RES / "post_review_robustness.gen.md").read_text(encoding="utf-8")

SURFACE, INK, INK2, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#e1e0d9", "#c3c2b7"
C_ALPHA, C_LAG, C_REF = "#2a78d6", "#eb6834", "#8a8984"   # series-1, series-2, neutral


# ---------------------------------------------------------------- data (p17 definitions)
def load(name):
    d = pd.read_csv(RES / name, index_col=0)
    if "fit_likelihood" in d.columns:
        d = d[d["fit_likelihood"].notna()]
    d.index = [str(x).upper() for x in d.index]
    return d[~d.index.duplicated()]


def spear(a, b):
    return float(np.corrcoef(pd.Series(a).rank().values, pd.Series(b).rank().values)[0, 1])


def gen_row(analysis, metric):
    """(point, lo, hi) from the machine-output table."""
    m = re.search(rf"^\| {re.escape(analysis)} \| {metric} \| (\d+) \| ([+-]\d\.\d+) \| "
                  rf"\[([+-]\d\.\d+), ([+-]\d\.\d+)\] \|$", GEN, re.M)
    assert m, f"row not found in gen.md: {analysis} / {metric}"
    return int(m[1]), float(m[2]), float(m[3]), float(m[4])


mv, vae, mo = load("multivelo_genes.csv"), load("multivelovae_genes.csv"), load("moflow_genes.csv")
sh = sorted(set(mv.index) & set(vae.index))
A, V = mv.loc[sh], vae.loc[sh]
proxy = lambda ac, a: 1 / ac.clip(1e-6) - 1 / a.clip(1e-6)
vae_mag = np.abs(proxy(V.vae_alpha_c, V.vae_alpha)).values
sh3 = sorted(set(sh) & set(mo.index[mo.cs_lag_median.notna()]))

# label, colour, (analysis, metric) for ρ, (analysis, metric) for Δρ or None, recomputed ρ
ROWS = [
    ("α  (transcription rate)", C_ALPHA, ("contract_MVxVAE", "rho_alpha"), None,
     spear(A.fit_alpha, V.vae_alpha)),
    ("α_c  (chromatin-opening rate)", C_REF, ("R1_alpha_c", "rho"), ("R1_alpha_c", "delta_rho_alpha_minus"),
     spear(A.fit_alpha_c, V.vae_alpha_c)),
    ("lag · MultiVelo priming interval (t_sw1)\n   vs VAE rate proxy, magnitude", C_LAG,
     ("R5_MVxVAE_priming", "rho"), ("R5_MVxVAE_priming", "delta_rho_alpha_minus"),
     spear(A.fit_t_sw1, vae_mag)),
    ("lag · MultiVelo coupled-on (t_sw2 − t_sw1)\n   vs VAE rate proxy, magnitude", C_LAG,
     ("R5_MVxVAE_coupled_on", "rho"), ("R5_MVxVAE_coupled_on", "delta_rho_alpha_minus"),
     spear(np.abs(A.fit_t_sw2 - A.fit_t_sw1), vae_mag)),
    ("lag · same formula in both (1/α_c − 1/α),\n   signed", C_LAG,
     ("R1_lag_rateproxy_signed", "rho"), ("R1_lag_rateproxy_signed", "delta_rho_alpha_minus"),
     spear(proxy(A.fit_alpha_c, A.fit_alpha), proxy(V.vae_alpha_c, V.vae_alpha))),
    ("lag · same formula in both (1/α_c − 1/α),\n   magnitude", C_LAG,
     ("R1_lag_rateproxy_mag", "rho"), ("R1_lag_rateproxy_mag", "delta_rho_alpha_minus"),
     spear(np.abs(proxy(A.fit_alpha_c, A.fit_alpha)), np.abs(proxy(V.vae_alpha_c, V.vae_alpha)))),
    ("lag · MultiVelo priming vs MoFlow DTW offset,\n   magnitude (537 genes)", C_LAG,
     ("R5_MVxMoFlow_priming", "rho"), ("R5_MVxMoFlow_priming", "delta_rho_alpha_minus"),
     spear(mv.loc[sh3].fit_t_sw1, np.abs(mo.loc[sh3].cs_lag_median))),
]

# Guard: recomputed point estimates must match the machine output to its printed precision.
for label, _c, key, _d, rho in ROWS:
    _n, pt, _lo, _hi = gen_row(*key)
    assert abs(rho - pt) < 6e-4, f"{label!r}: recomputed {rho:+.4f} vs gen.md {pt:+.3f}"
assert len(sh) == 538 and len(sh3) == 537, (len(sh), len(sh3))

fmt = lambda v: f"{v:+.3f}".replace("-", "−")

# ---------------------------------------------------------------- render
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 6.2, "axes.edgecolor": AXIS,
                     "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2})
fig = plt.figure(figsize=(7.0, 2.4), facecolor=SURFACE)
gs = fig.add_gridspec(1, 3, width_ratios=[1, 0.86, 1.47], wspace=0.0, left=0.07, right=0.985,
                      top=0.88, bottom=0.15)

# A. α scatter
ax = fig.add_subplot(gs[0]); ax.set_facecolor(SURFACE)
x, y = np.log10(A.fit_alpha.clip(1e-6)), np.log10(V.vae_alpha.clip(1e-6))
ax.scatter(x, y, s=4, color=C_ALPHA, alpha=0.55, linewidths=0)
lo, hi = min(x.min(), y.min()), max(x.max(), y.max())
_, a_pt, a_lo, a_hi = gen_row("contract_MVxVAE", "rho_alpha")
ax.set_xlabel("MultiVelo α (log10)"); ax.set_ylabel("MultiVeloVAE α (log10)")
ax.grid(color=GRID, lw=0.6); ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.text(0.03, 0.97, f"Spearman ρ = {fmt(a_pt)}\n95% CI [{fmt(a_lo)}, {fmt(a_hi)}]\n{len(sh)} genes",
        transform=ax.transAxes, ha="left", va="top", fontsize=6.2, color=INK)
ax.set_title("A   α across methods", loc="left", fontsize=7.6, fontweight="bold", color=INK)

# B. ρ with 95% CI per output / lag definition
bx = fig.add_subplot(gs[2]); bx.set_facecolor(SURFACE)
lab = fig.add_subplot(gs[1], sharey=bx); lab.set_axis_off()
ys = np.arange(len(ROWS))[::-1]
for yy, (label, col, key, dkey, _r) in zip(ys, ROWS):
    _n, pt, l, h = gen_row(*key)
    bx.plot([l, h], [yy, yy], color=col, lw=1.4, solid_capstyle="round", zorder=2)
    bx.scatter([pt], [yy], s=22, color=col, edgecolors=SURFACE, linewidths=1.6, zorder=3)
    lab.text(0.04, yy, label, ha="left", va="center", fontsize=5.9, color=INK, linespacing=1.15,
             transform=lab.get_yaxis_transform())
    bx.text(max(h, 0.0) + 0.03, yy + 0.02, fmt(pt), ha="left", va="center", fontsize=5.9, color=INK)
    if dkey:
        _n, d, dl, dh = gen_row(*dkey)
        bx.text(1.36, yy, f"Δρ {fmt(d)}\n[{fmt(dl)}, {fmt(dh)}]", ha="right", va="center",
                fontsize=5.6, color=INK2, linespacing=1.1)
bx.axvline(0, color=AXIS, lw=1, zorder=1)
_n, a_pt, _l, _h = gen_row("contract_MVxVAE", "rho_alpha")
bx.axvline(a_pt, color=C_ALPHA, lw=0.8, ls=(0, (3, 3)), zorder=1)
bx.set_xlim(-0.25, 1.36); bx.set_ylim(-0.6, len(ROWS) - 0.4)
bx.set_xticks([-0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0])
bx.set_yticks([])
bx.grid(axis="x", color=GRID, lw=0.6); bx.set_axisbelow(True)
for s in ("top", "right", "left"):
    bx.spines[s].set_visible(False)
bx.spines["bottom"].set_bounds(-0.2, 1.0)
bx.set_xlabel("Spearman ρ between methods (95% CI)", x=0.44)
bx.text(1.36, len(ROWS) - 0.45, "Δρ = ρ_α − ρ_output", ha="right", va="bottom", fontsize=5.8,
        color=INK2, style="italic")
lab.set_title("B   the lag under every definition", loc="left", fontsize=7.6,
              fontweight="bold", color=INK)

# Footnote dropped for print (2-column width): the figure caption carries it.

out = HERE / "fig01_concordance_v2.png"
fig.savefig(out, dpi=300, facecolor=SURFACE)
print(f"saved {out}  (all point estimates match gen.md)")
