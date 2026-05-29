#!/usr/bin/env python3
"""Render <paper-id>_core.md (+ optionally lens-*, methodology-brief) into a standalone HTML
report with Figures extracted from the source PDF.

See skills/core-to-html/SKILL.md for the full spec.

Usage:
    python3 build_html.py <paper-folder>
    python3 build_html.py <paper-folder> --figure-map "Fig1=33,Fig2=34"
    python3 build_html.py <paper-folder> --use-panels
    python3 build_html.py <paper-folder> --extract-only
    python3 build_html.py <paper-folder> --render-only
    python3 build_html.py <paper-folder> --include "lens-academic,lens-industry,methodology-brief"
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import fitz  # pymupdf
    import markdown
    from ruamel.yaml import YAML
except ImportError as e:
    print(
        f"missing dependency ({e}). Install with: "
        "pip install -r skills/source-grounding/scripts/requirements.txt",
        file=sys.stderr,
    )
    sys.exit(1)


REPO_ROOT = Path(__file__).resolve().parents[3]
yaml_io = YAML(typ="rt")


# ---------------------------------------------------------------------------
# CSS — inline so the HTML is standalone
# ---------------------------------------------------------------------------

CSS = """
:root {
    --bg: #fafaf7;
    --text: #222;
    --muted: #5f5f5d;
    --border: #e2e0db;
    --border-strong: #c8c5be;
    --prefix-bg: #f0eee8;
    --code-bg: #f3f1ec;
}
* { box-sizing: border-box; }
html, body {
    margin: 0;
    padding: 0;
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", "Apple SD Gothic Neo",
                 "Noto Sans KR", "Segoe UI", sans-serif;
    line-height: 1.65;
    font-size: 16px;
}
.layout { display: flex; max-width: 1280px; margin: 0 auto; }
.toc {
    width: 260px;
    padding: 32px 16px 32px 32px;
    border-right: 1px solid var(--border);
    position: sticky;
    top: 0;
    align-self: flex-start;
    height: 100vh;
    overflow-y: auto;
    font-size: 14px;
}
.toc h2 { font-size: 13px; text-transform: uppercase; color: var(--muted); margin: 0 0 8px; }
.toc ul { list-style: none; padding-left: 0; margin: 0; }
.toc li { margin: 4px 0; }
.toc a { color: var(--text); text-decoration: none; }
.toc a:hover { text-decoration: underline; }
.toc ul ul { padding-left: 14px; font-size: 13px; }
.content {
    flex: 1 1 auto;
    max-width: 880px;
    padding: 40px 48px;
}
h1, h2, h3, h4 {
    font-weight: 600;
    line-height: 1.25;
    margin-top: 1.6em;
    margin-bottom: 0.6em;
}
h1 { font-size: 28px; }
h2 { font-size: 22px; border-bottom: 1px solid var(--border); padding-bottom: 4px; }
h3 { font-size: 18px; color: #1c1c1c; }
h4 { font-size: 16px; color: var(--muted); }
p, ul, ol { margin: 0.6em 0; }
ul, ol { padding-left: 1.4em; }
li { margin: 0.2em 0; }
code {
    background: var(--code-bg);
    padding: 2px 6px;
    border-radius: 4px;
    font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
    font-size: 0.92em;
}
pre {
    background: var(--code-bg);
    padding: 14px 16px;
    border-radius: 8px;
    overflow-x: auto;
    font-size: 0.88em;
    line-height: 1.5;
}
pre code { background: none; padding: 0; }
blockquote {
    border-left: 3px solid var(--border-strong);
    margin: 1em 0;
    padding: 6px 14px;
    color: var(--muted);
    background: #f5f4ef;
    border-radius: 0 6px 6px 0;
}
table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
    font-size: 0.92em;
}
th, td {
    border: 1px solid var(--border);
    padding: 8px 10px;
    text-align: left;
    vertical-align: top;
}
th { background: #efeee8; font-weight: 600; }
tr:nth-child(even) td { background: rgba(0,0,0,0.015); }
img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 1em auto;
    border: 1px solid var(--border);
    border-radius: 12px;
}
.figure-block {
    margin: 1.5em 0;
    text-align: center;
}
.figure-block .caption {
    font-style: italic;
    color: var(--muted);
    font-size: 0.92em;
    margin-top: 4px;
}
.extracted-table {
    margin: 1em 0;
    overflow-x: auto;
}
.extracted-table .data-table {
    font-size: 0.88em;
}
.extracted-table .caption {
    font-style: italic;
    color: var(--muted);
    font-size: 0.85em;
    margin-top: 4px;
}
details.collapse-block {
    margin: 1em 0;
    padding: 8px 14px;
    background: rgba(0,0,0,0.025);
    border-radius: 6px;
    border-left: 3px solid var(--border-strong);
}
details.collapse-block > summary {
    cursor: pointer;
    font-weight: 600;
    padding: 4px 0;
    color: #1c5078;
    list-style: none;
}
details.collapse-block > summary::before {
    content: "▸ ";
    font-size: 0.85em;
    color: var(--muted);
}
details.collapse-block[open] > summary::before {
    content: "▾ ";
}
details.collapse-block[open] > summary {
    margin-bottom: 8px;
}
hr { border: none; border-top: 1px solid var(--border); margin: 2em 0; }
a { color: #1c5078; }
.prefix {
    display: inline-block;
    padding: 1px 6px;
    border-radius: 4px;
    font-weight: 600;
    font-size: 0.92em;
    margin-right: 2px;
}
.prefix-interpret { background: #d8e3eb; color: #1e3a52; }
.prefix-external  { background: #e9e6df; color: #4a4a48; }
.prefix-estimate  { background: #f3e0bd; color: #6a4d11; }
.prefix-missing   { background: #f0d4d4; color: #6e2a2a; }
.prefix-question  { background: #d5e7d0; color: #2a572a; }
.prefix-todo      { background: #efc9c9; color: #7a1f1f; }
.meta {
    font-size: 0.92em;
    color: var(--muted);
    margin: 0 0 1em;
    padding: 8px 12px;
    background: rgba(0,0,0,0.025);
    border-radius: 6px;
    border-left: 3px solid var(--border-strong);
}
@media (max-width: 900px) {
    .layout { flex-direction: column; }
    .toc { position: static; height: auto; width: 100%; border-right: none;
           border-bottom: 1px solid var(--border); padding: 16px; }
    .content { padding: 24px 16px; }
}
"""


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>{css}</style>
<script>
MathJax = {{tex: {{inlineMath: [['$','$'],['\\\\(','\\\\)']], displayMath: [['$$','$$'],['\\\\[','\\\\]']]}}}};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" async></script>
</head>
<body>
<div class="layout">
<aside class="toc">{toc}</aside>
<main class="content">
{body}
</main>
</div>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Prefix → colored span
# ---------------------------------------------------------------------------

PREFIX_CLASSES = {
    "해석": "prefix-interpret",
    "외부 맥락": "prefix-external",
    "추정": "prefix-estimate",
    "미제공": "prefix-missing",
    "질문": "prefix-question",
    "검토필요": "prefix-todo",
}


def highlight_prefixes(html: str) -> str:
    # Replace "해석:" / "외부 맥락:" / etc. at the start of inline text
    # with a styled span. We match after </p>... ", " starts, or after >, ", ".
    for prefix, klass in PREFIX_CLASSES.items():
        pattern = re.compile(rf"\b{re.escape(prefix)}:")
        replacement = f'<span class="prefix {klass}">{prefix}:</span>'
        html = pattern.sub(replacement, html)
    return html


# ---------------------------------------------------------------------------
# PDF helpers
# ---------------------------------------------------------------------------


def load_paper_info(yaml_path: Path) -> dict[str, Any]:
    with yaml_path.open("r", encoding="utf-8") as f:
        data = yaml_io.load(f)
    return data


def pdf_path_from_yaml(yaml_path: Path, data: dict) -> Path:
    local = (data.get("sources") or {}).get("paper", {}).get("local")
    if not local:
        raise FileNotFoundError("paper-info.yaml has no sources.paper.local")
    p = yaml_path.parent / local
    if not p.exists():
        raise FileNotFoundError(f"PDF not found: {p}")
    return p


FIG_CAPTION_RE = re.compile(
    r"""^\s*
        (?:Extended\s+Data\s+)?
        (?:Fig(?:ure)?\.?)\s*
        (\d+)
        \s*[|:.]
    """,
    re.IGNORECASE | re.VERBOSE,
)


def auto_detect_figure_pages(pdf_path: Path) -> dict[str, int]:
    """Return {'figure-1': page_num, 'extended-data-fig-1': page_num, ...}.

    Heuristic: a page whose first non-empty line matches "Fig(ure) N |" or
    "Extended Data Fig. N |" is the first page of that figure.
    """
    doc = fitz.open(pdf_path)
    found: dict[str, int] = {}
    for page_num in range(len(doc)):
        text = doc[page_num].get_text()
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            m = FIG_CAPTION_RE.match(line)
            if m:
                is_ext = line.lower().startswith("extended")
                num = m.group(1)
                key = f"{'extended-data-fig' if is_ext else 'figure'}-{num}"
                # only record first occurrence
                if key not in found:
                    found[key] = page_num + 1  # 1-based
            break  # only check the first non-empty line
    doc.close()
    return found


def _get_main_content_bbox(page: "fitz.Page", padding: float = 8.0) -> "fitz.Rect":
    """Return a bbox covering horizontal text blocks + image blocks on the page.

    PMC author-manuscript PDFs render an "Author Manuscript" sidebar as
    *rotated* (vertical) text and stamp page numbers / running headers as
    separate blocks at the page margins. By keeping only blocks whose text
    direction is roughly horizontal AND any embedded image bboxes, we cut
    out those margin noise areas automatically.
    """
    raw = page.get_text("dict")
    blocks = raw.get("blocks", [])

    page_rect = page.rect
    page_w = page_rect.width
    page_h = page_rect.height

    boxes: list[tuple[float, float, float, float]] = []

    # PMC author-manuscript margin layout:
    #   top  ~8%  : "Li et al." running header
    #   bot ~12%  : "Nat Biotechnol. Author manuscript..." footer
    #   left ~7%  : vertical "Author Manuscript" sidebar (also caught by
    #               the horizontal-only filter below, but cut explicitly
    #               in case a glyph slips through as a single character)
    TOP_CUT = 0.08
    BOT_CUT = 0.88
    LEFT_CUT = 0.07

    for blk in blocks:
        bbox = blk.get("bbox")
        if not bbox:
            continue
        x0, y0, x1, y1 = bbox
        # Margin filters: drop blocks that lie entirely in the page chrome.
        if y1 < page_h * TOP_CUT:        # entirely above the top-cut line
            continue
        if y0 > page_h * BOT_CUT:        # entirely below the bottom-cut line
            continue
        if x1 < page_w * LEFT_CUT:       # entirely inside the left sidebar
            continue
        # Image block
        if blk.get("type") == 1:
            boxes.append((x0, y0, x1, y1))
            continue
        # Text block: only keep predominantly-horizontal lines
        is_horizontal = False
        for line in blk.get("lines", []):
            dx, dy = line.get("dir", (1.0, 0.0))
            if abs(dy) < 0.3 and abs(dx) > 0.7:
                is_horizontal = True
                break
        if is_horizontal:
            boxes.append((x0, y0, x1, y1))

    if not boxes:
        return page_rect

    x0 = max(0.0, min(b[0] for b in boxes) - padding)
    y0 = max(0.0, min(b[1] for b in boxes) - padding)
    x1 = min(page_w, max(b[2] for b in boxes) + padding)
    y1 = min(page_h, max(b[3] for b in boxes) + padding)
    return fitz.Rect(x0, y0, x1, y1)


def render_page_to_png(pdf_path: Path, page_num: int, out_path: Path,
                       dpi: int = 150, trim: bool = True,
                       clip_bbox: tuple[float, float, float, float] | None = None) -> None:
    """Render a single 1-based page to PNG.

    When ``clip_bbox`` is given, render only that region (page coords, pt).
    Otherwise, when ``trim=True``, automatically crop to the bbox of
    horizontal text + image blocks, removing PMC sidebar and page-number
    margins.
    """
    doc = fitz.open(pdf_path)
    page = doc[page_num - 1]
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    if clip_bbox is not None:
        clip = fitz.Rect(*clip_bbox)
        pix = page.get_pixmap(matrix=mat, clip=clip, alpha=False)
    elif trim:
        clip = _get_main_content_bbox(page)
        pix = page.get_pixmap(matrix=mat, clip=clip, alpha=False)
    else:
        pix = page.get_pixmap(matrix=mat, alpha=False)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pix.save(str(out_path))
    doc.close()


# ---------------------------------------------------------------------------
# Smart per-figure bbox (figure + caption, no body text below)
# ---------------------------------------------------------------------------


def _compute_figure_bbox(
    pdf_path: Path, page_num: int, figure_key: str,
) -> tuple[float, float, float, float] | None:
    """Find a clip bbox for ``figure_key`` (e.g. ``"figure-3"``) on page
    ``page_num`` (1-based). Returns ``(x0, y0, x1, y1)`` in page-pt
    coordinates, or ``None`` if the caption is not detected (caller should
    fall back to whole-page snapshot).

    Strategy: locate the caption block via ``page.get_text("blocks")``.
    A block is treated as the caption when its first non-empty line matches
    ``^\\s*Fig(?:ure)?\\.?\\s*N\\s*[|.]``. The bbox spans the full page
    width, top of page → bottom of caption block (+ small margin). If the
    caption ends within 50pt of the page bottom, we just use the page
    bottom (the figure occupies the whole page).
    """
    # Extract just the figure number from key like 'figure-3' / 'extended-data-fig-3'
    m = re.search(r"(\d+)$", figure_key)
    if not m:
        return None
    n = m.group(1)
    cap_re = re.compile(
        rf"^\s*(?:Extended\s+Data\s+)?Fig(?:ure)?\.?\s*{n}\s*[|.]",
        re.IGNORECASE | re.MULTILINE,
    )

    doc = fitz.open(pdf_path)
    try:
        page = doc[page_num - 1]
        rect = page.rect
        # blocks: list of (x0, y0, x1, y1, text, block_no, block_type)
        blocks = page.get_text("blocks")
        # Sort top-to-bottom for predictable scan order.
        blocks_sorted = sorted(blocks, key=lambda b: (b[1], b[0]))

        caption_idx = None
        for i, blk in enumerate(blocks_sorted):
            text = blk[4] if len(blk) > 4 else ""
            if not text:
                continue
            # cap_re is multiline, so it matches the figure caption pattern
            # at the start of ANY line inside the block.
            if cap_re.search(text):
                caption_idx = i
                break
        if caption_idx is None:
            return None

        cap_block = blocks_sorted[caption_idx]
        cap_y0 = cap_block[1]
        cap_y1 = cap_block[3]

        # Multi-column papers (Nature, etc.) split a single caption across
        # left/right column blocks at the same vertical band. Treat any
        # block whose y0 falls inside the caption-block's y-range and is
        # NOT a body paragraph as a sibling caption block. Body paragraphs
        # start *below* the bottom of the deepest caption-band block.
        cap_band_bottom = cap_y1
        for blk in blocks_sorted:
            y0, y1_b = blk[1], blk[3]
            # block whose top sits inside the caption band → likely a
            # column-sibling of the caption (right-column continuation).
            if cap_y0 - 4.0 <= y0 <= cap_y1 + 4.0:
                cap_band_bottom = max(cap_band_bottom, y1_b)

        margin = 6.0
        y1 = min(rect.y1, cap_band_bottom + margin)
        # If caption ends near the page bottom, just use full page bottom.
        if (rect.y1 - cap_band_bottom) < 50.0:
            y1 = rect.y1
        return (rect.x0, rect.y0, rect.x1, y1)
    finally:
        doc.close()


def apply_panel_spec(pdf_path: Path, spec_path: Path, out_dir: Path) -> dict[str, Path]:
    """Use extract_panels.py-style spec to crop figures and panels.
    Returns {figure_label: composite_png_path}.
    """
    import subprocess

    extract = REPO_ROOT / "skills" / "core-figure" / "scripts" / "extract_panels.py"
    if not extract.exists():
        raise FileNotFoundError(f"extract_panels.py not found at {extract}")
    with spec_path.open("r", encoding="utf-8") as f:
        spec = json.load(f)
    results: dict[str, Path] = {}
    for figure_entry in spec.get("figures", []):
        label = figure_entry["label"]
        single_spec = out_dir / f".{label.lower().replace(' ', '-')}-spec.json"
        with single_spec.open("w", encoding="utf-8") as f:
            json.dump(figure_entry, f)
        subprocess.run(
            [
                sys.executable,
                str(extract),
                str(pdf_path),
                "--spec",
                str(single_spec),
                "--out",
                str(out_dir),
            ],
            check=True,
        )
        # extract_panels.py saves `<label>_crop.png`-like names; we expect the
        # caller to inspect manifest. For now, just record the spec.
        results[label] = out_dir / f"{label.lower().replace(' ', '_')}_crop.png"
    return results


# ---------------------------------------------------------------------------
# Figure mapping management
# ---------------------------------------------------------------------------


def parse_figure_map_arg(spec: str) -> dict[str, int]:
    """Parse 'Fig1=33,Fig2=34,EDFig1=27' format."""
    out = {}
    for piece in spec.split(","):
        piece = piece.strip()
        if not piece or "=" not in piece:
            continue
        key, val = piece.split("=", 1)
        key = key.strip().lower().replace(" ", "-")
        if key.startswith("fig"):
            key = "figure-" + re.sub(r"\D", "", key)
        elif key.startswith("ed"):
            key = "extended-data-fig-" + re.sub(r"\D", "", key)
        try:
            out[key] = int(val)
        except ValueError:
            print(f"warning: bad page number in --figure-map: {piece}", file=sys.stderr)
    return out


def merge_figure_maps(*sources: dict[str, int]) -> dict[str, int]:
    out: dict[str, int] = {}
    for s in sources:
        out.update(s)
    return out


# ---------------------------------------------------------------------------
# Markdown augmentation
# ---------------------------------------------------------------------------

FIGURE_HEADER_RE = re.compile(
    r"^(###\s+)(Figure\s+(\d+)|Extended\s+Data\s+Fig(?:ure)?\.?\s+(\d+))\b",
    re.MULTILINE | re.IGNORECASE,
)

TABLE_AUGMENT_MARKER_RE = re.compile(
    r"<!--\s*augment-table:\s*(?P<key>[\w-]+)\s*-->",
    re.IGNORECASE,
)

TABLE_CAPTION_RE = re.compile(
    r"(?:^|\n)\s*"
    r"(?P<prefix>Supp(?:lementary|\.)?\s+)?"
    r"Table\s*(?P<num>\d+)"
    r"\s*[|:.]",
    re.IGNORECASE,
)


def augment_markdown_with_figures(md_text: str, figures_dir: Path,
                                   figure_map: dict[str, int]) -> str:
    """Insert image markdown right under each '### Figure N' header."""

    def replacement(match: re.Match) -> str:
        header = match.group(0)
        num_fig = match.group(3)
        num_ext = match.group(4)
        if num_ext:
            key = f"extended-data-fig-{num_ext}"
        else:
            key = f"figure-{num_fig}"
        img_path = figures_dir / f"{key}.png"
        # Use repo-relative path for the markdown (HTML will use the same)
        if img_path.exists():
            rel = f"figures/{key}.png"
            return f"{header}\n\n![{match.group(2)}]({rel})\n"
        return header

    return FIGURE_HEADER_RE.sub(replacement, md_text)


# ---------------------------------------------------------------------------
# Table extraction (PDF → HTML table)
# ---------------------------------------------------------------------------


# Skip table extraction on supp PDFs whose filenames imply non-data content.
# Override per-run with --scan-all-supp.
NON_DATA_PDF_FILENAME_PATTERNS = (
    "peer-review",
    "reporting-summary",
    "review-file",
    "referee",
)

# Cheap pre-filter: only run pymupdf's expensive find_tables() on pages
# whose plain text actually contains a "Table N" / "Supplementary Table N"
# caption. find_tables() costs ~1-3 s/page; get_text() costs ~10 ms/page.
TABLE_CAPTION_FAST_RE = re.compile(
    r"(?:Supp(?:lementary|\.)?\s+)?Table\s+\d+\s*[|:.]",
    re.IGNORECASE,
)


def extract_tables_from_pdf(pdf_path: Path) -> list[dict]:
    """Return a list of {label, page, data, bbox} for tables in a single PDF.

    Uses pymupdf's page.find_tables() (v1.23+). Label inferred from the
    nearest 'Table N' / 'Supplementary Table N' caption on the same page.

    Performance: pre-filters pages via TABLE_CAPTION_FAST_RE so find_tables()
    only runs on pages with table-caption text. 10-50x speedup on docs
    where most pages have no tables (peer-review files, figure-only supp).
    """
    if not pdf_path.exists():
        return []
    out: list[dict] = []
    doc = fitz.open(pdf_path)
    try:
        candidate_pages: list[int] = [
            i for i in range(len(doc))
            if TABLE_CAPTION_FAST_RE.search(doc[i].get_text("text"))
        ]
        for page_num in candidate_pages:
            page = doc[page_num]
            try:
                tf = page.find_tables()
                tables = tf.tables if hasattr(tf, "tables") else list(tf)
            except Exception:
                tables = []
            if not tables:
                continue
            page_text = page.get_text()
            captions: list[str] = []
            for m in TABLE_CAPTION_RE.finditer(page_text):
                is_supp = bool(m.group("prefix"))
                num = m.group("num")
                captions.append(
                    f"supplementary-table-{num}" if is_supp else f"table-{num}"
                )
            for i, t in enumerate(tables):
                try:
                    data = t.extract()
                except Exception:
                    continue
                if not data or len(data) < 2:
                    continue
                label = captions[i] if i < len(captions) else None
                out.append({
                    "page": page_num + 1,
                    "label": label,
                    "data": data,
                    "bbox": list(t.bbox) if hasattr(t, "bbox") else None,
                })
    finally:
        doc.close()
    return out


_NUM_RE = re.compile(r"^-?[\d.,]+$")
_TABLE_CAP_LINE_RE = re.compile(
    r"^(?:Supp(?:lementary|\.)?\s+)?Table\s*S?(\d+)\s*[:.|]\s*(.*)$",
    re.IGNORECASE,
)


def reconstruct_table_from_page_text(text: str, source: str, page_num: int) -> dict | None:
    """Fallback for transposed supplementary tables that pymupdf's
    find_tables() misses. Looks for a 'Table SN: ...' caption near the
    bottom of the page and reconstructs the table from the lines above it.

    Expected layout (PMC author manuscript form):

        Supplementary Tables          <- section title (skipped)
        Mouse brain                   <- col header 1
        Mouse skin                    <- col header 2
        Human HSPC                    <- col header 3
        Human brain                   <- col header 4
        Runtime (min)                 <- row 1 label
        40                            <- row 1 col 1
        69                            <- row 1 col 2
        124                           <- row 1 col 3
        40                            <- row 1 col 4
        ...
        Table S1: ...                 <- caption (anchors detection)
    """
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    cap_idx = None
    label = None
    caption_text = None
    for i, ln in enumerate(lines):
        m = _TABLE_CAP_LINE_RE.match(ln)
        if m:
            cap_idx = i
            num = m.group(1)
            # Always treat the table as a supplementary one when called via
            # this fallback (it's only invoked on supp PDFs in practice).
            label = f"supplementary-table-{num}"
            caption_text = ln
            break
    if cap_idx is None:
        return None

    pre = lines[:cap_idx]
    drop_titles = {"supplementary tables", "supplementary table", "tables"}
    pre = [ln for ln in pre if ln.lower() not in drop_titles]
    if not pre:
        return None

    # Find the first numeric line: that's where the first data row begins.
    first_num_idx = None
    for i, ln in enumerate(pre):
        if _NUM_RE.match(ln):
            first_num_idx = i
            break
    if first_num_idx is None or first_num_idx == 0:
        return None

    # Walk forward from first_num_idx to count consecutive numerics — that's
    # the number of data columns (one per dataset / metric).
    n_cols = 0
    j = first_num_idx
    while j < len(pre) and _NUM_RE.match(pre[j]):
        n_cols += 1
        j += 1
    if n_cols < 2:
        return None

    # The first ``n_cols`` non-numeric lines are the column headers; the
    # remaining ``first_num_idx - n_cols`` lines between them and the first
    # numeric block are the *first row's* row label (typically 1 line).
    if first_num_idx < n_cols:
        return None
    col_headers = pre[:n_cols]

    # Now read alternating (row_label, n_cols numeric values).
    rows: list[list[str]] = []
    i = n_cols
    while i < len(pre):
        if _NUM_RE.match(pre[i]):
            # Unexpected — bail out gracefully.
            break
        row_label = pre[i]
        i += 1
        nums: list[str] = []
        while i < len(pre) and _NUM_RE.match(pre[i]) and len(nums) < n_cols:
            nums.append(pre[i])
            i += 1
        if len(nums) != n_cols:
            break
        rows.append([row_label] + nums)
    if not rows:
        return None

    # Build a 2D data array compatible with table_to_html
    data2d = [[""] + col_headers] + rows
    return {
        "page": page_num,
        "label": label,
        "data": data2d,
        "source": source,
        "caption": caption_text,
        "reconstructed": True,
    }


def _pdf_fingerprint(pdf_path: Path) -> list:
    """Cache key entry per PDF — invalidate on content change."""
    if not pdf_path.exists():
        return [str(pdf_path), "missing"]
    st = pdf_path.stat()
    return [str(pdf_path), st.st_mtime_ns, st.st_size]


def collect_tables_from_paper(yaml_dir: Path, data: dict,
                              scan_all_supp: bool = False,
                              cache_file: Path | None = None) -> dict[str, dict]:
    """Walk paper.local + supplementary[].local PDFs and collect tables.

    Tries pymupdf's find_tables() first. Falls back to text-based
    reconstruction for transposed supplementary tables that find_tables()
    cannot parse.

    Performance:
    - Skips supp PDFs whose filename matches NON_DATA_PDF_FILENAME_PATTERNS
      (peer review, reporting summary, etc.) — opt in via scan_all_supp=True.
    - mtime-based cache: cache_file stores result + per-PDF fingerprint;
      second run is ~instant if no PDF changed.
    - Page-level pre-filter inside extract_tables_from_pdf and the text
      fallback below — only pages with 'Table N' caption are touched.
    """
    sources = data.get("sources") or {}

    # Resolve which PDFs to scan (after filename filter).
    pdf_list: list[tuple[Path, str]] = []
    paper_local = (sources.get("paper") or {}).get("local")
    if paper_local:
        pdf_list.append((yaml_dir / paper_local, "paper"))
    for i, supp in enumerate(sources.get("supplementary") or []):
        local = supp.get("local")
        if not local:
            continue
        name = Path(local).name.lower()
        if not scan_all_supp and any(p in name for p in NON_DATA_PDF_FILENAME_PATTERNS):
            print(f"  skipping {local} (non-data filename — use --scan-all-supp to override)")
            continue
        pdf_list.append((yaml_dir / local, f"supp-{i+1}"))

    fingerprint = [_pdf_fingerprint(p) for p, _ in pdf_list]

    # Cache hit?
    if cache_file and cache_file.exists():
        try:
            cached = json.loads(cache_file.read_text(encoding="utf-8"))
            if cached.get("fingerprint") == fingerprint:
                n = len(cached.get("found") or {})
                print(f"  table cache hit ({n} table(s)) — {cache_file.relative_to(REPO_ROOT)}")
                return cached.get("found") or {}
        except Exception:
            pass

    # Cold path: actually extract.
    found: dict[str, dict] = {}
    for pdf, source_label in pdf_list:
        for t in extract_tables_from_pdf(pdf):
            label = t.get("label")
            if not label or label in found:
                continue
            t["source"] = source_label
            found[label] = t
        # Text fallback: same page pre-filter so peer-review etc. stays cheap.
        if not pdf.exists():
            continue
        doc = fitz.open(pdf)
        try:
            for page_num in range(len(doc)):
                text = doc[page_num].get_text()
                if not TABLE_CAPTION_FAST_RE.search(text):
                    continue
                rec = reconstruct_table_from_page_text(text, source_label, page_num + 1)
                if rec and rec["label"] not in found:
                    rec["source"] = source_label
                    found[rec["label"]] = rec
        finally:
            doc.close()

    # Save cache.
    if cache_file:
        try:
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            cache_file.write_text(
                json.dumps({"fingerprint": fingerprint, "found": found},
                           indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except Exception as e:
            print(f"  warning: failed to write table cache: {e}", file=sys.stderr)

    return found


def table_to_html(data: list[list], source_note: str | None = None) -> str:
    """Render a 2D list (header row + body) into an HTML table."""
    if not data:
        return ""
    # pymupdf sometimes returns None cells; replace with empty string
    def cell(v: Any) -> str:
        if v is None:
            return ""
        return str(v).replace("\n", "<br>").strip()

    header = data[0]
    body = data[1:]
    th = "".join(f"<th>{cell(c)}</th>" for c in header)
    tr_body = "".join(
        "<tr>" + "".join(f"<td>{cell(c)}</td>" for c in row) + "</tr>"
        for row in body
    )
    note = f'<div class="caption">{source_note}</div>' if source_note else ""
    return (
        f'<div class="extracted-table">'
        f'<table class="data-table"><thead><tr>{th}</tr></thead>'
        f'<tbody>{tr_body}</tbody></table>{note}</div>'
    )


_DETAILS_BLOCK_RE = re.compile(
    r"^:::\s*details\s+(?P<title>.+?)\s*\n(?P<body>.*?)\n^:::\s*$",
    re.MULTILINE | re.DOTALL,
)


def expand_details_blocks(md_text: str) -> str:
    """Pre-process ``::: details <title>\\n...content...\\n:::`` blocks
    into ``<details><summary>...</summary>HTML</details>`` so the contained
    markdown is properly nested under a collapsible disclosure widget.
    The body is rendered to HTML *before* the main markdown pass to avoid
    the parser swallowing it as raw HTML.
    """
    def replace(match: re.Match) -> str:
        title = match.group("title").strip()
        body_md = match.group("body")
        body_md, replacements = _protect_math_and_code(body_md)
        body_html = markdown.markdown(
            body_md,
            extensions=[
                "extra",
                "tables",
                "fenced_code",
                "mdx_truly_sane_lists",
            ],
            extension_configs={
                "mdx_truly_sane_lists": {"nested_indent": 2, "truly_sane": True},
            },
        )
        body_html = _restore_math_and_code(body_html, replacements)
        body_html = highlight_prefixes(body_html)
        return (
            f'<details class="collapse-block">\n'
            f'<summary>{title}</summary>\n'
            f'{body_html}\n'
            f'</details>'
        )

    return _DETAILS_BLOCK_RE.sub(replace, md_text)


def augment_markdown_with_tables(md_text: str, tables: dict[str, dict]) -> str:
    """Replace ``<!-- augment-table: <key> -->`` markers with HTML tables.

    The key (e.g. ``supplementary-table-1``) is matched against the dict
    returned by ``collect_tables_from_paper``. If no matching table was
    extracted, the marker is replaced with a small italic note so the
    failure is visible in the rendered HTML instead of silently vanishing.
    """

    def replacement(match: re.Match) -> str:
        key = match.group("key").lower()
        info = tables.get(key)
        if not info:
            return (
                f'<p class="caption"><em>(table augment marker for '
                f'<code>{key}</code> — extraction not available)</em></p>'
            )
        source = info.get("source", "?")
        page = info.get("page", "?")
        recon = " (text reconstruction)" if info.get("reconstructed") else ""
        note = f"<em>PDF 자동 추출{recon} — {source} PDF page {page}</em>"
        return table_to_html(info["data"], source_note=note)

    return TABLE_AUGMENT_MARKER_RE.sub(replacement, md_text)


# ---------------------------------------------------------------------------
# Math protection (preserve $...$ / $$...$$ / \(...\) / \[...\] through
# the markdown pass so MathJax can render them in the browser)
# ---------------------------------------------------------------------------

# Order matters: longest/most-specific delimiters first so $$...$$ is not
# eaten by $...$. We skip math inside fenced code (``` ... ```) and inline
# code (`...`) — code blocks are pulled out first, then restored.
_CODE_FENCE_RE = re.compile(r"(^|\n)(```.*?\n.*?\n```)", re.DOTALL)
_CODE_INLINE_RE = re.compile(r"`[^`\n]+`")

_MATH_PATTERNS = [
    re.compile(r"\$\$(.+?)\$\$", re.DOTALL),     # display $$...$$
    re.compile(r"\\\[(.+?)\\\]", re.DOTALL),     # display \[...\]
    re.compile(r"(?<!\\)\$(?!\s)(.+?)(?<!\s)(?<!\\)\$"),  # inline $...$
    re.compile(r"\\\((.+?)\\\)", re.DOTALL),     # inline \(...\)
]


def _protect_math_and_code(md_text: str) -> tuple[str, dict[str, str]]:
    """Replace math + code spans with unique placeholders so the markdown
    parser does not mangle special characters (``_``, ``*``, ``\``) inside
    them. Returns (modified_text, {placeholder: original}).

    Code spans are extracted *first* so that any ``$`` inside ``code``
    stays literal (not treated as math). Math is then extracted from what
    remains. Placeholders are restored *after* the HTML pass, so MathJax
    sees the original delimiters in the rendered HTML.
    """
    replacements: dict[str, str] = {}
    counter = [0]

    def stash(text: str) -> str:
        token = f"\x00MATHCODE{counter[0]:06d}\x00"
        counter[0] += 1
        replacements[token] = text
        return token

    # 1. Fenced code blocks (multi-line)
    def fenced_sub(m: re.Match) -> str:
        prefix = m.group(1)
        code = m.group(2)
        return prefix + stash(code)
    md_text = _CODE_FENCE_RE.sub(fenced_sub, md_text)

    # 2. Inline code
    md_text = _CODE_INLINE_RE.sub(lambda m: stash(m.group(0)), md_text)

    # 3. Math (display first, then inline)
    for pat in _MATH_PATTERNS:
        md_text = pat.sub(lambda m: stash(m.group(0)), md_text)

    return md_text, replacements


def _restore_math_and_code(html: str, replacements: dict[str, str]) -> str:
    for token, original in replacements.items():
        html = html.replace(token, original)
    return html


# ---------------------------------------------------------------------------
# Markdown → HTML
# ---------------------------------------------------------------------------


def md_to_html(md_text: str) -> tuple[str, str]:
    """Return (body_html, toc_html).

    `mdx_truly_sane_lists` honours 2-space indentation for nested lists,
    so the natural hierarchy in <paper-id>_core.md ("- Hidden assumption:\n  1. foo")
    renders as a real nested list instead of a flat one. We also avoid
    `sane_lists`, which would insist on 4-space indents.

    Math expressions (``$...$``, ``$$...$$``, ``\\(...\\)``, ``\\[...\\]``)
    and code spans are masked with placeholders before the markdown pass so
    the parser does not mangle their special characters; placeholders are
    restored in the resulting HTML for MathJax to pick up in the browser.
    """
    md_text, replacements = _protect_math_and_code(md_text)
    md = markdown.Markdown(
        extensions=[
            "extra",
            "tables",
            "toc",
            "fenced_code",
            "mdx_truly_sane_lists",
        ],
        extension_configs={
            "toc": {"permalink": False, "toc_depth": "2-3"},
            "mdx_truly_sane_lists": {
                "nested_indent": 2,
                "truly_sane": True,
            },
        },
    )
    body = md.convert(md_text)
    body = _restore_math_and_code(body, replacements)
    body = highlight_prefixes(body)
    toc = md.toc
    return body, toc


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def _paper_id_from_folder(paper_folder: Path) -> str:
    return paper_folder.resolve().name


def collect_markdown(paper_folder: Path, include: list[str]) -> str:
    """Concatenate <paper-id>_core.md + included files into one markdown string.

    Output files in the paper folder follow the ``<paper-id>_<role>.md``
    naming convention (paper-id == folder name). The ``include`` argument
    accepts role names (e.g. "lens-academic"), which are resolved to
    ``<paper-id>_lens-academic.md`` with a fallback to the legacy bare name.
    """
    parts = []
    paper_id = _paper_id_from_folder(paper_folder)
    core_path = paper_folder / f"{paper_id}_core.md"
    if not core_path.exists():
        legacy = paper_folder / "core.md"
        if legacy.exists():
            core_path = legacy
        else:
            print(f"{core_path.name} not found in {paper_folder}", file=sys.stderr)
            sys.exit(1)
    parts.append(core_path.read_text(encoding="utf-8"))
    for raw in include:
        name = raw.strip()
        if not name:
            continue
        name = name[:-3] if name.endswith(".md") else name
        candidates = [
            paper_folder / f"{paper_id}_{name}.md",
            paper_folder / f"{name}.md",
        ]
        p = next((c for c in candidates if c.exists()), None)
        if p is None:
            print(f"  (skip, not found): {candidates[0]}", file=sys.stderr)
            continue
        title = name.replace("-", " ").title()
        parts.append(f"\n\n---\n\n# {title}\n\n")
        parts.append(p.read_text(encoding="utf-8"))
    return "\n\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build HTML report from <paper-id>_core.md + PDF figures")
    parser.add_argument("paper_folder", type=Path, help="analysis/<topic>/<paper-id>/")
    parser.add_argument("--figure-map", default="", help="Override: 'Fig1=33,Fig2=34,EDFig1=27'")
    parser.add_argument("--use-panels", action="store_true", help="Use figures/panels.json (panel-level)")
    parser.add_argument("--extract-only", action="store_true", help="Extract figures, no HTML")
    parser.add_argument("--render-only", action="store_true", help="Render HTML, skip extraction")
    parser.add_argument("--include", default="lens-academic,lens-industry,methodology-brief",
                        help="Additional .md files to include in the HTML (comma-separated)")
    parser.add_argument("--dpi", type=int, default=150, help="PNG export DPI (default 150)")
    parser.add_argument("--no-toc", action="store_true", help="Skip TOC sidebar")
    parser.add_argument("--no-tables", action="store_true",
                        help="Skip PDF table extraction entirely (escape hatch for slow runs)")
    parser.add_argument("--scan-all-supp", action="store_true",
                        help="Scan ALL supp PDFs for tables; default skips peer-review/reporting-summary")
    args = parser.parse_args()

    folder = args.paper_folder.resolve()
    yaml_path = folder / "paper-info.yaml"
    if not yaml_path.exists():
        print(f"not found: {yaml_path}", file=sys.stderr)
        return 1

    data = load_paper_info(yaml_path)
    pdf = pdf_path_from_yaml(yaml_path, data)

    figures_dir = folder / "figures"
    figures_dir.mkdir(exist_ok=True)
    map_file = figures_dir / "figure-map.json"

    # ----- Figure extraction -----
    if not args.render_only:
        if args.use_panels:
            panels_spec = figures_dir / "panels.json"
            if not panels_spec.exists():
                print(f"--use-panels requested but {panels_spec} not found", file=sys.stderr)
                return 1
            print(f"applying panel spec from {panels_spec.relative_to(REPO_ROOT)}")
            apply_panel_spec(pdf, panels_spec, figures_dir)
        else:
            # Page-level (with smart per-figure bbox crop)
            auto_map = auto_detect_figure_pages(pdf)
            saved_map: dict[str, int] = {}
            saved_bbox: dict[str, list[float]] = {}
            if map_file.exists():
                with map_file.open("r", encoding="utf-8") as f:
                    raw_saved = json.load(f)
                for k, v in raw_saved.items():
                    # Back-compat: old schema stored {key: int}
                    if isinstance(v, int):
                        saved_map[k] = v
                    elif isinstance(v, dict) and "page" in v:
                        saved_map[k] = int(v["page"])
                        if "bbox" in v and v["bbox"] is not None:
                            saved_bbox[k] = list(v["bbox"])
            cli_map = parse_figure_map_arg(args.figure_map) if args.figure_map else {}
            # priority: cli > saved > auto
            final_map = merge_figure_maps(auto_map, saved_map, cli_map)

            if not final_map:
                print("no figure pages auto-detected and no override provided.", file=sys.stderr)
            else:
                print("figure → page mapping:")
                for key in sorted(final_map.keys()):
                    print(f"  {key}: page {final_map[key]}")

            # Compute / persist per-figure bbox map (new schema)
            new_map: dict[str, dict] = {}
            for key, page in final_map.items():
                out_path = figures_dir / f"{key}.png"
                bbox = None
                # If CLI overrode page or saved bbox is missing, recompute.
                if key in saved_bbox and key not in cli_map:
                    bbox = tuple(saved_bbox[key])
                else:
                    bbox = _compute_figure_bbox(pdf, page, key)
                if bbox is None:
                    print(
                        f"  warning: caption regex did not match on page {page} for {key}; "
                        f"falling back to whole-page snapshot",
                        file=sys.stderr,
                    )
                    render_page_to_png(pdf, page, out_path, dpi=args.dpi)
                    new_map[key] = {"page": page, "bbox": None}
                else:
                    render_page_to_png(pdf, page, out_path, dpi=args.dpi, clip_bbox=bbox)
                    new_map[key] = {"page": page, "bbox": list(bbox)}
                print(f"  wrote {out_path.relative_to(REPO_ROOT)}")

            # Persist the map for next run (new schema)
            with map_file.open("w", encoding="utf-8") as f:
                json.dump(new_map, f, indent=2, ensure_ascii=False)
            print(f"  saved mapping to {map_file.relative_to(REPO_ROOT)}")

    if args.extract_only:
        return 0

    # ----- Markdown augmentation -----
    include = [s for s in args.include.split(",") if s.strip()]
    full_md = collect_markdown(folder, include)

    # Figures
    augmented = augment_markdown_with_figures(full_md, figures_dir,
                                              figure_map={})

    # Tables (main + supp PDFs)
    if args.no_tables:
        pdf_tables = {}
        print("table extraction skipped (--no-tables)")
    else:
        pdf_tables = collect_tables_from_paper(
            folder, data,
            scan_all_supp=args.scan_all_supp,
            cache_file=figures_dir / ".table_cache.json",
        )
    if pdf_tables:
        print(f"extracted tables: {sorted(pdf_tables.keys())}")
        augmented = augment_markdown_with_tables(augmented, pdf_tables)
    else:
        if not args.no_tables:
            print("no PDF tables found via find_tables() or text fallback")

    # Expand ::: details Title ::: blocks into <details> disclosure widgets
    augmented = expand_details_blocks(augmented)

    paper_id = _paper_id_from_folder(folder)
    aug_path = folder / f"{paper_id}_core-with-figures.md"
    aug_path.write_text(augmented, encoding="utf-8")
    print(f"wrote {aug_path.relative_to(REPO_ROOT)}")

    # ----- HTML render -----
    body, toc = md_to_html(augmented)
    title = data.get("title") or folder.name
    html = HTML_TEMPLATE.format(
        title=title,
        css=CSS,
        toc=toc if not args.no_toc else "",
        body=body,
    )
    html_path = folder / f"{paper_id}_core.html"
    html_path.write_text(html, encoding="utf-8")
    print(f"wrote {html_path.relative_to(REPO_ROOT)}")
    print(f"\n브라우저에서 열기: open {html_path.relative_to(REPO_ROOT)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
