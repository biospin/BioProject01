#!/usr/bin/env python3
"""check_manuscript_numbers.py — 원고(draft_v2.md)의 수치가 근거 문서(FINDINGS/results)에 실재하는지 대조.

투고 전 사고 방지: 원고에만 있고 결과 문서엔 없는 수치(드리프트·오타·구버전 잔존·지어낸 값)를 잡는다.
WRITING_PLAN이 경고한 "FINDINGS 영문 절반 stale로 sealed 결과 누락" 류를 자동 탐지.
BIOP02 인용검증기와 같은 결의 QA — 단, 통과 판정은 사람이(자동 PASS 신뢰 금지).

사용:
  python3 scripts/check_manuscript_numbers.py                 # draft_v2.md vs results/*.md
  python3 scripts/check_manuscript_numbers.py --doc manuscript/draft_v2.md --json /tmp/n.json
종료코드: 0 = 미검출, 1 = 근거없는 수치 있음(리뷰 필요).
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

BENCH = Path(__file__).resolve().parents[1]
DEC = re.compile(r'[+\-−]?\d+\.\d+')            # 부호 포함 소수 (유니코드 마이너스 포함)
def norm(s): return s.replace('−', '-').replace('–', '-')

def load_sources(globs):
    corpus, files = "", []
    for g in globs:
        for p in sorted(BENCH.glob(g)):
            corpus += "\n" + norm(p.read_text(errors="ignore"))
            files.append(str(p.relative_to(BENCH)))
    return corpus, files

def claim_like(line, start, end):
    """수치가 '주장'스러운 문맥인지(DOI·날짜ID·버전·연도 배제)."""
    tok = line[start:end]
    # 뒤에 또 '.'/'/'가 오면 다분할 ID(DOI 10.1038/…, 날짜 2025.08.02, 버전) → 배제
    if end < len(line) and line[end] in "./":
        return False
    pre = line[max(0, start-4):start]
    if pre.endswith("10.") or pre.endswith("/"):           # DOI prefix
        return False
    v = abs(float(tok.replace('+', '').replace('−', '-')))
    if 1900 <= v <= 2035:                                   # 연도류
        return False
    return True

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--doc", default="manuscript/draft_v2.md")
    ap.add_argument("--src", nargs="*", default=["results/FINDINGS.md", "results/*.md"])
    ap.add_argument("--json", default=None)
    a = ap.parse_args()

    corpus, srcfiles = load_sources(a.src)
    src_signed = set(DEC.findall(corpus))
    src_bare = {n.lstrip('+-') for n in src_signed}

    doc = (BENCH / a.doc).read_text(errors="ignore")
    # References/Bibliography 이후는 인용 메타데이터(DOI·날짜)라 본문 주장 대조 대상 아님
    cut = re.search(r'(?im)^#{1,3}\s*(References|Bibliography|참고문헌)\b', doc)
    if cut:
        doc = doc[:cut.start()]
    misses = []
    for i, raw in enumerate(doc.splitlines(), 1):
        line = norm(raw)
        for m in DEC.finditer(line):
            tok, s, e = m.group(), m.start(), m.end()
            if not claim_like(line, s, e):
                continue
            if tok in src_signed or tok.lstrip('+-') in src_bare:
                continue
            misses.append({"line": i, "value": tok, "context": raw.strip()[:100]})

    print(f"원고: {a.doc}")
    print(f"근거 문서 {len(srcfiles)}개: {', '.join(srcfiles[:6])}{' …' if len(srcfiles)>6 else ''}")
    print(f"근거 소수값 {len(src_bare)}종\n")
    if not misses:
        print("✅ 원고의 모든 소수 수치가 근거 문서에 실재합니다(드리프트 없음).")
    else:
        print(f"⚠️ 근거 문서에 없는 원고 수치 {len(misses)}건 — 리뷰 필요(오타/구버전/드리프트/미반영 결과 가능):\n")
        for x in misses:
            print(f"  L{x['line']:<4} {x['value']:<9} | {x['context']}")
        print("\n(주의: CI 경계·파생값 등 정당한 미검출도 있을 수 있음 — 사람이 판정. 자동 PASS 신뢰 금지.)")
    if a.json:
        Path(a.json).write_text(json.dumps({"doc": a.doc, "sources": srcfiles,
            "n_source_values": len(src_bare), "misses": misses}, ensure_ascii=False, indent=2))
        print(f"\nJSON: {a.json}")
    sys.exit(1 if misses else 0)

if __name__ == "__main__":
    main()
