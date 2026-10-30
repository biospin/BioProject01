"""Build the BIOINFO/GIW ISCB-Asia 2026 oral talk (submission 241) from slide-plan.json.

Titles and speaker notes come from slide-plan.json (written by make_plan.py). Numbers drawn
natively on slides are copied from the verified sources listed in evidence-map.json; each block
below names its source next to the values.
"""
import json
import shutil
import sys
from pathlib import Path

SKILL_DIR = Path.home() / ".claude/skills/academic-conference-presentation"
PROJECT_DIR = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(SKILL_DIR / "scripts"))
from pptx_helpers import (new_deck, add_slide, add_text, add_rich_text, add_rect, add_picture_contain,  # noqa: E402
                          set_notes, save_deck, style_table, set_run_font, color)
from pptx.util import Inches, Pt  # noqa: E402
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR  # noqa: E402
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR  # noqa: E402
from pptx.oxml.xmlchemy import OxmlElement  # noqa: E402

theme = json.loads((PROJECT_DIR / "theme.json").read_text(encoding="utf-8"))
plan = json.loads((PROJECT_DIR / "slide-plan.json").read_text(encoding="utf-8"))
T = theme["tokens"]
TY = theme["typography"]
W, H, M = 13.333333, 7.5, theme["canvas"]["margin_in"]
CW = W - 2 * M
FIGDIR = PROJECT_DIR.parents[2] / "figures"
ASSETS = PROJECT_DIR / "assets"
OK, PARTIAL, BAD, GREY = "#1E7B34", "#B26B00", "#B42318", "#596579"
SOFT_BAD = "#FBEAE8"

plan_by_id = {s["id"]: s for s in plan["slides"]}
notes = []
prs = new_deck(theme)


def asset(name):
    ASSETS.mkdir(exist_ok=True)
    dst = ASSETS / name
    shutil.copy2(FIGDIR / name, dst)
    return dst


def notes_for(slide, sid):
    p = plan_by_id[sid]
    n = p["notes"]
    notes.append(set_notes(slide, slide_id=sid, title=p["title"], objective=n["objective"],
                           explanation=n["explanation"], cue=n["visual_cue"], transition=n["transition"],
                           seconds=p["estimated_seconds"], source=n["source_and_caveats"],
                           backup=p["main_or_backup"] == "backup", language="en"))


def slide_for(sid, number, citation=""):
    s = add_slide(prs, theme, plan_by_id[sid]["title"], number=number, citation=citation)
    if plan_by_id[sid]["main_or_backup"] == "backup":
        s._element.set("show", "0")
    return s


def txt(slide, text, x, y, w, h, size=None, bold=False, fill=None, align=PP_ALIGN.LEFT,
        vertical=MSO_ANCHOR.TOP, name="body"):
    return add_text(slide, text, x, y, w, h, theme, size=size or TY["body_pt"], bold=bold,
                    fill=fill, align=align, vertical=vertical, name=name)


def rich(slide, runs, x, y, w, h, size=None, align=PP_ALIGN.LEFT, name="body"):
    box = add_rich_text(slide, runs, x, y, w, h, theme, size=size, name=name)
    box.text_frame.paragraphs[0].alignment = align
    return box


def arrow(slide, x1, y1, x2, y2, col=None, width=2.25):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = color(col or T["muted_text"])
    c.line.width = Pt(width)
    ln = c.line._get_or_add_ln()
    from pptx.oxml.ns import qn
    from lxml import etree
    tail = etree.SubElement(ln, qn("a:tailEnd"))
    tail.set("type", "triangle")
    return c


def no_shadow(shp):
    sppr = shp._element.spPr
    if sppr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst') is None:
        sppr.append(OxmlElement('a:effectLst'))
    style = shp._element.find('{http://schemas.openxmlformats.org/presentationml/2006/main}style')
    if style is not None:
        eff = style.find('{http://schemas.openxmlformats.org/drawingml/2006/main}effectRef')
        if eff is not None:
            eff.set('idx', '0')
    return shp


def rounded(slide, x, y, w, h, fill, line=None, name="box"):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.name = name
    shp.adjustments[0] = 0.12
    shp.fill.solid()
    shp.fill.fore_color.rgb = color(fill)
    if line:
        shp.line.color.rgb = color(line)
        shp.line.width = Pt(1.25)
    else:
        shp.line.fill.background()
    sppr = shp._element.spPr
    if sppr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst') is None:
        sppr.append(OxmlElement('a:effectLst'))
    style = shp._element.find('{http://schemas.openxmlformats.org/presentationml/2006/main}style')
    if style is not None:
        eff = style.find('{http://schemas.openxmlformats.org/drawingml/2006/main}effectRef')
        if eff is not None:
            eff.set('idx', '0')
    return shp


def table(slide, rows, x, y, w, h, col_w, size=17, header_fill=None, first_bold=True, left_cols=(0,)):
    nr, nc = len(rows), len(rows[0])
    gt = slide.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(w), Inches(h))
    gt.name = "table"
    tb = gt.table
    for j, cw in enumerate(col_w):
        tb.columns[j].width = Inches(cw)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = tb.cell(i, j)
            cell.margin_left = cell.margin_right = Inches(0.08)
            cell.margin_top = cell.margin_bottom = Inches(0.04)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = cell.text_frame
            tf.word_wrap = True
            parts = val if isinstance(val, list) else [(val, {})]
            p = tf.paragraphs[0]
            for k, (t, st) in enumerate(parts):
                if st.get("newline") and k:
                    p = tf.add_paragraph()
                r = p.add_run()
                r.text = t
                r.font.size = Pt(st.get("size", size))
                r.font.bold = st.get("bold", i == 0 or (first_bold and j == 0))
                r.font.color.rgb = color(st.get("fill", T["on_primary"] if i == 0 else T["text"]))
                set_run_font(r, TY["family"], TY["east_asian_family"], TY["language"])
            for par in tf.paragraphs:
                par.alignment = PP_ALIGN.LEFT if j in left_cols else PP_ALIGN.CENTER
            cell.fill.solid()
            cell.fill.fore_color.rgb = color(header_fill or T["primary"]) if i == 0 else \
                color(T["surface"] if i % 2 == 0 else T["background"])
    return tb


def v(main, ci=None, fill=None, bold=False, size=18):
    """Cell content: main value plus an optional smaller CI line."""
    out = [(main, {"size": size, "bold": bold, **({"fill": fill} if fill else {})})]
    if ci:
        out.append((ci, {"size": 13, "newline": True, "bold": False, "fill": T["muted_text"]}))
    return out


# ---------------------------------------------------------------- S00 cover
s = prs.slides.add_slide(next(l for l in prs.slide_layouts if l.name == "Blank"))
s.background.fill.solid()
s.background.fill.fore_color.rgb = color(T["background"])
add_rect(s, 0, 0, W, 0.16, T["primary"], name="top-band")
txt(s, "BIOINFO/GIW ISCB-Asia 2026  ·  Oral presentation, submission 241", M, 0.62, CW, 0.4, size=18,
    fill=T["primary_ink"], bold=True, name="venue")
txt(s, plan_by_id["S00"]["title"], M, 1.25, CW, 1.9, size=40, bold=True, name="title")
rich(s, [{"text": "Ka-Kyung Kim", "bold": True}, {"text": "¹ ", "bold": True},
         {"text": "(presenting),  Jaemyun Lyu²˒³,  Geongyu Lee¹˒⁴,  Sejin Park⁵,  Yong Gi Ji⁶"}],
     M, 3.55, CW, 0.55, size=22, name="authors")
txt(s, "¹ Pseudo Lab, Seoul   ² R&D Center, Genolution Inc., Seoul   ³ Laboratory of RNA Cell Biology, Department of "
       "Bioconvergence Engineering, Dankook University Graduate School, Yongin   ⁴ Omixai Co., Ltd., Seoul   ⁵ Seegene Inc., Seoul   ⁶ Qaumtum c&s, Seoul   "
       "(all Republic of Korea)", M, 4.2, CW, 0.9, size=15, fill=T["muted_text"], name="affiliations")
add_rect(s, M, 5.55, CW, 0.012, T["border"], name="rule")
txt(s, "Yonsei University, Seoul  ·  17–20 November 2026", M, 5.72, CW, 0.45, size=18, fill=T["muted_text"],
    name="date")
notes_for(s, "S00")

# ---------------------------------------------------------------- S01 question
s = slide_for("S01", 1, "Recent benchmarks score velocity at the embedding and transition level: Luo et al. 2026; "
                         "Huang et al. 2026 (preprint); Wu et al. 2026.")
top = s.content_top + 0.05
bw1 = 3.25
rounded(s, M, top, bw1, 2.45, T["surface"], T["border"])
txt(s, "10x Multiome, per cell", M + 0.2, top + 0.15, bw1 - 0.3, 0.45, size=19, bold=True)
txt(s, "unspliced RNA\nspliced RNA\nchromatin accessibility\n(ATAC)", M + 0.2, top + 0.7, bw1 - 0.3, 1.7, size=17,
    fill=T["muted_text"])
arrow(s, M + bw1 + 0.05, top + 1.22, M + bw1 + 0.5, top + 1.22)
x2 = M + bw1 + 0.55
rounded(s, x2, top, bw1, 2.45, T["surface"], T["border"])
txt(s, "Kinetic model per gene", x2 + 0.2, top + 0.15, bw1 - 0.3, 0.45, size=19, bold=True)
txt(s, "MultiVelo, MultiVeloVAE, MoFlow, CRAK-Velo; scVelo as the RNA-only floor", x2 + 0.2, top + 0.7,
    bw1 - 0.3, 1.6, size=17, fill=T["muted_text"])
arrow(s, x2 + bw1 + 0.05, top + 1.22, x2 + bw1 + 0.5, top + 1.22)
x3 = x2 + bw1 + 0.55
w3 = M + CW - x3
outs = [("α", "transcription rate"), ("γ", "degradation rate"), ("α_c", "chromatin opening rate"),
        ("lag", "chromatin-to-transcription timing")]
oy = top
for sym, desc in outs:
    rounded(s, x3, oy, w3, 0.53, T["primary_soft"])
    rich(s, [{"text": f"{sym}   ", "bold": True, "fill": T["primary_ink"]}, {"text": desc}],
         x3 + 0.15, oy + 0.07, w3 - 0.2, 0.42, size=18)
    oy += 0.64
qy = top + 2.85
add_rect(s, M, qy, 0.08, 1.45, T["primary"], name="question-bar")
txt(s, "Which of these per-gene numbers is reliable enough to use as a feature?", M + 0.3, qy, CW - 0.3, 0.9,
    size=26, bold=True)
txt(s, "Our starting case: does early chromatin priming predict when a gene responds to an epigenetic drug?",
    M + 0.3, qy + 0.98, CW - 0.3, 0.5, size=19, fill=T["muted_text"])
notes_for(s, "S01")

# ---------------------------------------------------------------- S02 four axes
s = slide_for("S02", 2)
top = s.content_top + 0.05
axes = [("1", "Cross-method reproducibility", "Do two methods on the same cells rank genes the same way? Spearman ρ, permutation test"),
        ("2", "Within-lineage ATAC shuffle", "Permute ATAC across cells inside each lineage, refit. "
                                              "Breaks each cell's chromatin–RNA pairing"),
        ("3", "External replication", "Five external multiomes, from bone marrow to mouse gastrulation; gastrulation preregistered"),
        ("4", "External anchoring", "α vs measured synthesis, γ vs measured half-life, each against transcript abundance")]
cw = (CW - 3 * 0.25) / 4
for i, (n, head, body) in enumerate(axes):
    x = M + i * (cw + 0.25)
    rounded(s, x, top, cw, 3.15, T["surface"], T["border"])
    circ = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x + 0.2), Inches(top + 0.2), Inches(0.55), Inches(0.55))
    circ.fill.solid(); circ.fill.fore_color.rgb = color(T["primary"]); circ.line.fill.background()
    no_shadow(circ)
    tf = circ.text_frame; tf.text = n
    r = tf.paragraphs[0].runs[0]; r.font.size = Pt(20); r.font.bold = True; r.font.color.rgb = color(T["on_primary"])
    set_run_font(r, TY["family"], TY["east_asian_family"], TY["language"])
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    txt(s, head, x + 0.2, top + 0.88, cw - 0.35, 0.8, size=20, bold=True)
    txt(s, body, x + 0.2, top + 1.7, cw - 0.35, 1.4, size=16, fill=T["muted_text"])
dy = top + 3.45
add_rect(s, M, dy, CW, 0.012, T["border"], name="rule")
rich(s, [{"text": "Data  ", "bold": True, "fill": T["primary_ink"]},
         {"text": "Human hematopoietic stem and progenitor cells (HSPC), 10x Multiome (GSE209878), day 0 + day 7 integrated, "
                  "21,878 cells"}], M, dy + 0.12, CW, 0.75, size=18)
rich(s, [{"text": "Arms  ", "bold": True, "fill": T["primary_ink"]},
         {"text": "scVelo (RNA-only floor), MultiVelo, MultiVeloVAE, MoFlow, CRAK-Velo, branching from one common "
                  "preprocessing"}], M, dy + 0.92, CW, 0.75, size=18)
notes_for(s, "S02")

# ---------------------------------------------------------------- S03 lag definitions
s = slide_for("S03", 3, "Li et al. 2023 (MultiVelo); Li et al. 2025 (MultiVeloVAE); Hong et al. 2025 (MoFlow); "
                        "El Kazwini et al. 2026 (CRAK-Velo).")
rows = [["Method", "What the “lag” is", "Role here"],
        ["MultiVelo", "Priming interval t_sw1: chromatin opens, transcription has not started", v("Primary", bold=True, fill=T["primary_ink"])],
        ["MultiVelo", "Coupled-on duration t_sw2 − t_sw1: chromatin open and transcription on", v("Sensitivity")],
        ["MultiVeloVAE", "Rate proxy 1/α_c − 1/α", v("Partner")],
        ["MoFlow, CRAK-Velo", "Offsets from dynamic time warping", v("Partner")],
        ["MultiVelo and MultiVeloVAE", "One identical formula, 1/α_c − 1/α, computed in both", v("Control")]]
table(s, rows, M, s.content_top + 0.05, CW, 3.9, [3.3, 6.9, 2.03], size=18, left_cols=(0, 1))
txt(s, "No two of these are the same object, so we compare every definition we can compute.",
    M, s.content_top + 4.2, CW, 0.5, size=20, bold=True, fill=T["primary_ink"])
notes_for(s, "S03")

# ---------------------------------------------------------------- S04 central figure
s = slide_for("S04", 4, "538 shared genes (537 with MoFlow). Spearman ρ, gene-bootstrap 95% CI, B = 10,000; "
                        "Δρ on the same bootstrap draw.")
add_picture_contain(s, asset("fig01_concordance_v2.png"), M, s.content_top, CW, H - s.content_top - 0.55,
                    name="fig-concordance")
notes_for(s, "S04")

# ---------------------------------------------------------------- S05 robustness rows
s = slide_for("S05", 5)
top = s.content_top + 0.1
rows5 = [("+0.72", "lower bound ≥ +0.58",
          "Resampling whole co-expression modules (10 to 100 modules) keeps the α − lag gap.",
          "coupled-on duration, 538 genes"),
         ("54.6%", "sign agreement, n = 560",
          "Methods barely agree on direction; chromatin leads in 41–49% of genes.",
          "a genome-wide “chromatin primes transcription” ordering is not supported"),
         ("+0.624", "vs α +0.949",
          "Refitting MultiVelo on 12 overlapping 70% subsamples: the coupled-on duration is moderately stable.",
          "the failure is across methods and definitions, not only fitting noise; priming interval not refit-tested")]
for i, (big, small, line, note) in enumerate(rows5):
    y = top + i * 1.45
    txt(s, big, M, y, 2.6, 0.75, size=40, bold=True, fill=T["primary_ink"])
    txt(s, small, M, y + 0.78, 2.6, 0.4, size=15, fill=T["muted_text"])
    txt(s, line, M + 2.9, y + 0.05, CW - 2.9, 0.8, size=21)
    txt(s, note, M + 2.9, y + 0.8, CW - 2.9, 0.45, size=16, fill=T["muted_text"])
    if i < 2:
        add_rect(s, M, y + 1.33, CW, 0.012, T["border"], name="rule")
notes_for(s, "S05")

# ---------------------------------------------------------------- S06 ATAC shuffle
s = slide_for("S06", 6, "MultiVelo refit after within-lineage ATAC shuffle, one realization, 538 genes; ρ CI from "
                        "10,000 gene bootstraps.")
fig_h = 3.85
add_picture_contain(s, asset("figT01_atac_shuffle_priming.png"), M, s.content_top, CW, fig_h, name="fig-shuffle")
cy = s.content_top + fig_h + 0.12
rounded(s, M, cy, CW, 1.0, T["primary_soft"])
txt(s, "Coupled-on duration: ρ 0.72.  Chromatin likelihood 0.239 → 0.237.  The shuffle keeps lineage-level chromatin, "
       "so it does not show that chromatin contributes nothing; the cell × gene velocity matrix shows a small, "
       "bounded chromatin contribution.", M + 0.2, cy + 0.06, CW - 0.4, 0.88, size=16, vertical=MSO_ANCHOR.MIDDLE)
notes_for(s, "S06")

# ---------------------------------------------------------------- S07 replication table (manuscript Table 1)
s = slide_for("S07", 7, "BMMC, bone marrow mononuclear cells. Within α: median of 3 method pairs. Lag: magnitude, coupled-on "
                        "duration vs rate proxy. One sample per system.")
hl = T["primary_ink"]
rows = [["System", "Relation", "Within α", "Within lag", "Cross α", "Cross lag"],
        ["HSPC (GSE209878)", "primary", v("+0.882"), v("+0.163", "[+0.078, +0.244]"), v("—"), v("—")],
        ["Macrophage (GSE284047)", "HSPC-derived", v("+0.865"), v("+0.074", "[+0.006, +0.143]"),
         v("+0.643", "[+0.554, +0.719]"), v("+0.148", "[+0.027, +0.263]")],
        ["Human BMMC (GSE194122)", "same tissue", v("+0.851"), v("−0.088", "[−0.209, +0.034]"),
         v("+0.550", "[+0.368, +0.696]"), v("+0.052", "[−0.164, +0.262]")],
        ["Human fetal cortex (GSE162170)", "distant", v("N/A*"), v("−0.052*", "[−0.135, +0.029]"),
         v("+0.475", "[+0.292, +0.626]"), v("+0.185", "[−0.005, +0.369]")],
        ["Mouse gastrulation (GSE205117)", "developmental", v("+0.927", fill=hl, bold=True),
         v("−0.026", "[−0.089, +0.038]", fill=hl, bold=True), v("+0.415", "[+0.244, +0.561]", fill=hl, bold=True),
         v("+0.028", "[−0.165, +0.224]", fill=hl, bold=True)],
        ["E18 mouse brain (10x)", "cross-species", v("+0.810"), v("+0.057", "[−0.005, +0.118]"),
         v("+0.321", "[+0.158, +0.472]"), v("+0.105", "[−0.069, +0.269]")]]
tb = table(s, rows, M, s.content_top - 0.1, CW, 3.9, [4.0, 1.7, 1.3, 1.74, 1.74, 1.74], size=16)
for j in range(6):
    tb.cell(5, j).fill.solid()
    tb.cell(5, j).fill.fore_color.rgb = color(T["primary_soft"])
cy = H - 1.5
rich(s, [{"text": "Same gene pairs, α minus lag: ", "bold": True, "fill": T["primary_ink"]},
         {"text": "macrophage Δρ +0.843 [+0.773, +0.912], mouse gastrulation Δρ +0.979 [+0.916, +1.041].  "},
         {"text": "Mouse gastrulation: ", "bold": True, "fill": T["primary_ink"]},
         {"text": "6 predictions sealed before any fit (e.g. α ≥ 0.50, lag ≤ 0.15, α − lag ≥ 0.35); 6 of 6 passed. "
                  "Other systems were not preregistered. Cross-dataset α CIs overlap.  *Fetal cortex: no MultiVeloVAE fit; lag pair is MultiVelo × MoFlow."}],
     M, cy, CW, 1.0, size=14.5)
notes_for(s, "S07")

# ---------------------------------------------------------------- S08 α anchoring (manual bars with CIs)
s = slide_for("S08", 8, "K562 transient transcriptome sequencing (GSE229305), non-housekeeping genes, n = 193, 235, 251; abundance: point estimate. "
                        "Second source: Schwalb et al. 2016.")
cx, cy0, cwid, chgt = M + 0.95, s.content_top + 0.35, 6.0, 3.55
vmax = 0.5
base_y = cy0 + chgt
txt(s, "Spearman ρ with measured synthesis rate", M, s.content_top - 0.1, 7.0, 0.4, size=16, fill=T["muted_text"])
for tick in (0, 0.1, 0.2, 0.3, 0.4, 0.5):
    ty = base_y - tick / vmax * chgt
    add_rect(s, cx, ty, cwid, 0.008 if tick else 0.016, T["border"] if tick else T["muted_text"], name="grid")
    txt(s, f"{tick:.1f}", cx - 0.62, ty - 0.17, 0.5, 0.33, size=14, fill=T["muted_text"], align=PP_ALIGN.RIGHT)
bars = [("scVelo\n(RNA-only)", 0.236, 0.095, 0.368, T["primary"]),
        ("MultiVelo", 0.262, 0.133, 0.385, T["primary"]),
        ("MultiVeloVAE", 0.285, 0.165, 0.398, T["primary"]),
        ("Transcript\nabundance", 0.410, None, None, T["baseline"])]
bw, gap = 0.95, (cwid - 4 * 0.95) / 4
for i, (lab, val, lo, hi, col) in enumerate(bars):
    bx = cx + gap / 2 + i * (bw + gap)
    bh = val / vmax * chgt
    add_rect(s, bx, base_y - bh, bw, bh, col, name="bar")
    if lo is not None:
        ylo, yhi = base_y - lo / vmax * chgt, base_y - hi / vmax * chgt
        add_rect(s, bx + bw / 2 - 0.012, yhi, 0.024, ylo - yhi, T["text"], name="ci")
        add_rect(s, bx + bw / 2 - 0.12, yhi - 0.01, 0.24, 0.024, T["text"], name="ci-cap")
        add_rect(s, bx + bw / 2 - 0.12, ylo - 0.01, 0.24, 0.024, T["text"], name="ci-cap")
        label_y = yhi - 0.42
    else:
        label_y = base_y - bh - 0.42
    txt(s, f"+{val:.3f}", bx - 0.2, label_y, bw + 0.4, 0.36, size=17, bold=True, align=PP_ALIGN.CENTER)
    txt(s, lab, bx - 0.3, base_y + 0.08, bw + 0.6, 0.65, size=14.5, align=PP_ALIGN.CENTER)
txt(s, "fitted α", cx + gap / 2, base_y + 0.72, 3 * bw + 2 * gap, 0.35, size=14, fill=T["primary_ink"],
    align=PP_ALIGN.CENTER)
rx = M + 7.55
rw = CW - 7.55
items = [("Second synthesis source", "Null: ρ −0.05 to −0.01", BAD),
         ("α agreement beyond abundance", "MultiVelo × MultiVeloVAE +0.882 → +0.715 [+0.659, +0.765] after removing "
                                          "mean expression; lag (coupled-on) +0.182", OK),
         ("Kinetic accuracy of that component", "Not shown; it may come from the shared unspliced and spliced counts", PARTIAL)]
yy = s.content_top
for head, body, col in items:
    add_rect(s, rx, yy + 0.05, 0.07, 1.05, col, name="marker")
    txt(s, head, rx + 0.22, yy, rw - 0.22, 0.4, size=18, bold=True)
    txt(s, body, rx + 0.22, yy + 0.42, rw - 0.22, 0.85, size=15.5, fill=T["muted_text"])
    yy += 1.42
notes_for(s, "S08")

# ---------------------------------------------------------------- S09 γ table
s = slide_for("S09", 9, "Spearman ρ, fitted γ vs measured degradation rate, non-housekeeping genes, 95% CI. "
                        "MOLM13 half-lives: RNADecayCafe.")
rows = [["Method (γ)", "K562", "THP1", "MOLM13 (uncensored)"],
        ["scVelo, RNA-only", v("−0.118", "[−0.320, +0.091]"), v("−0.167", "[−0.324, +0.002]"),
         v("−0.224", "[−0.359, −0.085]  reversed", fill=BAD, bold=True)],
        ["MultiVelo", v("+0.053", "[−0.147, +0.247]"), v("+0.028", "[−0.127, +0.183]"), v("−0.003", "[−0.136, +0.134]")],
        ["MultiVeloVAE", v("−0.011", "[−0.198, +0.175]"), v("+0.120", "[−0.033, +0.271]"),
         v("+0.164", "[+0.028, +0.291]  weak", fill=OK, bold=True)]]
tb = table(s, rows, M, s.content_top + 0.05, CW, 3.0, [3.2, 2.8, 2.8, 3.43], size=18)
tb.cell(1, 3).fill.solid(); tb.cell(1, 3).fill.fore_color.rgb = color(SOFT_BAD)
txt(s, "1 of 9 method × cell-line pairs recovers γ, weakly.", M, s.content_top + 3.3, CW, 0.5, size=21,
    bold=True, fill=T["primary_ink"])
txt(s, "Cross-method γ agreement in HSPC: ρ ≈ −0.11.", M, s.content_top + 3.85, CW, 0.5, size=21, bold=True,
    fill=T["primary_ink"])
txt(s, "Positive ρ means recovery. The reversal belongs to the RNA-only scVelo γ, not to MultiVelo.",
    M, s.content_top + 4.45, CW, 0.45, size=16, fill=T["muted_text"])
notes_for(s, "S09")

# ---------------------------------------------------------------- S10 reliability map
s = slide_for("S10", 10)
add_picture_contain(s, asset("fig07_reliability_map_v2.png"), M, s.content_top - 0.1, CW, H - s.content_top - 0.35,
                    name="fig-map")
notes_for(s, "S10")

# ---------------------------------------------------------------- S11 routing rule
s = slide_for("S11", 11, "Leave-one-lineage-out across six HSPC lineages, 472 genes; Spearman ρ between predicted and fitted values; gain = difference in ρ.")
steps = [("1", "Enter transcript abundance first."),
         ("2", "Add α only as its abundance-orthogonal component; keep it only if held-out performance improves."),
         ("3", "Do not consume a single-method lag, its sign, or γ without an orthogonal measurement.")]
yy = s.content_top + 0.05
for n, line in steps:
    circ = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(M), Inches(yy + 0.05), Inches(0.55), Inches(0.55))
    circ.fill.solid(); circ.fill.fore_color.rgb = color(T["primary"]); circ.line.fill.background()
    no_shadow(circ)
    tf = circ.text_frame; tf.text = n
    r = tf.paragraphs[0].runs[0]; r.font.size = Pt(20); r.font.bold = True; r.font.color.rgb = color(T["on_primary"])
    set_run_font(r, TY["family"], TY["east_asian_family"], TY["language"])
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    txt(s, line, M + 0.8, yy, 6.4, 1.3, size=21)
    yy += {"1": 0.95, "2": 1.6, "3": 1.3}[n]
rx, rw = M + 7.6, CW - 7.6
rounded(s, rx, s.content_top, rw, 4.25, T["surface"], T["border"])
txt(s, "Held-out lineages", rx + 0.25, s.content_top + 0.15, rw - 0.5, 0.4, size=18, bold=True)
ev = [("Predicting α from", ""), ("abundance alone", "+0.724"), ("day-0 ATAC alone", "+0.309"),
      ("abundance + ATAC", "+0.708"), ("gain from ATAC", "−0.016"), ("Predicting the lag (coupled-on) from", ""), ("day-0 ATAC", "+0.049")]
yy = s.content_top + 0.7
for lab, val in ev:
    if not val:
        txt(s, lab, rx + 0.25, yy, rw - 0.5, 0.38, size=15, fill=T["muted_text"])
        yy += 0.42
        continue
    txt(s, lab, rx + 0.4, yy, rw - 1.5, 0.4, size=17)
    txt(s, val, rx + rw - 1.15, yy, 0.95, 0.4, size=18, bold=True, fill=T["primary_ink"], align=PP_ALIGN.RIGHT)
    yy += 0.5
notes_for(s, "S11")

# ---------------------------------------------------------------- S12 take-home
s = slide_for("S12", 12)
pts = ["Reliability of a velocity output is testable, on four axes.",
       "Among per-gene outputs only α reproduces, also beyond abundance; its kinetic accuracy is still open.",
       "The lag does not reproduce under any definition tested: treat it as a model output that needs orthogonal "
       "validation, not as a regulatory clock."]
yy = s.content_top
for p in pts:
    add_rect(s, M, yy + 0.12, 0.08, 0.62, T["primary"], name="bullet")
    txt(s, p, M + 0.3, yy, CW - 0.3, 0.95, size=22)
    yy += 1.0
ly = yy + 0.1
rounded(s, M, ly, CW, 1.05, T["surface"], T["border"])
rich(s, [{"text": "Limits  ", "bold": True, "fill": T["primary_ink"]},
         {"text": "Pseudotime is not wall-clock time. External replications are single samples (no donor variation). "
                  "The α anchor is one of two synthesis sources, measured in K562 rather than HSPC. Within-method "
                  "stability was assessed only for MultiVelo's coupled-on duration. We audited per-gene parameters, "
                  "not trajectories."}], M + 0.2, ly + 0.08, CW - 0.4, 0.95, size=15)
txt(s, "Thanks to Pseudo Lab, a non-profit AI/ML research community, and to Sangjun Park (Yonsei University) for the "
       "initial idea. Supported by the Open Source AI·SW Developer and Community Support Program, Ministry of Science "
       "and ICT, Republic of Korea.", M, H - 0.95, CW - 0.8, 0.6, size=12.5, fill=T["muted_text"], name="acknowledgements")
notes_for(s, "S12")

# ---------------------------------------------------------------- backups
s = slide_for("B01", 13, "Lag = MultiVelo coupled-on duration. 258 genes with an interior lag profile and positive curvature "
                         "κ on both axes; nuisance parameters fixed.")
rows = [["Coordinates for the curvature κ", "Median κ_α / κ_lag", "Interquartile range", "α tighter"],
        ["ln α vs ln lag (as submitted)", v("3.53"), v("[1.92, 7.41]"), v("94.6%")],
        ["ln α vs lag as a fraction of the horizon", v("0.10"), v("[0.03, 0.22]"), v("1.9%")]]
table(s, rows, M, s.content_top + 0.05, CW, 1.9, [4.9, 2.6, 2.9, 1.83], size=18)
txt(s, "Neither coordinate system is canonical, so the claim is cross-method non-reproducibility, not strict "
       "non-identifiability.", M, s.content_top + 2.3, CW, 0.9, size=21, bold=True, fill=T["primary_ink"])
txt(s, "Lag classes among the 538 genes: 302 interior, 205 boundary-pinned, 31 degenerate. 199 of the 205 "
       "boundary-pinned lags come from induction-only fits, which reflects trajectory coverage more than "
       "non-identifiability.", M, s.content_top + 3.3, CW, 1.2, size=18)
notes_for(s, "B01")

s = slide_for("B02", 14, "MultiVelo lag = coupled-on duration (t_sw2 − t_sw1). 537 genes shared by the three methods; 95% CI, B = 10,000.")
rows = [["Pair (lag magnitude unless noted)", "Spearman ρ", "Δρ = ρ_α − ρ_lag"],
        ["MultiVelo × MultiVeloVAE", v("+0.165", "[+0.080, +0.248]"), v("+0.717", "[+0.635, +0.799]")],
        ["MultiVelo × MoFlow", v("−0.013", "[−0.097, +0.070]"), v("+0.896", "[+0.807, +0.984]")],
        ["MultiVeloVAE × MoFlow", v("−0.064", "[−0.148, +0.023]"), v("+0.946", "[+0.855, +1.031]")],
        ["MultiVeloVAE × MoFlow, signed", v("+0.107", "[+0.022, +0.188]"), v("+0.776", "[+0.692, +0.861]")],
        ["α, MultiVelo × MultiVeloVAE", v("+0.882", "[+0.854, +0.905]", bold=True, fill=T["primary_ink"]), v("—")]]
table(s, rows, M, s.content_top + 0.05, CW, 4.3, [5.4, 3.4, 3.43], size=17)
notes_for(s, "B02")

s = slide_for("B03", 15, "Lag here: MultiVelo coupled-on duration vs MultiVeloVAE rate proxy, magnitude; the priming "
                         "interval was recomputed in HSPC only.")
rich(s, [{"text": "MultiVelo × MultiVeloVAE, α:    ", "bold": True},
         {"text": "+0.882, +0.917, +0.898, +0.906, +0.953", "fill": OK, "bold": True}],
     M, s.content_top - 0.2, CW, 0.4, size=17)
rich(s, [{"text": "MultiVelo × MultiVeloVAE, lag:  ", "bold": True},
         {"text": "+0.163, +0.074, +0.057, −0.088, −0.026", "fill": BAD, "bold": True},
         {"text": "     (HSPC, macrophage, E18 mouse brain, human BMMC, mouse gastrulation)", "fill": T["muted_text"], "size": 14}],
     M, s.content_top + 0.25, CW, 0.4, size=17)
add_picture_contain(s, ASSETS / "figS01_per_dataset_concordance_crop.png", M, s.content_top + 0.75, CW,
                    H - s.content_top - 1.2, name="fig-per-dataset")
notes_for(s, "B03")

s = slide_for("B04", 16, "Preregistration sealed 2026-07-12, before any fit on GSE205117; the pass lines are the sealed "
                         "thresholds, not HSPC observations.")
rows = [["#", "Prediction", "Sealed threshold", "Observed", "Result"],
        ["1", "Within-dataset α reproduces", "ρ ≥ 0.50", v("+0.927 (median of 3 pairs)"), v("Pass", fill=OK, bold=True)],
        ["2", "Within-dataset lag does not", "ρ ≤ 0.15", v("−0.026"), v("Pass", fill=OK, bold=True)],
        ["3", "α over lag", "Δρ ≥ 0.35", v("+0.979"), v("Pass", fill=OK, bold=True)],
        ["4", "Cross-dataset HSPC ↔ gastrulation", "α > +0.20 and α > lag", v("+0.415 vs +0.028"), v("Pass", fill=OK, bold=True)],
        ["5", "Per-gene disagreement larger for lag (MV × MoFlow) than α (MV × VAE)", "lag > α", v("0.294 vs 0.052"), v("Pass", fill=OK, bold=True)],
        ["6", "Lag fragile even at maximal priming", "2 and 3 hold", v("both hold"), v("Pass", fill=OK, bold=True)]]
table(s, rows, M, s.content_top + 0.05, CW, 4.4, [0.55, 4.2, 2.6, 3.6, 1.28], size=16, left_cols=(0, 1))
notes_for(s, "B04")

save_deck(prs, PROJECT_DIR / "GIW2026_oral241_velocity_reliability_map.pptx", notes, overwrite=True)
print(f"saved {len(prs.slides)} slides")
