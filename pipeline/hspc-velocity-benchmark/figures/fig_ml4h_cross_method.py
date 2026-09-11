#!/usr/bin/env python3
"""fig_ml4h_cross_method — HSPC cross-method concordance, the ML4H 4-page paper's Figure 1.

The paper's headline is that only the transcription rate alpha reproduces across methods
while the chromatin->transcription lag does not. This figure shows exactly that, on the
same pair the text cites (MultiVelo x MultiVeloVAE, HSPC):

  left  : alpha rank-rank        -> Spearman +0.882  (the reproducible leg)
  right : |lag| rank-rank        -> Spearman +0.163  (the fragile leg, strongest pair)

Definitions are copied verbatim from figS01 / the concordance scripts, so the rho printed
here must equal the value already in results/concordance.md. The script hard-fails on drift.

Drawn at the size it is placed at (one jmlr column, ~3.2in) so that the fonts are not
shrunk by \\includegraphics. The previous Figure 1 was a 19in-wide 3-panel figure scaled to
3.18in, which reduced its labels to about 1.7pt and made them unreadable.

Input : results/multivelo_genes.csv, results/multivelovae_genes.csv
Output: figures/fig_ml4h_cross_method.png   (image is gitignored, only this script is tracked)

Run: python figures/fig_ml4h_cross_method.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import rankdata, spearmanr

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
GREEN, RED = "#55A868", "#C44E52"

# results/concordance.md 3.6 에 기록된 값. 어긋나면 멈춘다.
EXPECT_ALPHA = 0.882
EXPECT_LAG = 0.163
TOL = 0.0015


def load(name: str) -> pd.DataFrame:
    d = pd.read_csv(RES / name, index_col=0)
    if "fit_likelihood" in d.columns:
        d = d[d["fit_likelihood"].notna()]
    return d[~d.index.duplicated()]


def check(computed: float, reported: float, what: str) -> None:
    if abs(computed - reported) > TOL:
        sys.exit(f"MISMATCH {what}: recomputed {computed:+.4f} vs results/*.md {reported:+.4f}")
    print(f"  [ok ] {what}: rho={computed:+.3f} matches results/*.md {reported:+.3f}")


mv = load("multivelo_genes.csv")
vae = load("multivelovae_genes.csv")
sh = mv.index.intersection(vae.index)
print(f"HSPC shared n={len(sh)}")

a1 = mv.loc[sh, "fit_alpha"].astype(float)
a2 = vae.loc[sh, "vae_alpha"].astype(float)
r_a = float(spearmanr(a1, a2).statistic)
check(r_a, EXPECT_ALPHA, "alpha MVxVAE")

l1 = (mv.loc[sh, "fit_t_sw2"].astype(float) - mv.loc[sh, "fit_t_sw1"].astype(float)).abs()
l2 = (1.0 / vae.loc[sh, "vae_alpha_c"].astype(float).clip(1e-6)
      - 1.0 / vae.loc[sh, "vae_alpha"].astype(float).clip(1e-6)).abs()
r_l = float(spearmanr(l1, l2).statistic)
check(r_l, EXPECT_LAG, "|lag| MVxVAE")

# 배치 크기 그대로 그린다(jmlr 한 컬럼 = 3.19in). p4 여유가 21pt뿐이라 높이는 1.2in 이내.
FS = 6.0
plt.rcParams.update({
    "font.size": FS, "axes.titlesize": FS, "axes.labelsize": FS - 0.3,
    "xtick.labelsize": FS - 1, "ytick.labelsize": FS - 1,
})
fig, ax = plt.subplots(1, 2, figsize=(3.19, 0.88))

# 제목을 한 줄로, y축 이름은 왼쪽에만. 세로 공간이 본문 4페이지 예산에 직접 걸린다.
for j, (a, (x, y, rho, color, name)) in enumerate(zip(ax, [
    (a1, a2, r_a, GREEN, "rate $\\alpha$"),
    (l1, l2, r_l, RED, "lag"),
])):
    a.scatter(rankdata(x), rankdata(y), s=1.4, alpha=0.40, color=color, linewidths=0)
    a.set_title(f"{name}: Spearman {rho:+.3f}", fontsize=FS, pad=1.8)
    a.set_xlabel("MultiVelo rank", labelpad=1.2)
    if j == 0:
        a.set_ylabel("MultiVeloVAE rank", labelpad=1.2)
    a.set_xticks([]); a.set_yticks([])
    a.spines[["top", "right"]].set_visible(False)
    for s in a.spines.values():
        s.set_linewidth(0.5)

fig.tight_layout(pad=0.16, w_pad=0.8)
out = Path(__file__).resolve().parent / "fig_ml4h_cross_method.png"
fig.savefig(out, dpi=600, bbox_inches="tight")
print(f"saved {out.name}  n={len(sh)}  alpha {r_a:+.3f}  |lag| {r_l:+.3f}")
