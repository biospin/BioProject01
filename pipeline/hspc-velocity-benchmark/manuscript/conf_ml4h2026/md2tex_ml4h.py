#!/usr/bin/env python3
"""CONF_ML4H2026_BIOP01.md -> ML4H 2026 (jmlr/pmlr) two-column LaTeX.

GIW 선례(`../conf_giw2026/md2tex.py`)와 같은 원칙을 따른다.

- **수치를 사람이 옮겨 적지 않는다.** 마크다운을 기계 변환하므로 드리프트가 생길 수 없다.
- **한국어 제출-전-제거 메모가 원천적으로 안 실린다.** 본문을 첫 `# ` 제목 줄부터 잘라 쓰므로
  파일 머리의 HTML 주석 블록(수치 출처·내부 판단)은 들어갈 수 없다.
- 그리스 문자·수학 기호는 LaTeX 매크로로 치환하고, 변환 후 남은 non-ASCII를 출력한다(정상 = none).

ML4H 규정(2026 CFP 실측):
- Findings 트랙 본문 **4페이지**, 참고문헌과 부록은 **페이지 수에 포함되지 않는다**.
- 이중맹검. 저자·소속·자기 인용 귀속이 드러나면 desk rejection.
- 공식 템플릿은 `jmlr` 클래스에 `[pmlr,twocolumn,10pt]` 옵션.

사용:
  python3 md2tex_ml4h.py <build_dir>/main.tex
"""
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "CONF_ML4H2026_BIOP01.md")
FIGDIR = "figures"
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/ml4h/main.tex"

# 본문에 실제로 등장하는 17종(md2tex_ml4h 점검 기준). GIW 표에 없던 것 = kappa, tau, gg, gtrsim, uuml.
UNI = {
    "α": r"$\alpha$", "β": r"$\beta$", "γ": r"$\gamma$", "ρ": r"$\rho$",
    "κ": r"$\kappa$", "τ": r"$\tau$", "Δ": r"$\Delta$",
    "×": r"$\times$", "≤": r"$\le$", "≥": r"$\ge$", "≈": r"$\approx$",
    "≫": r"$\gg$", "≳": r"$\gtrsim$",
    "→": r"$\rightarrow$", "↔": r"$\leftrightarrow$", "−": r"$-$",
    "⁴": r"$^4$", "±": r"$\pm$", "ü": r'\"u',
    "–": "--", "—": "---", "’": "'", "‘": "'", "“": "``", "”": "''",
    "…": r"\ldots{}", "\u00a0": "~",
}
SPECIAL = {"&": r"\&", "%": r"\%", "#": r"\#", "_": r"\_", "~": r"$\sim$"}

# 아래첨자로 살려야 하는 것들(esc가 \_ 로 만든 뒤 되돌린다)
SUBS = [
    (r"$\alpha$\_c", r"$\alpha_c$"),
    (r"$\Delta$\_rr", r"$\Delta_{rr}$"),
    (r"k\_deg", r"$k_{\mathrm{deg}}$"),
    (r"t\_sw1", r"$t_{\mathrm{sw1}}$"),
    (r"t\_sw2", r"$t_{\mathrm{sw2}}$"),
]


def esc(s):
    for k, v in SPECIAL.items():
        s = s.replace(k, v)
    for k, v in UNI.items():
        s = s.replace(k, v)
    return s


def inline(s):
    """markdown inline -> LaTeX. 코드부터 처리해 그 안이 다시 마크되지 않게 한다."""
    holes = []

    def stash(tex):
        holes.append(tex)
        return f"\x00{len(holes) - 1}\x00"

    s = re.sub(r"`([^`]+)`", lambda m: stash(r"\texttt{" + esc(m.group(1)) + "}"), s)
    s = re.sub(r"\*\*(.+?)\*\*", lambda m: stash(r"\textbf{" + esc(m.group(1)) + "}"), s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", lambda m: stash(r"\emph{" + esc(m.group(1)) + "}"), s)
    s = esc(s)
    for a, b in SUBS:
        s = s.replace(a, b)
    return re.sub(r"\x00(\d+)\x00", lambda m: holes[int(m.group(1))], s)


def paragraphs(text):
    out = []
    for para in re.split(r"\n\s*\n", text):
        if para.strip().startswith("|"):        # 표는 따로 처리
            continue
        para = " ".join(para.split())
        if para:
            out.append(inline(para))
    return out


def md_table(text):
    """마크다운 표 -> (헤더 리스트, 행 리스트). 구분선(|---|)은 버린다."""
    rows = []
    for line in text.split("\n"):
        line = line.strip()
        if not line.startswith("|"):
            continue
        if re.fullmatch(r"\|[\s:|-]+\|", line):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        rows.append(cells)
    return (rows[0], rows[1:]) if rows else ([], [])


def table_env(head, body_text, label, colspec, fontsize, env="table*", place="[t]"):
    """본문 표. 4페이지 제약이 빡빡하므로 폭을 명시해 넘침을 막는다.
    env='table'이면 단(column) float이라 페이지 상·하단 어디에나 앉을 수 있어
    참고문헌 뒤로 밀려나지 않는다."""
    header, rows = md_table(body_text)
    lead = [p for p in paragraphs(body_text)]
    caption = inline(re.sub(r"^Table\s+\d+\.\s*", "", head))   # LaTeX가 번호를 매긴다
    if lead:
        caption += " " + lead[0]
    tex = [f"\\begin{{{env}}}{place}", "\\centering", f"\\{fontsize}",
           "\\setlength{\\tabcolsep}{2pt}",
           f"\\caption{{{caption}}}", f"\\label{{{label}}}",
           f"\\begin{{tabular}}{{{colspec}}}", "\\toprule",
           " & ".join(f"\\textbf{{{inline(c)}}}" for c in header) + " \\\\", "\\midrule"]
    for r in rows:
        tex.append(" & ".join(inline(c) for c in r) + " \\\\")
    tex += ["\\bottomrule", "\\end{tabular}", f"\\end{{{env}}}", ""]
    return "\n".join(tex)


def plain_table(body_text):
    """부록용 비-float 표. 순서가 어긋나지 않게 그 자리에 그대로 조판한다."""
    header, rows = md_table(body_text)
    if not header:
        return ""
    n = len(header)
    # 열 폭을 균등 분배하면 CI 문자열("+0.643 [+0.554, +0.719]")이 접힌다.
    # 열별 최대 글자수에 비례해 나눈다.
    mx = [max(len(r[i]) if i < len(r) else 0 for r in [header] + rows) for i in range(n)]
    ws = [max(m, 6) for m in mx]
    tot = sum(ws)
    ws = [0.93 * w / tot for w in ws]
    colspec = "".join(f">{{\\raggedright\\arraybackslash}}p{{{w:.3f}\\textwidth}}" for w in ws)
    tex = ["\\begin{center}", "\\scriptsize" if n >= 5 else "\\footnotesize",
           "\\setlength{\\tabcolsep}{2pt}",
           f"\\begin{{tabular}}{{{colspec}}}", "\\toprule",
           " & ".join(f"\\textbf{{{inline(c)}}}" for c in header) + " \\\\", "\\midrule"]
    for r in rows:
        tex.append(" & ".join(inline(c) for c in r) + " \\\\")
    tex += ["\\bottomrule", "\\end{tabular}", "\\end{center}", ""]
    return "\n".join(tex)


def blocks(text):
    """문단과 표를 소스 순서 그대로 잇는다(부록 전용)."""
    out = []
    for para in re.split(r"\n\s*\n", text):
        if para.strip().startswith("|"):
            t = plain_table(para)
            if t:
                out.append(t)
            continue
        para = " ".join(para.split())
        if para:
            out.append(inline(para))
    return "\n\n".join(out)


raw = open(SRC, encoding="utf-8").read()
body = raw[raw.index("\n# "):].strip()          # 한국어 메모 주석 블록을 버린다
lines = body.split("\n")
title = lines[0][2:].strip()
rest = "\n".join(lines[1:])

parts = re.split(r"^## ", rest, flags=re.M)
sections = []
for chunk in parts[1:]:
    headline, _, text = chunk.partition("\n")
    sections.append((headline.strip(), text.strip()))


def subsections(text):
    """### 소제목을 \\subsection 으로. 소제목 앞의 도입 문단은 그대로 둔다."""
    bits = re.split(r"^### ", text, flags=re.M)
    out = ["\n\n".join(paragraphs(bits[0]))] if bits[0].strip() else []
    for b in bits[1:]:
        h, _, t = b.partition("\n")
        h = re.sub(r"^\d+(\.\d+)*\.?\s*", "", h.strip())      # "3.1 " 번호 제거(클래스가 매김)
        out.append(f"\\subsection{{{inline(h)}}}")
        out.append("\n\n".join(paragraphs(t)))
    return "\n\n".join(x for x in out if x.strip())


# --- figure legend -> caption ------------------------------------------------
legend = ""
for head, text in sections:
    if head.lower().startswith("figure legend"):
        m = re.search(r"\*\*Figure 1\.\*\*(.*)", text, re.S)
        if m:
            cap = " ".join(m.group(1).split())
            cap = re.sub(r"Source figure:\s*`[^`]+`\.?", "", cap).strip()
            legend = inline(cap)

FIG = ("\\begin{figure}[t]\n\\centering\n"
       f"\\includegraphics[width=\\columnwidth]{{{FIGDIR}/fig01_p2_concordance.png}}\n"
       f"\\caption{{{legend}}}\n\\label{{fig:concordance}}\n\\end{{figure}}\n")

abstract = ""
main, tables, refs, appendix = [], [], "", []

for head, text in sections:
    h = head.lower()
    if h.startswith("abstract"):
        abstract = "\n\n".join(paragraphs(text))
    elif h.startswith("table "):
        ncol = len(md_table(text)[0])
        if ncol <= 3:   # 단(column) float. 실측상 전폭 table*보다 본문 줄을 덜 먹는다.
            tables.append(table_env(head, text, f"tab:t{len(tables)+1}",
                                    ">{\\raggedright\\arraybackslash}p{0.22\\columnwidth}"
                                    ">{\\raggedright\\arraybackslash}p{0.43\\columnwidth}"
                                    ">{\\raggedright\\arraybackslash}p{0.29\\columnwidth}",
                                    "footnotesize", env="table", place="[t]"))
        else:
            w = 0.92 / ncol
            tables.append(table_env(head, text, f"tab:t{len(tables)+1}",
                                    "".join(f"p{{{w:.3f}\\textwidth}}" for _ in range(ncol)),
                                    "footnotesize", env="table*", place="[t]"))
    elif h.startswith("figure legend"):
        continue
    elif h.startswith("references"):
        items = [inline(" ".join(l.split()))
                 for l in text.split("\n") if l.strip().startswith("[")]
        refs = ("\\section*{References}\n\\begin{refs}\n"
                + "\n".join(f"\\item {it}" for it in items) + "\n\\end{refs}\n")
    elif h.startswith("appendix"):
        bits = re.split(r"^### ", text, flags=re.M)
        for b in bits[1:]:
            hh, _, tt = b.partition("\n")
            hh = re.sub(r"^[A-Z]\.\s*", "", hh.strip())
            appendix.append(f"\\section{{{inline(hh)}}}\n" + blocks(tt) + "\n")
    else:
        name = re.sub(r"^\d+\.?\s*", "", head)                 # "1. Introduction" -> "Introduction"
        main.append(f"\\section{{{inline(name)}}}\n{subsections(text)}\n")

# 표는 처음 참조되는 소절 근처에 끼워 넣는다. Conclusion 뒤에 몰아 두면 전폭 float이
# 참고문헌 뒤 페이지로 밀려 본문에서 표를 볼 수 없다.
for i, block in enumerate(main):
    if block.startswith("\\section{Results}"):
        block = block.replace("\\section{Results}\n", "\\section{Results}\n" + FIG, 1)
        if tables:
            # 소제목 문구에 의존하지 않는다. 끝에서 두 번째 소절 앞에 끼운다
            # (표를 처음 참조하는 마지막 소절보다 한 칸 앞).
            pos = [m.start() for m in re.finditer(r"\\subsection\{", block)]
            if not pos:
                sys.exit("Results 소절을 찾지 못해 본문 표를 배치할 수 없다")
            at = pos[-2] if len(pos) >= 2 else pos[-1]
            block = block[:at] + "".join(tables) + block[at:]
        main[i] = block
        break
else:
    sys.exit("Results 절을 찾지 못했다")
tables = []      # 본문에 이미 끼워 넣었으므로 뒤에 다시 붙이지 않는다

PRE = r"""\PassOptionsToPackage{sort}{natbib}
\PassOptionsToPackage{hidelinks}{hyperref}
\documentclass[pmlr,twocolumn,10pt]{jmlr}

\usepackage{booktabs,array,graphicx}
\usepackage{enumitem}
\usepackage{xurl}

\newlist{refs}{enumerate}{1}
\setlist[refs]{label=,leftmargin=1.1em,itemindent=-1.1em,
               nosep,itemsep=1pt,font=\footnotesize}

\jmlryear{2026}
\jmlrworkshop{Machine Learning for Health (ML4H) 2026}
\jmlrvolume{}

\title[Reliability map for multiome velocity outputs]{TITLE}

% Double-blind: no author names, affiliations or emails. Do not edit this block
% before submission; identifying information here is a desk-rejection risk.
\author{\Name{Anonymous Author(s)}}

\begin{document}
\maketitle

\begin{abstract}
ABSTRACT
\end{abstract}

MAIN
TABLES
REFS

\appendix
\onecolumn
APPENDIX
\end{document}
"""

tex = (PRE.replace("TITLE", inline(title))
          .replace("ABSTRACT", abstract)
          .replace("MAIN", "\n".join(main))
          .replace("TABLES", "\n".join(tables))
          .replace("REFS", refs)
          .replace("APPENDIX", "\n".join(appendix)))
tex = re.sub(r'"([^"\n]+)"', r"``\1''", tex)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write(tex)

leftover = sorted({c for c in tex if ord(c) > 127})
print("wrote", OUT, "|", len(tex), "chars")
print("sections:", len(main), "| tables:", len(tables), "| appendix:", len(appendix))
print("non-ASCII left:", [(c, unicodedata.name(c, "?")) for c in leftover] or "none")
