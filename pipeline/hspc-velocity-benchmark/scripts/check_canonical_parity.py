#!/usr/bin/env python3
"""check_canonical_parity.py — 모델2 정본 수치 파리티 게이트.

모델2에서 results/<base>.md(한국어 정본)·<base>.en.md(영문)는 사람이 관리하고,
<base>.gen.md(기계 산출)만 재계산 게이트로 byte 검증된다. 정본이 인용 근거가 되므로,
사람이 윤문·번역하며 수치를 지어내거나(예: .gen.md엔 없는 값) 표기를 바꾸면(0.193→0.19)
check_manuscript_numbers는 이를 못 잡는다(코퍼스 어딘가에 있으면 통과). 그 구멍을 이 게이트가 막는다.

규칙(수치·표기 형식 불변):
  - 정본/영문의 모든 수치 토큰은 대응 .gen.md에 **그대로(byte)** 존재해야 한다.
  - 없으면 FAIL(지어낸 수치 또는 반올림·형식 변경).
  - .gen.md에만 있고 정본에 없는 토큰은 NOTE(윤문 중 근거 누락 — 경고).

수치 토큰: 언어 독립(한/영 정본 공통). 정규식은 bilingual-trap 복구 절차와 동일.
실행: python3 scripts/check_canonical_parity.py [--strict]
  기본: invented가 있으면 rc=1. --strict: dropped(NOTE)도 rc=1.
"""
from __future__ import annotations
import re
import sys
import argparse
from pathlib import Path

RESULTS = Path(__file__).resolve().parents[1] / "results"
# 소수점 뒤에 숫자를 요구(마침표 아티팩트 "18." 방지) + 지수 표기. 언어 독립.
NUM = re.compile(r"[-+]?[0-9]+(?:\.[0-9]+)?(?:[eE]-?[0-9]+)?")


def tokens(path: Path) -> set[str]:
    return set(NUM.findall(path.read_text(encoding="utf-8")))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true",
                    help="dropped(정본에 빠진 기계 수치)도 실패로 취급")
    a = ap.parse_args()

    gens = sorted(RESULTS.glob("*.gen.md"))
    if not gens:
        print("check_canonical_parity: .gen.md 없음 — 모델2 대상 없음 (SKIP)")
        return 0

    fail = 0
    warn = 0
    for gen in gens:
        base = gen.name[:-len(".gen.md")]
        gset = tokens(gen)
        for suffix in (".md", ".en.md"):
            var = RESULTS / f"{base}{suffix}"
            if not var.exists():
                continue
            vset = tokens(var)
            invented = sorted(vset - gset)
            dropped = sorted(gset - vset)
            tag = "정본" if suffix == ".md" else "영문"
            if invented:
                fail += 1
                print(f"✗ FAIL {var.name} ({tag}): .gen.md에 없는 수치 {len(invented)}종 "
                      f"→ {', '.join(invented[:12])}{' …' if len(invented) > 12 else ''}")
            if dropped:
                warn += 1
                lvl = "✗ FAIL" if a.strict else "· NOTE"
                if a.strict:
                    fail += 1
                print(f"{lvl} {var.name} ({tag}): .gen.md에만 있는 수치 {len(dropped)}종"
                      f"{' (근거 누락 가능)' if not a.strict else ''}"
                      f" → {', '.join(dropped[:12])}{' …' if len(dropped) > 12 else ''}")
            if not invented and not dropped:
                print(f"✓ {var.name} ({tag}): 수치 토큰 {len(vset)}종 .gen.md와 일치")

    print(f"\ncheck_canonical_parity: {len(gens)}개 result, FAIL={fail}, NOTE={warn}")
    if fail:
        print("→ 정본/영문에 기계 근거(.gen.md) 밖 수치가 있음. 윤문·번역 시 수치·표기 형식은 불변이어야 한다.")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
