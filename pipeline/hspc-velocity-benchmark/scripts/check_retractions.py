#!/usr/bin/env python3
"""check_retractions.py — 인용 논문 철회(retraction) 조회 게이트 (BIOP01-81 항목 2, stdlib only).

왜 있나
------
검증된 인용이라도 나중에 철회될 수 있다. 어제 철회된 논문이 오늘 원고에 남아 있으면
출고 사고다. 그래서 출고 직전 refs.bib의 모든 DOI를 다시 조회해 철회 여부를 확인한다.
(ai_scientist §6.1 인용 무결성 게이트의 (3) 항목. hyperresearch 하네스의 retracted-citations 대응.)

설계 규율 (verify_citations.py와 동일)
- stdlib만(urllib/json). 외부 패키지 없음.
- **조회 실패는 절대 PASS가 아니다.** 네트워크 실패·DOI 미해결은 NEEDS_HUMAN(표면화)이지 조용한 OK가 아니다.
- 판정은 명시적. 철회는 하드 블록.

데이터 출처: OpenAlex `works/doi:{doi}` 의 `is_retracted` 불리언.

판정
  OK           is_retracted=false
  RETRACTED    is_retracted=true  → 출고 차단(하드 에러)
  NEEDS_HUMAN  조회 실패/미해결(네트워크·404) → 사람 확인

사용:
  python3 scripts/check_retractions.py                      # manuscript/refs.bib
  python3 scripts/check_retractions.py --bib manuscript/refs.bib --cache /tmp/retr.json --json out.json
종료코드: 0 = 전부 OK, 1 = NEEDS_HUMAN 있음(철회 없음), 2 = RETRACTED 있음(출고 차단).
"""
from __future__ import annotations
import argparse, json, re, sys, time, urllib.request, urllib.error, urllib.parse
from pathlib import Path

BENCH = Path(__file__).resolve().parents[1]
DOI_RE = re.compile(r'doi\s*=\s*[{"]\s*(?:https?://doi\.org/)?(10\.[^\s},"]+)', re.IGNORECASE)
KEY_RE = re.compile(r'@\w+\s*\{\s*([^,\s]+)')
OPENALEX = "https://api.openalex.org/works/doi:{doi}?select=id,is_retracted,display_name&mailto=biospinleader@gmail.com"

def parse_bib(text: str) -> list[dict]:
    """@article{key, ... doi = {..} ..} 항목에서 (key, doi) 추출."""
    entries, key = [], None
    for line in text.splitlines():
        mk = KEY_RE.match(line.strip())
        if mk:
            key = mk.group(1)
        md = DOI_RE.search(line)
        if md:
            entries.append({"key": key or "?", "doi": md.group(1).rstrip('.')})
    return entries

def lookup(doi: str, cache: dict) -> dict:
    if doi in cache:
        return cache[doi]
    url = OPENALEX.format(doi=urllib.parse.quote(doi, safe=""))
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            data = json.load(r)
        retr = data.get("is_retracted")
        if retr is True:
            res = {"verdict": "RETRACTED", "title": data.get("display_name", "")}
        elif retr is False:
            res = {"verdict": "OK", "title": data.get("display_name", "")}
        else:
            res = {"verdict": "NEEDS_HUMAN", "title": "", "note": "is_retracted 필드 없음"}
    except urllib.error.HTTPError as e:
        res = {"verdict": "NEEDS_HUMAN", "title": "", "note": f"HTTP {e.code} (DOI 미해결?)"}
    except Exception as e:  # noqa: BLE001 - 조회 실패는 PASS가 아니라 NEEDS_HUMAN
        res = {"verdict": "NEEDS_HUMAN", "title": "", "note": f"조회 실패: {type(e).__name__}"}
    cache[doi] = res
    return res

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bib", default="manuscript/refs.bib")
    ap.add_argument("--cache")
    ap.add_argument("--json")
    ap.add_argument("--sleep", type=float, default=0.1, help="요청 간 간격(초), 예의상 rate limit")
    args = ap.parse_args()

    bib = (BENCH / args.bib) if not Path(args.bib).is_absolute() else Path(args.bib)
    if not bib.exists():
        print(f"refs.bib 없음: {bib}", file=sys.stderr); return 2
    entries = parse_bib(bib.read_text(errors="ignore"))
    if not entries:
        print("DOI 항목을 찾지 못함(형식 확인 필요).", file=sys.stderr); return 1

    cache = {}
    if args.cache and Path(args.cache).exists():
        cache = json.loads(Path(args.cache).read_text())

    results = []
    for i, e in enumerate(entries):
        r = lookup(e["doi"], cache)
        results.append({**e, **r})
        if args.sleep and i < len(entries) - 1:
            time.sleep(args.sleep)

    if args.cache:
        Path(args.cache).write_text(json.dumps(cache, ensure_ascii=False, indent=2))
    if args.json:
        Path(args.json).write_text(json.dumps(results, ensure_ascii=False, indent=2))

    retracted = [r for r in results if r["verdict"] == "RETRACTED"]
    needs = [r for r in results if r["verdict"] == "NEEDS_HUMAN"]
    ok = [r for r in results if r["verdict"] == "OK"]

    for r in retracted:
        print(f"  ⛔ RETRACTED  {r['key']}  {r['doi']}  {r.get('title','')}")
    for r in needs:
        print(f"  ⚠ NEEDS_HUMAN {r['key']}  {r['doi']}  ({r.get('note','')})")
    print(f"\n합계: {len(results)} DOI — OK {len(ok)} / NEEDS_HUMAN {len(needs)} / RETRACTED {len(retracted)}")

    if retracted:
        print("출고 차단: 철회된 논문 인용. 제거하거나 철회를 명시해야 한다.", file=sys.stderr)
        return 2
    if needs:
        print("사람 확인 필요: 일부 DOI를 조회하지 못했다(자동 통과 아님).", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
