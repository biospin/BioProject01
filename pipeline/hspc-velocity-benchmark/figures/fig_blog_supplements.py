#!/usr/bin/env python3
"""블로그 03/05 삽입용 + 04 독립 하네스 개념도 3종 생성.

숫자 출처(검증됨, 하드코딩):
- fig02 cross-dataset concordance: results/concordance_e18_mouse_brain.md,
  concordance_human_brain.md, concordance_GSE194122_bmmc.md 의 "B. Cross-dataset" rank Spearman.
- fig03 novelty: 블로그 05 본문(MoFlow=우연거름/인과대조 없음, 사후보고 O; 우리=셋 다).
- fig04 harness: 블로그 04 본문(지침 SKILL.md ↔ 코드 scripts/ 분리, 사람/OpenClaw 재실행).

라벨은 영어(서버에 한글 폰트 없음 → tofu 방지). 블로그 alt-text가 한/영 병기로 보완.

실행: conda run -n scv-preprocess python pipeline/hspc-velocity-benchmark/figures/fig_blog_supplements.py
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

OUT = Path(__file__).resolve().parent
BLUE, GREEN, RED, GRAY = "#4C72B0", "#55A868", "#C44E52", "#8C8C8C"

# ─────────────────────────── fig02: cross-dataset concordance ───────────────────────────
datasets = ["E18 mouse brain", "Human brain\n(GSE162170)", "Human BMMC\n(GSE194122)"]
alpha_cross = [0.321, 0.475, 0.550]   # rate α, cross-dataset rank Spearman
lag_cross   = [0.105, 0.185, 0.052]   # chromatin→transcription lag magnitude, same

x = np.arange(len(datasets)); w = 0.36
fig, ax = plt.subplots(figsize=(7.6, 4.4))
b1 = ax.bar(x - w/2, alpha_cross, w, label="transcription rate α (robust)", color=GREEN, edgecolor="white")
b2 = ax.bar(x + w/2, lag_cross,  w, label="chromatin→transcription lag (fragile)", color=RED, edgecolor="white")
for bars in (b1, b2):
    for r in bars:
        ax.text(r.get_x()+r.get_width()/2, r.get_height()+0.012, f"{r.get_height():.2f}",
                ha="center", va="bottom", fontsize=9)
ax.axhline(0.30, color=GRAY, ls=":", lw=1)
ax.text(len(datasets)-0.5, 0.315, "|ρ|=0.30 replication mark", ha="right", va="bottom", fontsize=8, color=GRAY)
ax.set_xticks(x); ax.set_xticklabels(datasets, fontsize=9)
ax.set_ylabel("cross-dataset rank Spearman ρ"); ax.set_ylim(0, 0.62)
ax.set_title("Across tissue and species, α reproduces; chromatin→transcription lag does not\n"
             "(within-HSPC reference: α cross-method ρ=0.88, lag ρ≈0)", fontsize=10)
ax.legend(fontsize=8.5, loc="upper left"); ax.spines[["top","right"]].set_visible(False)
fig.tight_layout(); fig.savefig(OUT/"fig02_crossdataset_concordance.png", dpi=130, bbox_inches="tight")
plt.close(fig)

# ─────────────────────────── fig03: novelty comparison ───────────────────────────
rows = ["Reports partial cross-method\nlag agreement (post-hoc)",
        "Chance control\n(permutation FDR)",
        "Causal control\n(scrambled-chromatin negative)"]
moflow = [True, False, False]
ours   = [True, True, True]
fig, ax = plt.subplots(figsize=(7.2, 3.6)); ax.axis("off"); ax.set_xlim(0,1); ax.set_ylim(0,1)
cols_x = [0.60, 0.83]
ax.text(cols_x[0], 0.92, "MoFlow\n(closest prior)", ha="center", va="center", fontsize=10, fontweight="bold")
ax.text(cols_x[1], 0.92, "Ours", ha="center", va="center", fontsize=10, fontweight="bold")
for i, row in enumerate(rows):
    y = 0.72 - i*0.24
    ax.text(0.02, y, row, ha="left", va="center", fontsize=9.5)
    for cx, val in zip(cols_x, (moflow[i], ours[i])):
        ax.text(cx, y, "✓" if val else "✗", ha="center", va="center", fontsize=20,
                color=GREEN if val else RED, fontweight="bold")
ax.plot([0.0,0.95],[0.84,0.84], color=GRAY, lw=0.8)
ax.set_title("What the closest prior work established, and what we add", fontsize=10.5, loc="left")
fig.savefig(OUT/"fig03_novelty_comparison.png", dpi=130, bbox_inches="tight")
plt.close(fig)

# ─────────────────────────── fig04: harness concept (standalone) ───────────────────────────
fig, ax = plt.subplots(figsize=(7.4, 3.6)); ax.axis("off"); ax.set_xlim(0,10); ax.set_ylim(0,6)
def box(x, y, w, h, text, fc):
    ax.add_patch(FancyBboxPatch((x,y), w, h, boxstyle="round,pad=0.08,rounding_size=0.15",
                 fc=fc, ec="#333", lw=1.2))
    ax.text(x+w/2, y+h/2, text, ha="center", va="center", fontsize=9.5)
box(0.4, 3.6, 3.4, 1.5, "Instructions (WHAT)\nSKILL.md · ROUTES · dataset→task", "#DCE6F5")
box(0.4, 0.7, 3.4, 1.5, "Code (HOW)\nscripts/  (download→…→viz)", "#E7F0DE")
box(6.2, 2.15, 3.3, 1.5, "Same procedure re-run\nby Human or OpenClaw", "#F5E6DC")
ax.add_patch(FancyArrowPatch((3.8,4.35),(6.2,3.2), arrowstyle="->", mutation_scale=16, color="#333", lw=1.3))
ax.add_patch(FancyArrowPatch((3.8,1.45),(6.2,2.7), arrowstyle="->", mutation_scale=16, color="#333", lw=1.3))
ax.text(5.0, 4.15, "name dataset\n+ task", ha="center", va="center", fontsize=8, color="#555")
ax.set_title("Reproducible harness: split WHAT (instructions) from HOW (code)\n"
             "so the same procedure re-runs by name — for a person or a machine", fontsize=10)
fig.savefig(OUT/"fig04_harness_concept.png", dpi=130, bbox_inches="tight")
plt.close(fig)

for f in ("fig02_crossdataset_concordance", "fig03_novelty_comparison", "fig04_harness_concept"):
    p = OUT/f"{f}.png"
    print(f"✓ {p.name}  {p.stat().st_size//1024}KB")
