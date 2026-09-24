#!/usr/bin/env python3
"""00_all.md 재생성 — 개별 편 01~08을 순서대로 결합한다.

README 규율: `00_all.md` 는 파생물이다. 직접 고치지 말고 개별 편을 고친 뒤 이 스크립트를 돌린다.

2026-09-24 신설. 그전에는 손으로 붙였고, 그래서 개별 편을 고쳐도 합본이 따라오지 않는 일이
있었다(7/27에 멈춰 있던 사례, BIOP01-83). 결합 규칙은 당시 산출물에서 역설계해
바이트 단위로 재현되는 것을 확인한 뒤 고정했다.

실행: python3 blog/make_all.py [--check]
  --check  파일을 쓰지 않고 현재 00_all.md 와 일치하는지만 본다(종료코드 1 이면 불일치).
"""
import glob
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "00_all.md")
SEP = "\n\n---\n\n"
HEADER = (
    "# BIOP01 개발 블로그 — 전체 합본\n"
    "\n"
    "> 생성 2026-09-02. 개별 편 `01`~`08`을 순서대로 결합한 파일이다.\n"
    "> 정본은 각 개별 편이며, 이 합본은 파생물이다. 개별 편을 고치면 이 파일을 다시 만든다.\n"
    "\n---\n\n"
)


def build():
    parts = sorted(glob.glob(os.path.join(HERE, "0[1-8]_*.md")))
    if len(parts) != 8:
        sys.exit(f"개별 편이 8개가 아니다: {len(parts)}개 — {[os.path.basename(p) for p in parts]}")
    bodies = [io.open(p, encoding="utf-8").read().strip() for p in parts]
    return HEADER + SEP.join(bodies) + "\n", parts


def main():
    text, parts = build()
    if "--check" in sys.argv:
        cur = io.open(OUT, encoding="utf-8").read()
        if cur == text:
            print(f"일치 — {len(text):,}자, 개별 {len(parts)}편")
            return
        sys.exit(f"불일치 — 현재 {len(cur):,}자 대 재생성 {len(text):,}자. 합본을 다시 만들 것.")
    io.open(OUT, "w", encoding="utf-8").write(text)
    print(f"wrote {OUT}  {len(text):,}자  (개별 {len(parts)}편)")


if __name__ == "__main__":
    main()
