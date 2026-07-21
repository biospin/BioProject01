#!/usr/bin/env python3
"""figS01 — per-dataset cross-method concordance scatter (Additional file 11, panel 1).

For each of the five multiome systems that carry two chromatin-aware velocity arms,
plot the rank-rank scatter of MultiVelo vs MultiVeloVAE for
  (top row)    transcription rate alpha            -> the reproducible leg
  (bottom row) chromatin->transcription lag magnitude -> the fragile leg

Definitions are taken verbatim from the concordance scripts (so the rho printed here
must equal the rho already reported in results/concordance_*.md):
  alpha : MultiVelo fit_alpha            vs MultiVeloVAE vae_alpha
  lag   : |MultiVelo fit_t_sw2 - fit_t_sw1| vs |1/vae_alpha_c - 1/vae_alpha|
  gene set: fit_likelihood-notna genes, intersection of the two arms.
(cross_dataset/p3_concordance_macrophage.py lines "A1/A2"; same for BMMC/E18/gastrulation.)

Input : results/multivelo_genes[_<ds>].csv, results/multivelovae_genes[_<ds>].csv
Output: figures/figS01_per_dataset_concordance.png   (English labels only)

Run: ~/miniconda3/envs/scv-preprocess/bin/python figures/figS01_per_dataset_concordance.py
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import spearmanr, rankdata

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
GREEN, RED = "#55A868", "#C44E52"

# (label, filename suffix, rho_alpha reported in results/*.md, rho_lag reported, source)
DATASETS = [
    ("HSPC (GSE209878)",        "",                  0.882, None,   "concordance.md 3.6"),
    ("Macrophage",              "_macrophage",       0.917, 0.074,  "concordance_macrophage.md A1/A2"),
    ("E18 mouse brain",         "_e18_mouse_brain",  0.898, 0.057,  "concordance_e18_mouse_brain.md A1/A2"),
    ("Human BMMC (GSE194122)",  "_GSE194122_bmmc",   0.906, -0.088, "concordance_GSE194122_bmmc.md A1/A2"),
    ("Mouse gastrulation\n(GSE205117)", "_gse205117", 0.953, -0.026, "prereg_gse205117_scorecard.csv"),
]


def load(name: str) -> pd.DataFrame:
    d = pd.read_csv(RES / name, index_col=0)
    if "fit_likelihood" in d.columns:
        d = d[d["fit_likelihood"].notna()]
    return d[~d.index.duplicated()]


def check(computed: float, reported: float | None, what: str) -> str:
    """Hard-fail if a recomputed rho drifts from the number already in results/*.md."""
    if reported is None:
        print(f"  [new] {what}: rho={computed:+.3f} (no prior value in results/*.md)")
        return "newly computed"
    if abs(computed - reported) > 0.002:
        raise SystemExit(f"MISMATCH {what}: recomputed {computed:+.4f} vs results/*.md {reported:+.4f}")
    print(f"  [ok ] {what}: rho={computed:+.3f} matches results/*.md {reported:+.3f}")
    return "matches results/*.md"


fig, ax = plt.subplots(2, len(DATASETS), figsize=(19, 7.4))
summary = []

for j, (label, sfx, exp_a, exp_l, src) in enumerate(DATASETS):
    mv = load(f"multivelo_genes{sfx}.csv")
    vae = load(f"multivelovae_genes{sfx}.csv")
    sh = mv.index.intersection(vae.index)
    print(f"{label.splitlines()[0]}  shared n={len(sh)}")

    # --- alpha (robust leg) ---
    a1 = mv.loc[sh, "fit_alpha"].astype(float)
    a2 = vae.loc[sh, "vae_alpha"].astype(float)
    r_a = float(spearmanr(a1, a2).statistic)
    check(r_a, exp_a, f"{label.splitlines()[0]} alpha MVxVAE")
    ax[0, j].scatter(rankdata(a1), rankdata(a2), s=7, alpha=0.45, color=GREEN, linewidths=0)
    ax[0, j].set_title(f"{label}\nalpha: Spearman {r_a:+.3f}  (n={len(sh)})", fontsize=9.5)

    # --- lag magnitude (fragile leg) ---
    l1 = (mv.loc[sh, "fit_t_sw2"].astype(float) - mv.loc[sh, "fit_t_sw1"].astype(float)).abs()
    l2 = (1.0 / vae.loc[sh, "vae_alpha_c"].astype(float).clip(1e-6)
          - 1.0 / vae.loc[sh, "vae_alpha"].astype(float).clip(1e-6)).abs()
    r_l = float(spearmanr(l1, l2).statistic)
    check(r_l, exp_l, f"{label.splitlines()[0]} |lag| MVxVAE")
    ax[1, j].scatter(rankdata(l1), rankdata(l2), s=7, alpha=0.45, color=RED, linewidths=0)
    ax[1, j].set_title(f"lag magnitude: Spearman {r_l:+.3f}", fontsize=9.5)

    for i in (0, 1):
        ax[i, j].set_xticks([]); ax[i, j].set_yticks([])
        ax[i, j].spines[["top", "right"]].set_visible(False)
    summary.append((label.replace("\n", " "), len(sh), r_a, r_l))

ax[0, 0].set_ylabel("MultiVeloVAE rank (vae_alpha)", fontsize=9)
ax[1, 0].set_ylabel("MultiVeloVAE rank (|1/a_c - 1/a|)", fontsize=9)
for j in range(len(DATASETS)):
    ax[1, j].set_xlabel("MultiVelo rank", fontsize=9)

fig.suptitle("Cross-method concordance within each dataset (MultiVelo x MultiVeloVAE, rank-rank): "
             "the transcription rate alpha reproduces in all five systems, the chromatin->transcription "
             "lag magnitude does not\n"
             "Genes are the fit_likelihood-defined intersection of the two arms; "
             "MultiVelo lag sign is structurally positive (4-state monotone ordering) so only magnitude "
             "rank is compared.", fontsize=10.5)
fig.tight_layout(rect=[0, 0, 1, 0.90])
out = Path(__file__).resolve().parent / "figS01_per_dataset_concordance.png"
fig.savefig(out, dpi=130, bbox_inches="tight")
print(f"\nsaved {out.name}")
for lab, n, ra, rl in summary:
    print(f"  {lab:34s} n={n:5d}  alpha {ra:+.3f}  |lag| {rl:+.3f}")
