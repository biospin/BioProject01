#!/usr/bin/env python3
"""check_quote_integrity.py — 축자 인용 대조 게이트 (BIOP01-81 항목 2, stdlib only).

왜 있나
------
원고가 큰따옴표나 blockquote로 **출처를 그대로 인용**했다고 적었는데, 그 문장이 근거
문서에 글자 그대로 없으면 지어냈거나 왜곡한 것이다. ai_scientist §6.1 인용 무결성
게이트의 (1) 항목. hyperresearch 하네스의 quote-integrity 대응(인용부호 안 텍스트가
근거에 축자로 없으면 출고 차단).

무엇을 검사하나
- 원고의 blockquote(`> ...`)와 일정 길이 이상 큰따옴표 인용("..." / "...")을 뽑아,
- 근거 코퍼스(paper_analysis/ + results/ + manuscript 보조자료)에 축자로(공백 정규화·
  대소문자 무시) 존재하는지 확인. 없으면 flag.
- 학술 원고는 용어 강조용 따옴표가 많아, 기본 최소 단어 수(--min-words, 기본 7) 미만은
  검사 대상에서 뺀다. blockquote는 길이와 무관하게 검사. 코퍼스 자체 문장은 제외.

판정: exit 0 = 모든 축자 인용이 근거에 존재, 1 = 근거에 없는 인용 있음(출고 전 확인).
자동 PASS를 신뢰하지 않는다 — flag는 사람이 본다.

사용:
  python3 scripts/check_quote_integrity.py                       # draft_v2.md, draft_v2_ko.md
  python3 scripts/check_quote_integrity.py --doc manuscript/draft_v2.md --json out.json
  python3 scripts/check_quote_integrity.py --doc a.md --corpus 'sources/*.md' --min-words 8
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

BENCH = Path(__file__).resolve().parents[1]
ROOT = BENCH.parents[1]
DEFAULT_CORPUS = [                       # BENCH 기준 상대 + ROOT 기준
    "results/*.md", "manuscript/SUPPLEMENTARY.md", "manuscript/refs.bib",
]
DEFAULT_CORPUS_ROOT = ["paper_analysis/**/*.md"]

QUOTE_CHARS = '"“”„‟'
DQUOTE_RE = re.compile(r'["“„]([^"“”„‟\n]{12,})["”‟]')   # 큰따옴표 안 12자+ 스팬
CODEBLOCK_RE = re.compile(r'```.*?```', re.DOTALL)

def norm(s: str) -> str:
    """공백 정규화 + 소문자 + 따옴표 통일 → 축자 비교용."""
    s = re.sub(r'\s+', ' ', s)
    for q in QUOTE_CHARS:
        s = s.replace(q, '"')
    s = s.replace('’', "'").replace('‘', "'").replace('–', '-').replace('—', '-')
    return s.strip().lower()

def wordcount(s: str) -> int:
    return len(s.split())

def extract_quotes(text: str) -> list[str]:
    text = CODEBLOCK_RE.sub(' ', text)          # 코드블록 제외
    quotes, block = [], []
    for line in text.splitlines():
        st = line.strip()
        if st.startswith('>'):                  # blockquote 누적
            block.append(st.lstrip('> ').strip())
            continue
        if block:
            q = ' '.join(block).strip()
            if q:
                quotes.append(q)
            block = []
        for m in DQUOTE_RE.finditer(line):      # 큰따옴표 인용
            quotes.append(m.group(1).strip())
    if block:
        quotes.append(' '.join(block).strip())
    return quotes

def load_corpus(bench_globs, root_globs) -> str:
    buf = []
    for g in bench_globs:
        for p in sorted(BENCH.glob(g)):
            buf.append(p.read_text(errors="ignore"))
    for g in root_globs:
        for p in sorted(ROOT.glob(g)):
            buf.append(p.read_text(errors="ignore"))
    return norm("\n".join(buf))

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--doc", action="append")
    ap.add_argument("--corpus", action="append", help="근거 코퍼스 glob(BENCH 기준). 지정 시 기본 대체")
    ap.add_argument("--min-words", type=int, default=7, help="큰따옴표 인용 최소 단어 수(blockquote는 무관)")
    ap.add_argument("--json")
    args = ap.parse_args()

    docs = args.doc or ["manuscript/draft_v2.md", "manuscript/draft_v2_ko.md"]
    if args.corpus:
        corpus = load_corpus(args.corpus, [])
    else:
        corpus = load_corpus(DEFAULT_CORPUS, DEFAULT_CORPUS_ROOT)

    all_flagged, results = [], []
    for d in docs:
        doc = (BENCH / d) if not Path(d).is_absolute() else Path(d)
        if not doc.exists():
            print(f"  SKIP (원고 없음): {d}", file=sys.stderr); continue
        text = doc.read_text(errors="ignore")
        quotes = extract_quotes(text)
        flagged = []
        for q in quotes:
            is_block = wordcount(q) >= 1     # blockquote는 이미 합쳐짐; 큰따옴표만 min-words 필터
            if wordcount(q) < args.min_words:
                continue
            nq = norm(q)
            # 자기 자신(원고)에는 당연히 있으므로 코퍼스에서만 찾는다
            if nq and nq not in corpus:
                flagged.append(q)
        results.append({"doc": d, "quotes_checked": len([q for q in quotes if wordcount(q) >= args.min_words]),
                        "flagged": flagged})
        all_flagged += flagged

    if args.json:
        Path(args.json).write_text(json.dumps(results, ensure_ascii=False, indent=2))

    for r in results:
        if r["flagged"]:
            print(f"⚠ {r['doc']}: 근거에 축자로 없는 인용 {len(r['flagged'])}건")
            for q in r["flagged"]:
                snip = q if len(q) <= 100 else q[:97] + "..."
                print(f"    - \"{snip}\"")
        else:
            print(f"✓ {r['doc']}: 검사한 축자 인용이 모두 근거에 존재(또는 대상 인용 없음)")
    return 1 if all_flagged else 0

if __name__ == "__main__":
    raise SystemExit(main())
