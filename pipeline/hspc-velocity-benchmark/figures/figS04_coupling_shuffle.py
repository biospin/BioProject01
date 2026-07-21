#!/usr/bin/env python3
"""figS04 — chromatin-RNA coupling vs its ATAC-shuffle (Additional file 11, panel 4).

coupling[g] = Spearman(C[:, g], S[:, g]) across the 21,878 HSPC cells
(C = chromatin layer, S = Ms spliced), on the 538 MultiVelo genes.
The shuffle permutes the ATAC gene labels and recomputes.

Contrast with figS03: the model lag is INVARIANT to the chromatin shuffle, whereas
this model-free coupling COLLAPSES -- so coupling is genuinely chromatin-dependent.
It is still not a usable replacement for the lag, because it fails the
cross-dataset reproducibility criterion (results/coupling_lag_alternative.md,
verdict A: HSPC<->human_brain rho=+0.173, prespecified failure bound |rho|<=0.2).

Input : results/coupling_per_gene.csv (columns coupling, coupling_shuffle0, abundance)
        checked against results/coupling_lag_alternative.md
Output: figures/figS04_coupling_shuffle.png   (English labels only)

CAVEAT rendered on the figure: the CSV stores realization 0 only. The pooled
Mann-Whitney p=5.6e-75 in the results markdown was computed over K=20 shuffle
realizations (scripts/p7_coupling_lag_alternative.py); it is quoted, not recomputed here.

Run: ~/miniconda3/envs/scv-preprocess/bin/python figures/figS04_coupling_shuffle.py
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
GREEN, GREY, BLUE = "#55A868", "#8C8C8C", "#4C72B0"

MD = dict(real_med=0.126, real_pos=0.872, delta_med=0.098, delta_pos=0.753)
MD_POOLED_MW = "5.6e-75"   # quoted from results/coupling_lag_alternative.md (K=20 shuffles)

cp = pd.read_csv(RES / "coupling_per_gene.csv")
real, shuf = cp["coupling"].astype(float), cp["coupling_shuffle0"].astype(float)
delta = real - shuf
got = dict(real_med=real.median(), real_pos=(real > 0).mean(),
           delta_med=delta.median(), delta_pos=(delta > 0).mean())
for k, v in MD.items():
    if abs(got[k] - v) > 0.002:
        raise SystemExit(f"MISMATCH {k}: recomputed {got[k]:.4f} vs coupling_lag_alternative.md {v}")
    print(f"[ok] {k}: {got[k]:.3f} (coupling_lag_alternative.md {v})")
print(f"[note] shuffle realization 0 median {shuf.median():+.3f} "
      f"(md quotes +0.021 pooled over 20 realizations)")

fig, ax = plt.subplots(1, 3, figsize=(16.4, 4.6))

# A. distributions
bins = np.linspace(-0.6, 0.9, 60)
ax[0].hist(real, bins=bins, color=GREEN, alpha=0.65, label=f"observed (median {real.median():+.3f})")
ax[0].hist(shuf, bins=bins, color=GREY, alpha=0.65,
           label=f"ATAC-shuffled (median {shuf.median():+.3f})")
ax[0].axvline(0, color="k", lw=0.8)
ax[0].set_xlabel("per-gene chromatin-RNA coupling  Spearman(C, S) across cells")
ax[0].set_ylabel("genes")
ax[0].set_title(f"A. Coupling collapses under the ATAC shuffle (n={len(cp)})\n"
                f"{got['real_pos']:.1%} of genes positive when observed; pooled Mann-Whitney "
                f"p={MD_POOLED_MW} over 20 shuffles (quoted)", fontsize=9.5)
ax[0].legend(fontsize=9); ax[0].spines[["top", "right"]].set_visible(False)

# B. paired scatter
lim = (min(real.min(), shuf.min()) * 1.05, max(real.max(), shuf.max()) * 1.05)
ax[1].plot(lim, lim, color=GREY, ls=":", lw=1)
ax[1].axhline(0, color="k", lw=0.6); ax[1].axvline(0, color="k", lw=0.6)
ax[1].scatter(shuf, real, s=9, alpha=0.45, color=GREEN, linewidths=0)
ax[1].set_xlim(*lim); ax[1].set_ylim(*lim)
ax[1].set_xlabel("ATAC-shuffled coupling (realization 0)")
ax[1].set_ylabel("observed coupling")
ax[1].set_title("B. Almost every gene sits above the identity line", fontsize=9.5)
ax[1].spines[["top", "right"]].set_visible(False)

# C. per-gene delta
ax[2].hist(delta, bins=50, color=BLUE, edgecolor="white")
ax[2].axvline(0, color="k", lw=1)
ax[2].axvline(delta.median(), color="crimson", ls="--", lw=1.4,
              label=f"median {delta.median():+.3f}")
ax[2].set_xlabel("per-gene delta = observed - shuffled coupling")
ax[2].set_ylabel("genes")
ax[2].set_title(f"C. Positive for {got['delta_pos']:.1%} of genes\n"
                "contrast: the model lag is unchanged by the same shuffle (Fig S3)", fontsize=9.5)
ax[2].legend(fontsize=9); ax[2].spines[["top", "right"]].set_visible(False)

fig.suptitle("Chromatin-RNA coupling shuffle control (results/coupling_lag_alternative.md; "
             "scripts/p7_coupling_lag_alternative.py)\n"
             "Coupling is chromatin-dependent where the fitted lag is not -- but it is NOT a reproducible "
             "replacement for the lag: cross-dataset rho=+0.173 (HSPC vs human brain) fails the "
             "prespecified |rho|>0.2 bound, and it replicates only in the nearest tissue (macrophage +0.281).",
             fontsize=10)
fig.tight_layout(rect=[0, 0, 1, 0.88])
out = Path(__file__).resolve().parent / "figS04_coupling_shuffle.png"
fig.savefig(out, dpi=130, bbox_inches="tight")
print(f"saved {out.name}")
