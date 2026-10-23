#!/usr/bin/env python3
"""fig07 v2 — Figure 2 of the GIW long abstract — velocity-output reliability map, 3 columns.

Replaces the 4-column fig07 (cross-method reproducible / chromatin-causal /
baseline-predictable / measurement-corroborated) with the structure promised in the
ML4H Submission 294 rebuttal (2026-10-13):

    Reproducibility evidence | Accuracy evidence | Routing decision

Reproducibility = do two methods, run on the same cells, rank genes alike.
Accuracy        = has the value been compared with a laboratory measurement of the same rate.
Routing         = what a downstream model should do with the value.

The "chromatin-causal" column is dropped: the rebuttal narrowed the within-lineage ATAC
shuffle to "cell-level pairing destroyed", which is not a causal test of chromatin.

Every number drawn in a cell is guarded against a source text (assert token-in-source):
  R  = results/post_review_robustness.gen.md                     (machine output, R1–R5)
  A  = manuscript/CONF_LONGABSTRACT_GIW2026_BIOP01.md            (numbers carried over from draft_v2)
A failed guard stops the script instead of drawing an unsourced number.

Status colours (good / warning / critical) never carry meaning alone: every cell has a
glyph and a word label, so the figure reads in greyscale and under CVD.

Run:
  conda run -n scv-preprocess python pipeline/hspc-velocity-benchmark/figures/fig07_reliability_map_v2.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Patch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SRC = {
    "R": (ROOT / "results" / "post_review_robustness.gen.md").read_text(encoding="utf-8"),
    "A": (ROOT / "manuscript" / "CONF_LONGABSTRACT_GIW2026_BIOP01.md").read_text(encoding="utf-8"),
}

# ----------------------------------------------------------------------------------
# Categories. Status palette (fixed); label ink per the palette's label-on-fill rule.
# ----------------------------------------------------------------------------------
CAT = {
    "yes":  dict(fc="#0ca30c", tc="#ffffff", glyph="✓"),   # supported / use
    "part": dict(fc="#fab219", tc="#0b0b0b", glyph="~"),   # partial, caveat, population-only
    "no":   dict(fc="#d03b3b", tc="#ffffff", glyph="✗"),   # not supported / do not use
    "na":   dict(fc="#e1e0d9", tc="#52514e", glyph="–"),   # not tested / reference
}
SURFACE, INK, INK2 = "#fcfcfb", "#0b0b0b", "#52514e"

COLS = ["Reproducibility evidence", "Accuracy evidence", "Routing decision"]

# (row label, [(category, headline, detail, [(source, guard-token), ...]) x 3])
ROWS = [
    ("Transcript abundance\n(reference, not a velocity output)", [
        ("na", "Reference baseline", "not a velocity output", []),
        ("part", "Partial", "vs synthesis +0.410\n(TT-seq source 1)", [("A", "+0.410")]),
        ("yes", "Enter first", "baseline for every\nrate feature", []),
    ]),
    ("Transcription rate α", [
        ("yes", "Supported", "MV×VAE +0.882\nbeyond abundance +0.715", [("R", "+0.882"), ("R", "+0.715")]),
        ("part", "Partial", "+0.262 vs synthesis, 1 of 2 sources\nabundance +0.410 ≥ α", [("A", "+0.262"), ("A", "+0.410")]),
        ("part", "Use beside abundance", "add abundance-orthogonal part;\nkeep only if held-out gain", []),
    ]),
    ("Population directional\nbalance (~50/50)", [
        ("part", "Population-level only", "chromatin-leads 41–49%", [("A", "41–49%")]),
        ("na", "Not tested", "no measured reference", []),
        ("part", "Population statement", "not a per-gene feature", []),
    ]),
    ("Canonical priming-\nmarker direction", [
        ("part", "Population-level only", "direction agrees across methods", [("A", "direction agreement")]),
        ("na", "Not tested", "correlational only", [("A", "correlational")]),
        ("part", "Population statement", "not causal", []),
    ]),
    ("Chromatin-opening rate α_c", [
        ("no", "Not supported", "MV×VAE +0.291\nbeyond abundance +0.264", [("R", "+0.291"), ("R", "+0.264")]),
        ("na", "Not tested", "no measured reference", []),
        ("no", "Do not use", "without an independent\nmeasurement", []),
    ]),
    ("Degradation rate γ", [
        ("no", "Not supported", "cross-method ρ≈−0.11", [("A", "ρ≈−0.11")]),
        ("no", "Not supported", "half-life not recovered;\nscVelo reversed −0.224", [("A", "−0.224")]),
        ("no", "Do not use", "without an independent\nmeasurement", []),
    ]),
    ("Per-gene lag magnitude\n(every definition tested)", [
        ("no", "Not supported", "priming +0.364 · coupled-on +0.163\nsame formula −0.009 · vs MoFlow +0.038",
         [("R", "+0.364"), ("R", "+0.163"), ("R", "-0.009"), ("R", "+0.038")]),
        ("na", "Not tested", "no measured lag", []),
        ("no", "Do not use", "value depends on method\nand definition", []),
    ]),
    ("Per-gene lag sign /\nabsolute timing", [
        ("no", "Not supported", "sign agreement 54.6% (n=560)", [("A", "54.6%"), ("A", "n=560")]),
        ("na", "Not tested", "pseudotime ≠ wall-clock", [("A", "pseudotime is not wall-clock")]),
        ("no", "Do not use", "without an independent\nmeasurement", []),
    ]),
]

# Guards: every displayed number must exist in its source text. The ASCII hyphen in the
# R table is mapped to the typographic minus used in the figure.
for label, cells in ROWS:
    assert len(cells) == len(COLS), label
    for _cat, _head, detail, guards in cells:
        for src, token in guards:
            assert token in SRC[src], f"GUARD FAILED {label!r}: {token!r} not in source {src}"
            if token[0] in "+-−0123456789n":   # numeric tokens must be drawn verbatim
                shown = token.replace("-0.", "−0.")
                assert shown in detail, f"guarded token {token!r} not drawn in {label!r}: {detail!r}"

# ----------------------------------------------------------------------------------
# Render.
# ----------------------------------------------------------------------------------
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8})
nrows, ncols = len(ROWS), len(COLS)
LABEL_W = 1.05            # row-label gutter, in cell-width units
GAP = 0.035               # 2px-ish surface gap between fills

fig, ax = plt.subplots(figsize=(10.5, 6.6))
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)
ax.set_xlim(-LABEL_W, ncols)
ax.set_ylim(-0.05, nrows + 0.55)
ax.set_axis_off()

for i, (label, cells) in enumerate(ROWS):
    y = nrows - 1 - i
    for j, (cat, head, detail, _g) in enumerate(cells):
        st = CAT[cat]
        ax.add_patch(FancyBboxPatch((j + GAP, y + GAP), 1 - 2 * GAP, 1 - 2 * GAP,
                                    boxstyle="round,pad=0,rounding_size=0.04",
                                    facecolor=st["fc"], edgecolor="none", zorder=1))
        ax.text(j + 0.5, y + 0.66, f"{st['glyph']}  {head}", ha="center", va="center",
                fontsize=8.6, fontweight="bold", color=st["tc"], zorder=2)
        ax.text(j + 0.5, y + 0.33, detail, ha="center", va="center",
                fontsize=6.9, color=st["tc"], linespacing=1.25, zorder=2)
    ax.text(-0.06, y + 0.5, label, ha="right", va="center", fontsize=8.3,
            color=INK2 if i == 0 else INK, style="italic" if i == 0 else "normal",
            linespacing=1.2)

# rule under the reference row
ax.plot([-LABEL_W, ncols], [nrows - 1, nrows - 1], color="#c3c2b7", lw=1.0, ls=(0, (4, 3)))

for j, c in enumerate(COLS):
    ax.text(j + 0.5, nrows + 0.12, c, ha="center", va="bottom", fontsize=9.6,
            fontweight="bold", color=INK)

handles = [
    Patch(facecolor=CAT["yes"]["fc"], label="✓ supported / use"),
    Patch(facecolor=CAT["part"]["fc"], label="~ partial, caveat or population-only"),
    Patch(facecolor=CAT["no"]["fc"], label="✗ not supported / do not use"),
    Patch(facecolor=CAT["na"]["fc"], label="– not tested / reference"),
]
leg = ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, 0.0), ncol=4,
                frameon=False, fontsize=7.6, handlelength=1.2, columnspacing=1.4)
for t in leg.get_texts():
    t.set_color(INK2)

fig.text(0.5, 0.012,
         "Reproducibility: rank agreement of two methods on the same cells (MultiVelo × MultiVeloVAE, 538 genes "
         "unless noted). Accuracy: comparison with a measured rate (K562 TT-seq synthesis; SLAM-seq half-life), "
         "not HSPC.\nWithin one method the lag is moderately stable (MultiVelo refits, coupled-on +0.624), so "
         "“not supported” means not reproducible across methods and definitions.",
         ha="center", va="bottom", fontsize=6.6, color=INK2, linespacing=1.35)
assert "+0.624" in SRC["A"]

fig.subplots_adjust(left=0.01, right=0.99, top=0.98, bottom=0.13)
out = HERE / "fig07_reliability_map_v2.png"
fig.savefig(out, dpi=300, facecolor=SURFACE)
print(f"saved {out}  rows={nrows} cols={ncols}  (all guards passed)")
