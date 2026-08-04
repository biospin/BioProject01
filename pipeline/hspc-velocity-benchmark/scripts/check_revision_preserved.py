#!/usr/bin/env python3
"""check_revision_preserved.py — 수정 단계 숫자·인용 보존 가드 (BIOP01-81 항목 1).

'고치되 다시 쓰지 마라'의 자동 확인. critic/reviewer 지적을 반영하는 **수정** 단계에서
manuscript-writer는 원고를 Write로 통째 재작성하지 않고 Edit로 외과적 패치만 한다
(하네스 규율 — .claude/agents/manuscript-writer.md, paper-production-orchestrator SKILL).

이 스크립트는 수정 **전 baseline**과 수정 **후 현재본**을 대조해, 검증이 끝난
헤드라인 숫자(소수·과학표기·p값·n)와 인용 마커([n])가 수정 중 조용히 사라지거나
바뀌었는지 surface한다. 도구 권한만으로는 못 막는 "값이 다른 값으로 바뀐" 경우를 잡는다.

baseline 기본값 = git HEAD 판본. --baseline <file> 로 직접 지정 가능.
자동 PASS를 신뢰하지 않는다(다른 QA 도구와 같은 결). exit 1이면 사람이 확인한다.

사용:
  python3 scripts/check_revision_preserved.py                       # draft_v2.md, draft_v2_ko.md vs git HEAD
  python3 scripts/check_revision_preserved.py --doc manuscript/draft_v2.md
  python3 scripts/check_revision_preserved.py --doc a.md --baseline b.md --json /tmp/r.json
종료코드: 0 = 헤드라인 숫자·인용 보존, 1 = 사라지거나 바뀐 것 있음(리뷰 필요), 2 = baseline 없음.
"""
from __future__ import annotations
import argparse, json, re, subprocess, sys
from collections import Counter
from pathlib import Path

BENCH = Path(__file__).resolve().parents[1]

# 헤드라인 토큰: 부호 포함 소수, 과학표기(p값), n=정수, 인용 마커 [n]
RE_DECIMAL = re.compile(r'[+\-−–]?\d+\.\d+')
RE_SCI     = re.compile(r'\b\d+(?:\.\d+)?[eE][+\-]?\d+\b')      # 1e-6, 2.3E-4
RE_N       = re.compile(r'\bn\s*=\s*\d+', re.IGNORECASE)
RE_CITE    = re.compile(r'\[\d+(?:\s*[,\-–]\s*\d+)*\]')          # [12], [3,4], [5-7]

def norm(s: str) -> str:
    return s.replace('−', '-').replace('–', '-')

def is_claimish(line: str, start: int, end: int) -> bool:
    """DOI·날짜ID·버전·연도류 소수는 헤드라인 숫자로 보지 않는다 (check_manuscript_numbers.py와 같은 결)."""
    if end < len(line) and line[end] in "./":
        return False
    pre = line[max(0, start - 4):start]
    if pre.endswith("10.") or pre.endswith("/"):
        return False
    tok = line[start:end]
    try:
        v = abs(float(norm(tok).replace('+', '')))
    except ValueError:
        return True
    if 1900 <= v <= 2035:
        return False
    return True

def extract(text: str) -> Counter:
    """헤드라인 토큰의 멀티셋."""
    c: Counter = Counter()
    for raw in text.splitlines():
        line = norm(raw)
        for m in RE_DECIMAL.finditer(line):
            if is_claimish(line, m.start(), m.end()):
                c[('num', m.group().replace('+', ''))] += 1
        for m in RE_SCI.finditer(line):
            c[('sci', m.group().lower())] += 1
        for m in RE_N.finditer(line):
            c[('n', re.sub(r'\s+', '', m.group().lower()))] += 1
        for m in RE_CITE.finditer(line):
            c[('cite', re.sub(r'\s+', '', m.group()))] += 1
    return c

def git_head_version(rel_path: str) -> str | None:
    try:
        out = subprocess.run(
            ["git", "-C", str(BENCH.parents[1]), "show", f"HEAD:{rel_path}"],
            capture_output=True, text=True, check=True)
        return out.stdout
    except subprocess.CalledProcessError:
        return None

def check_one(doc: Path, baseline_text: str) -> dict:
    cur = extract(doc.read_text(errors="ignore"))
    base = extract(baseline_text)
    removed = base - cur          # baseline에 있었는데 현재본에서 사라진(=바뀐/삭제된) 토큰
    added = cur - base
    def fmt(counter):
        return sorted(f"{kind}:{val}×{n}" for (kind, val), n in counter.items())
    return {
        "doc": str(doc.relative_to(BENCH)) if str(doc).startswith(str(BENCH)) else str(doc),
        "removed": fmt(removed),       # ← 검증된 값이 사라짐: 위험
        "added": fmt(added),           # ← 새로 등장(수정에서 추가됐을 수 있음): 참고
        "removed_count": sum(removed.values()),
    }

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--doc", action="append",
                    help="검사할 원고(반복 가능). 기본: manuscript/draft_v2.md, draft_v2_ko.md")
    ap.add_argument("--baseline", help="baseline 파일(미지정 시 git HEAD 판본)")
    ap.add_argument("--json", help="결과 JSON 출력 경로")
    args = ap.parse_args()

    docs = args.doc or ["manuscript/draft_v2.md", "manuscript/draft_v2_ko.md"]
    results, missing_baseline = [], []
    for d in docs:
        doc = (BENCH / d) if not Path(d).is_absolute() else Path(d)
        if not doc.exists():
            print(f"  SKIP (원고 없음): {d}", file=sys.stderr); continue
        if args.baseline:
            baseline_text = Path(args.baseline).read_text(errors="ignore")
        else:
            rel = str(doc.relative_to(BENCH.parents[1]))
            baseline_text = git_head_version(rel)
            if baseline_text is None:
                missing_baseline.append(d); continue
        results.append(check_one(doc, baseline_text))

    if args.json:
        Path(args.json).write_text(json.dumps(
            {"results": results, "missing_baseline": missing_baseline},
            ensure_ascii=False, indent=2))

    if missing_baseline:
        print(f"⚠ baseline 없음(신규 파일이거나 커밋 전): {', '.join(missing_baseline)}", file=sys.stderr)
    flagged = False
    for r in results:
        if r["removed_count"]:
            flagged = True
            print(f"⚠ {r['doc']}: 수정 중 사라지거나 바뀐 헤드라인 토큰 {r['removed_count']}개")
            for item in r["removed"]:
                print(f"    - {item}")
        else:
            print(f"✓ {r['doc']}: 헤드라인 숫자·인용 보존됨")
    if missing_baseline and not results:
        return 2
    return 1 if flagged else 0

if __name__ == "__main__":
    raise SystemExit(main())
