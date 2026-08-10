#!/usr/bin/env python3
"""fig07 — Velocity-output reliability decision map (main; new).

Visual form of draft_v2.md Table 2 ("Velocity-output reliability decision map",
L148-161) and the Fig. 7 legend (L301). Rows = velocity outputs; columns = the four
reliability axes named in the legend:
    cross-method reproducible / chromatin-causal / baseline-predictable / measurement-corroborated.

SINGLE SOURCE OF TRUTH: this script *parses* Table 2 out of draft_v2.md (read-only) and
guards every displayed number against the parsed source cell (assert token-in-source), so a
change to Table 2 fails loudly here instead of silently drifting. No number is invented.

Table 2 has its own four columns (cross-method reproducibility | external measurement anchor |
reliability | recommended action). Fig. 7's four axes are a RE-ASSIGNMENT of those cells; the
provenance of every plotted cell -> Table 2 (row, source-column) is recorded in CELLS below.
Axes with no basis in Table 2 for a given row are drawn grey ("not scored in Table 2"), NOT
invented. In particular the per-gene lag's chromatin-causal control lives in Fig. 2 (ATAC
shuffle, MW p=0.20), which is outside Table 2 -> grey here, flagged in the caption.

Honest-colour rules (task): alpha is "Reliable, but largely expression" (Table 2) -> hatched
green, never pure green. Amber ("population / correlation-only") is reserved for the two
population-level rows' cross-method cells. The null causal test for markers (p=0.58) fails the
chromatin-causal axis -> red on that axis only (the marker DIRECTION stays amber/correlational).

Input : ../manuscript/draft_v2.md  (Table 2 block, read-only)
Output: figures/fig07_reliability_map.png  (300 dpi; image gitignored, only this .py tracked)
Note  : 300 dpi per task brief (fig01/fig05 use 130; this deliberately overrides).

Run:
  conda run -n scv-preprocess python pipeline/hspc-velocity-benchmark/figures/fig07_reliability_map.py
"""
from __future__ import annotations
import re
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "manuscript" / "draft_v2.md"

# ----------------------------------------------------------------------------------
# 1. Parse Table 2 from draft_v2.md (read-only). Guard against the row-7 literal pipes
#    in "|rho|<=0.08" by masking "|ρ|" before the pipe-split, then asserting 5 fields.
# ----------------------------------------------------------------------------------
PIPE_SENTINEL = ""  # private-use char, cannot occur in the markdown


def parse_table2() -> dict[str, list[str]]:
    text = DRAFT.read_text(encoding="utf-8")
    block = text.split("### Table 2.")[1].split("*Inventory tables")[0]
    rows: dict[str, list[str]] = {}
    for raw in block.splitlines():
        line = raw.strip()
        if not (line.startswith("|") and line.endswith("|")):
            continue
        if set(line) <= set("|-: "):       # separator row |---|---|
            continue
        masked = line.replace("|ρ|", PIPE_SENTINEL + "ρ" + PIPE_SENTINEL)
        cells = [c.strip().replace(PIPE_SENTINEL, "|") for c in masked.strip("|").split("|")]
        assert len(cells) == 5, f"Table 2 row did not yield 5 fields: {cells!r}"
        key = cells[0]
        if key.lower().startswith("velocity output"):   # header row
            continue
        rows[key] = cells  # [output, cross-method, external-anchor, reliability, action]
    assert len(rows) == 8, f"expected 8 Table 2 data rows, got {len(rows)}"
    return rows


T2 = parse_table2()
# Canonical Table-2 row keys (as they appear in draft_v2.md), top-to-bottom for the figure.
R_ABUND = "*Steady-state abundance (reference, not a velocity output)*"
R_ALPHA = "Transcription rate α"
R_POP = "Population directional balance (~50/50)"
R_MARK = "Canonical priming-marker direction"
R_AC = "Chromatin-opening rate α_c"
R_GAMMA = "Degradation rate γ"
R_LAGMAG = "Per-gene lag magnitude"
R_LAGSGN = "Per-gene lag sign / absolute timing"
for k in (R_ABUND, R_ALPHA, R_POP, R_MARK, R_AC, R_GAMMA, R_LAGMAG, R_LAGSGN):
    assert k in T2, f"row key not found in parsed Table 2: {k!r}"

# Table-2 source-column indices within each parsed row.
C_CROSS, C_EXT, C_REL = 1, 2, 3

# ----------------------------------------------------------------------------------
# 2. Categories -> colours (task legend: Reliable / population-correlation / Unreliable / N/A).
# ----------------------------------------------------------------------------------
GREEN, AMBER, RED, GREY = "#2E7D32", "#E8A33D", "#C44E52", "#D9D9D9"
CAT = {
    "reliable":  dict(fc=GREEN, hatch=None, tc="white"),
    "caveat":    dict(fc=GREEN, hatch="////", tc="white"),   # reliable, abundance caveat (alpha)
    "pop":       dict(fc=AMBER, hatch=None, tc="#3a2a00"),    # population / correlation-only
    "unreliable":dict(fc=RED,   hatch=None, tc="white"),
    "na":        dict(fc=GREY,  hatch=None, tc="#6b6b6b"),    # not scored in Table 2
}

ROW_ORDER = [R_ABUND, R_ALPHA, R_POP, R_MARK, R_AC, R_GAMMA, R_LAGMAG, R_LAGSGN]
ROW_LABELS = {
    R_ABUND: "Steady-state abundance\n(reference, not a velocity output)",
    R_ALPHA: "Transcription rate α",
    R_POP:   "Population directional\nbalance (~50/50)",
    R_MARK:  "Canonical priming-\nmarker direction",
    R_AC:    "Chromatin-opening rate α_c",
    R_GAMMA: "Degradation rate γ",
    R_LAGMAG:"Per-gene lag magnitude",
    R_LAGSGN:"Per-gene lag sign /\nabsolute timing",
}
COLS = ["Cross-method\nreproducible", "Chromatin-\ncausal",
        "Baseline-\npredictable", "Measurement-\ncorroborated"]

# ----------------------------------------------------------------------------------
# 3. Cells. Each = (category, short label, Table-2 source-column, guard token).
#    guard token MUST appear in T2[row][source-col]; else assert fails (no fabrication).
#    source-col = None  -> grey "not scored in Table 2" cell (no Table-2 basis for that axis).
# ----------------------------------------------------------------------------------
NA = ("na", "—", None, None)
CELLS: dict[str, list[tuple]] = {
    # row:            cross-method                              chromatin-causal                                   baseline-predictable                     measurement-corroborated
    R_ABUND:  [("na", "not method-\ndependent", C_CROSS, "Not method-dependent"), NA,                              ("na", "(is the baseline)", None, None), ("reliable", "tracks synthesis\nρ=+0.41 (≥ α)", C_EXT, "+0.41")],
    R_ALPHA:  [("caveat", "ρ=0.88\nfloor recovers", C_CROSS, "0.88"),             NA,                              ("caveat", "α↔abundance\nρ=0.81", C_REL, "0.81"), ("caveat", "+0.24–0.29\nvs abund +0.41", C_EXT, "+0.24")],
    R_POP:    [("pop", "two methods\nconverge", C_CROSS, "two methods converge"), NA,                              NA,                                      NA],
    R_MARK:   [("pop", "agrees across\nmethods", C_CROSS, "agrees across methods"), ("unreliable", "ATAC-shuffle null\np=0.58 (no causal)", C_EXT, "0.58"), NA,                                   NA],
    R_AC:     [("unreliable", "ρ=0.29", C_CROSS, "0.29"),                          NA,                              NA,                                      NA],
    R_GAMMA:  [("unreliable", "ρ≈−0.1", C_CROSS, "0.1"),                           NA,                              NA,                                      ("unreliable", "K562 3/3 null\nscVelo γ −0.224", C_EXT, "0.224")],
    R_LAGMAG: [("unreliable", "|ρ|≤0.08\n(strongest +0.163)", C_CROSS, "0.163"),   NA,                              ("unreliable", "≈chance", C_EXT, "chance"), NA],
    R_LAGSGN: [("unreliable", "54.6% (chance)\nstructurally biased", C_CROSS, "54.6"), NA,                          NA,                                      NA],
}

# Guard: every plotted number/phrase must be present in its Table-2 source cell.
for row, cells in CELLS.items():
    assert len(cells) == 4, f"{row} needs 4 axis cells"
    for cat, label, srccol, guard in cells:
        if srccol is None:
            continue
        src = T2[row][srccol]
        assert guard in src, (
            f"GUARD FAILED for row {row!r}: token {guard!r} not in Table-2 source cell {src!r}")

# ----------------------------------------------------------------------------------
# 4. Render.
# ----------------------------------------------------------------------------------
nrows, ncols = len(ROW_ORDER), len(COLS)
LABEL_L = -1.85                       # row-label gutter, kept INSIDE xlim so bbox stays tight
fig, ax = plt.subplots(figsize=(15, 8.4))
ax.set_xlim(LABEL_L, ncols)
ax.set_ylim(0, nrows)
ax.set_axis_off()

for i, row in enumerate(ROW_ORDER):
    y = nrows - 1 - i               # row 0 (abundance) at the top
    for j, (cat, label, _srccol, _guard) in enumerate(CELLS[row]):
        st = CAT[cat]
        # solid base (white border); keeps white cell text legible even for the caveat cells
        ax.add_patch(Rectangle((j, y), 1, 1, facecolor=st["fc"], edgecolor="white",
                               linewidth=2.2, zorder=1))
        if st["hatch"]:   # caveat: darker-green hatch overlay UNDER the text, not white-on-green
            ax.add_patch(Rectangle((j, y), 1, 1, facecolor="none", edgecolor="#134a1a",
                                   linewidth=0.0, hatch=st["hatch"], zorder=1.4))
        ax.text(j + 0.5, y + 0.5, label, ha="center", va="center",
                fontsize=8.2, color=st["tc"], zorder=2)
    # row label (left); abundance italic to mark it as the reference, not a velocity output
    ax.text(-0.12, y + 0.5, ROW_LABELS[row], ha="right", va="center", fontsize=9.2,
            style="italic" if row == R_ABUND else "normal",
            color="#333333" if row == R_ABUND else "black")

# horizontal rule beneath the reference (abundance) row (stays within xlim)
ax.plot([LABEL_L, ncols], [nrows - 1, nrows - 1], color="#333333", lw=1.4,
        ls=(0, (5, 3)), clip_on=False, zorder=3)

# column headers
for j, c in enumerate(COLS):
    ax.text(j + 0.5, nrows + 0.12, c, ha="center", va="bottom", fontsize=10.5, fontweight="bold")

# title + routing rule
fig.suptitle("Fig. 7  Velocity-output reliability decision map (visual form of Table 2)",
             fontsize=13.5, fontweight="bold", y=0.985)
ax.text(ncols / 2, nrows + 0.95,
        "Routing rule: trust α and rate-derived signals; treat lag, its sign, absolute timing, "
        "and γ as requiring orthogonal validation.",
        ha="center", va="bottom", fontsize=9.3, style="italic", color="#222222")

# legend
handles = [
    Patch(facecolor=GREEN, edgecolor="white", label="Reliable"),
    Patch(facecolor=GREEN, edgecolor="white", hatch="////", label="Reliable, with abundance caveat (α)"),
    Patch(facecolor=AMBER, edgecolor="white", label="Population / correlation-only"),
    Patch(facecolor=RED, edgecolor="white", label="Unreliable / fails this axis"),
    Patch(facecolor=GREY, edgecolor="white", label="Not scored in Table 2"),
]
ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.02),
          ncol=5, frameon=False, fontsize=8.3, handlelength=1.3, columnspacing=1.2)

# caption: the lag's chromatin-causal control is Fig. 2 (outside Table 2 -> grey here)
fig.text(0.5, -0.055,
         "Grey = the axis is not scored for that output in Table 2 (no basis invented). The per-gene lag's "
         "chromatin-causal control is Fig. 2 (within-lineage ATAC shuffle, MW p=0.20; per-gene ρ=0.72), "
         "outside Table 2 and shown grey here. Steady-state abundance is a reference baseline, not a velocity "
         "output: α adds no demonstrable synthesis information beyond it (abundance↔synthesis +0.41 ≥ α↔synthesis +0.26). "
         "Cells parsed from draft_v2.md Table 2 (L152–161); every number guarded against its source cell.",
         ha="center", va="top", fontsize=7.3, color="#444444", wrap=True)

fig.subplots_adjust(left=0.02, right=0.99, top=0.90, bottom=0.12)
out = Path(__file__).resolve().parent / "fig07_reliability_map.png"
fig.savefig(out, dpi=300, bbox_inches="tight")
print(f"saved {out.name}  rows={nrows} cols={ncols}  (all cell guards passed)")
