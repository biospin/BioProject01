#!/usr/bin/env python3
"""figS03 — ATAC-shuffle (scrambled-chromatin) lag distribution vs the observed lag
(Additional file 11, panel 3).

Negative control: MultiVelo is refitted after permuting the ATAC (chromatin) layer
across cells within lineage. If the chromatin channel drove the fitted
chromatin->transcription lag, the refit lag should collapse. It does not.

This is a SINGLE scrambled realization (seed p2_config.RANDOM_SEED), i.e. an
overlay of the shuffled lag distribution on the observed one -- not a
many-permutation null envelope. Labelled as such on the figure.

Input : results/multivelo_genes.csv (observed), results/scrambled_genes.csv (ATAC-shuffled refit)
        every statistic printed here is cross-checked against results/scrambled_null.md
Output: figures/figS03_atac_shuffle_lag.png   (English labels only)

Run: ~/miniconda3/envs/scv-preprocess/bin/python figures/figS03_atac_shuffle_lag.py
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import spearmanr, mannwhitneyu, ks_2samp, wilcoxon

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
BLUE, ORANGE, GREY = "#4C72B0", "#DD8452", "#8C8C8C"

# values reported in results/scrambled_null.md (the figure must reproduce them)
MD = dict(n=538, obs_med=5.868, scr_med=5.475, mw=0.1957, ks_D=0.050, ks_p=0.5074,
          wil=0.0003, rho=0.721, relchg=0.147)


def load(name):
    d = pd.read_csv(RES / name, index_col=0)
    d = d[d["fit_likelihood"].notna()]
    return d[~d.index.duplicated()]


mv, sc = load("multivelo_genes.csv"), load("scrambled_genes.csv")
sh = mv.index.intersection(sc.index)
obs = (mv.loc[sh, "fit_t_sw2"] - mv.loc[sh, "fit_t_sw1"]).astype(float)
scr = (sc.loc[sh, "fit_t_sw2"] - sc.loc[sh, "fit_t_sw1"]).astype(float)

stats = dict(n=len(sh), obs_med=obs.median(), scr_med=scr.median(),
             mw=mannwhitneyu(obs, scr).pvalue, ks_D=ks_2samp(obs, scr).statistic,
             ks_p=ks_2samp(obs, scr).pvalue, wil=wilcoxon(obs, scr).pvalue,
             rho=spearmanr(obs, scr).statistic,
             relchg=float(np.median(np.abs(scr - obs) / np.abs(obs))))
for k, v in MD.items():
    got = stats[k]
    tol = 0.0001 if k == "wil" else max(0.002, abs(v) * 0.01)
    if abs(got - v) > tol:
        raise SystemExit(f"MISMATCH {k}: recomputed {got:.4f} vs scrambled_null.md {v}")
    print(f"[ok] {k}: {got:.4f} (scrambled_null.md {v})")

fig, ax = plt.subplots(1, 2, figsize=(12.4, 4.8))

# A. distributions overlaid
bins = np.linspace(0, max(obs.max(), scr.max()), 45)
ax[0].hist(obs, bins=bins, color=BLUE, alpha=0.60, label=f"observed (median {obs.median():.2f})")
ax[0].hist(scr, bins=bins, color=ORANGE, alpha=0.60,
           label=f"ATAC-shuffled refit (median {scr.median():.2f})")
ax[0].axvline(obs.median(), color=BLUE, ls="--", lw=1.4)
ax[0].axvline(scr.median(), color=ORANGE, ls="--", lw=1.4)
ax[0].set_xlabel("MultiVelo lag  fit_t_sw2 - fit_t_sw1  (pseudotime)")
ax[0].set_ylabel("genes")
ax[0].set_title(f"A. Shuffling the chromatin layer leaves the\nlag distribution intact (n={len(sh)})\n"
                f"Mann-Whitney p={stats['mw']:.3f}; KS D={stats['ks_D']:.3f}, p={stats['ks_p']:.3f}\n"
                f"paired Wilcoxon p={stats['wil']:.1e} (small systematic shift)", fontsize=9.5)
ax[0].legend(fontsize=9)
ax[0].spines[["top", "right"]].set_visible(False)

# B. per-gene paired
lim = max(obs.max(), scr.max()) * 1.02
ax[1].plot([0, lim], [0, lim], color=GREY, lw=1, ls=":")
ax[1].scatter(obs, scr, s=9, alpha=0.45, color=BLUE, linewidths=0)
ax[1].set_xlim(0, lim); ax[1].set_ylim(0, lim)
ax[1].set_xlabel("observed lag (pseudotime)")
ax[1].set_ylabel("ATAC-shuffled refit lag (pseudotime)")
ax[1].set_title(f"B. Per-gene lag survives the shuffle:\nSpearman {stats['rho']:.3f}, median relative change {stats['relchg']:.1%}\n"
                "the lag is set by gene-intrinsic RNA dynamics and the\nmodel's monotone switch ordering, not by chromatin",
                fontsize=9.5)
ax[1].spines[["top", "right"]].set_visible(False)

fig.suptitle("ATAC-shuffle negative control: a single within-lineage chromatin permutation, refit end to end "
             "(results/scrambled_null.md; scripts/p3_scrambled_null.py)\n"
             "One realization, seed p2_config.RANDOM_SEED -- an overlay of the shuffled distribution on the "
             "observed one, not a multi-permutation null envelope.", fontsize=10)
fig.tight_layout(rect=[0, 0, 1, 0.90])
out = Path(__file__).resolve().parent / "figS03_atac_shuffle_lag.png"
fig.savefig(out, dpi=130, bbox_inches="tight")
print(f"saved {out.name}")
