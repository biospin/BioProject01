#!/usr/bin/env python3
"""CONF_LONGABSTRACT_GIW2026_BIOP01.md -> 2-page two-column LaTeX for GIW submission.

Text is converted mechanically (no retyping) so no number can drift.  The Korean
pre-submission memo (the leading HTML comment) is dropped by construction: the body
starts at the first '# ' title line.  Figure legends become the figure captions.
"""
import re, sys, unicodedata

SRC = "/home/kkkim/project/BioProject01/manuscript/CONF_LONGABSTRACT_GIW2026_BIOP01.md"
FIGDIR = "figures"
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/claude-10005/giw/main.tex"

UNI = {
    "α": r"$\alpha$", "γ": r"$\gamma$", "ρ": r"$\rho$", "Δ": r"$\Delta$",
    "×": r"$\times$", "≤": r"$\le$", "≥": r"$\ge$", "≈": r"$\approx$",
    "→": r"$\rightarrow$", "↔": r"$\leftrightarrow$", "−": r"$-$",
    "⁴": r"$^4$", "±": r"$\pm$", "~": r"$\sim$",
    "–": "--", "—": "---", "’": "'", "‘": "'", "“": "``", "”": "''",
    "…": r"\ldots{}", "\u00a0": "~",
}
SPECIAL = {"&": r"\&", "%": r"\%", "#": r"\#", "_": r"\_"}


def esc(s):
    for k, v in SPECIAL.items():
        s = s.replace(k, v)
    for k, v in UNI.items():
        s = s.replace(k, v)
    return s


def inline(s):
    """markdown inline -> LaTeX. Code first so its content is not re-marked."""
    holes = []

    def stash(tex):
        holes.append(tex)
        return f"\x00{len(holes)-1}\x00"

    s = re.sub(r"`([^`]+)`", lambda m: stash(r"\texttt{" + esc(m.group(1)) + "}"), s)
    s = re.sub(r"\*\*(.+?)\*\*", lambda m: stash(r"\textbf{" + esc(m.group(1)) + "}"), s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", lambda m: stash(r"\emph{" + esc(m.group(1)) + "}"), s)
    s = esc(s)
    # alpha_c style subscripts written as "alpha_c" survive esc() as \_ ; fix the known one
    s = s.replace(r"$\alpha$\_c", r"$\alpha_c$")
    return re.sub(r"\x00(\d+)\x00", lambda m: holes[int(m.group(1))], s)


raw = open(SRC, encoding="utf-8").read()
body = raw[raw.index("\n# "):].strip()          # drops the Korean memo comment block
lines = body.split("\n")

title = lines[0][2:].strip()
rest = "\n".join(lines[1:])

# --- split into sections -------------------------------------------------
parts = re.split(r"^## ", rest, flags=re.M)
preamble = parts[0]
sections = []
for chunk in parts[1:]:
    head, _, text = chunk.partition("\n")
    sections.append((head.strip(), text.strip()))

# --- figure legends become captions --------------------------------------
legends = {}
for head, text in sections:
    if head.lower().startswith("figure legend"):
        for m in re.finditer(r"\*\*Figure (\d)\.\*\*(.*?)(?=\*\*Figure \d\.\*\*|\Z)", text, re.S):
            cap = " ".join(m.group(2).split())
            cap = re.sub(r"Source:\s*`[^`]+`\.?", "", cap).strip()
            legends[int(m.group(1))] = cap

FIGS = {1: (f"{FIGDIR}/fig01_p2_concordance.png", "fig1"),
        2: (f"{FIGDIR}/fig07_reliability_map.png", "fig2")}


def figure_env(n):
    path, lab = FIGS[n]
    return ("\\begin{figure}[t]\n\\centering\n"
            f"\\includegraphics[width=\\columnwidth]{{{path}}}\n"
            f"\\caption{{{inline(legends[n])}}}\n\\label{{{lab}}}\n"
            "\\end{figure}\n")


def paragraphs(text):
    out = []
    for para in re.split(r"\n\s*\n", text):
        para = " ".join(para.split())
        if para:
            out.append(inline(para))
    return out


chunks = []
for head, text in sections:
    h = head.lower()
    if h.startswith("figure legend"):
        continue
    if h.startswith("references"):
        items = [inline(" ".join(l.split()))
                 for l in text.split("\n") if l.strip().startswith("[")]
        chunks.append("\\section*{References}\n\\begin{refs}\n" +
                      "\n".join(f"\\item {it}" for it in items) + "\n\\end{refs}\n")
        continue
    chunks.append(f"\\section*{{{inline(head)}}}\n")
    if h.startswith("results"):
        chunks.append(figure_env(1))
    if h.startswith("conclusion"):
        chunks.append(figure_env(2))
    chunks.append("\n\n".join(paragraphs(text)) + "\n")

subtitle = ""
m = re.search(r"^\*\((.+?)\)\*", preamble.strip(), re.M | re.S)
if m:
    subtitle = inline(" ".join(m.group(1).split()))

TEX = r"""\documentclass[10pt,twocolumn]{article}
\usepackage[a4paper,margin=1.9cm,columnsep=0.7cm]{geometry}
\usepackage{graphicx}
\usepackage{amsmath,amssymb}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{caption}
\captionsetup{font=footnotesize,labelfont=bf,skip=4pt}
\newlist{refs}{enumerate}{1}
\setlist[refs]{label=,leftmargin=1.1em,itemindent=-1.1em,
               nosep,itemsep=1pt,font=\footnotesize}
\setlength{\parskip}{0pt}
\setlength{\parindent}{1em}
\pagestyle{empty}
\renewcommand{\baselinestretch}{0.98}
\begin{document}
\twocolumn[
\begin{@twocolumnfalse}
\begin{center}
{\large\bfseries TITLE\par}
\vspace{2pt}
{\footnotesize\itshape SUBTITLE\par}
\end{center}
\vspace{6pt}
\end{@twocolumnfalse}
]
\small
BODY
\end{document}
"""

tex = (TEX.replace("SUBTITLE", subtitle)          # before TITLE: 'SUBTITLE' contains 'TITLE'
          .replace("TITLE", inline(title))
          .replace("BODY", "\n".join(chunks)))
# straight ASCII quote pairs -> proper TeX quotes
tex = re.sub(r'"([^"\n]+)"', r"``\1''", tex)

import os
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write(tex)

leftover = sorted({c for c in tex if ord(c) > 127})
print("wrote", OUT, "|", len(tex), "chars")
print("non-ASCII left:", [(c, unicodedata.name(c, "?")) for c in leftover] or "none")
print("figures:", {n: FIGS[n][0] for n in legends})
