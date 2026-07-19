#!/usr/bin/env python
"""
**본문이 이름으로 부르는 출처인데 인용이 없는 곳**을 찾는다 (BIOP01-61).

기존 `verify_citations.py`와 방향이 반대다.
  verify_citations.py : 참고문헌 목록 -> CrossRef  ("내가 적은 문헌이 실존하나")
  이 스크립트         : 본문 -> 참고문헌 목록      ("이름을 부른 출처에 인용이 있나")

목록만 검사해서는 **목록에 없는 것**을 원리적으로 못 잡는다. 2026-07-19에 실제로
Schwalb·Todorovski·TOST·sloppy·scrublet·STARsolo·velocyto 등 12건이 이 구멍으로
빠져나갔다. 그래서 검사 축을 하나 더 둔다.

exit code 1 = 인용 없는 언급이 남아 있음(투고 전 해소 대상).
"""
import os
import re
import sys

M = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "manuscript")

# 본문에서 이름으로 불리면 인용이 따라야 하는 것들.
# (표시명, 정규식) — 새 도구·데이터·방법을 쓰면 여기 추가한다.
NAMED = [
    ("velocyto", r"velocyto"), ("scVelo", r"scVelo"), ("MultiVelo", r"MultiVelo\b"),
    ("MultiVeloVAE", r"MultiVeloVAE"), ("MoFlow", r"MoFlow"), ("CRAK-Velo", r"CRAK-Velo"),
    ("veloVI", r"veloVI"), ("veloVAE", r"veloVAE"), ("ConsensusVelo", r"ConsensusVelo"),
    ("scrublet", r"scrublet"), ("STARsolo", r"STARsolo"), ("CellRanger", r"[Cc]ell[Rr]anger"),
    ("ArchR", r"ArchR"), ("Signac", r"Signac"), ("Seurat", r"Seurat"), ("scanpy", r"[Ss]canpy"),
    ("TT-seq", r"TT-seq"), ("SLAM-seq", r"SLAM-seq"), ("Schwalb", r"Schwalb"),
    ("Todorovski", r"Todorovski"), ("Reactome", r"Reactome"), ("Enrichr", r"Enrichr"),
    ("TOST", r"TOST"), ("Benjamini-Hochberg", r"Benjamini|Hochberg"),
    ("sloppy/stiff", r"\bsloppy\b"), ("profile-likelihood", r"profile[- ]likelihood"),
    ("Mann-Whitney", r"Mann–Whitney|Mann-Whitney"), ("Spearman", r"Spearman"),
    ("dyngen", r"[Dd]yngen"), ("Palantir", r"Palantir"), ("SEACells", r"SEACells"),
]
# 인용을 요구하지 않는 것(통계 관용어 등). 여기 넣는 이유를 반드시 적을 것.
EXEMPT = {"Spearman", "Mann-Whitney"}   # 표준 통계량, 원논문 인용 관행 없음

WINDOW = 220   # 언급 지점 뒤 이 범위 안에 [n]이 있으면 인용된 것으로 본다


def check(path):
    s = open(path).read()
    m = re.search(r"^\[1\] ", s, re.M)
    body = s[:m.start()] if m else s
    bg = re.search(r"^## Background", body, re.M)
    body = body[bg.start():] if bg else body      # 초록은 무인용이 규약
    af = re.search(r"^## Additional files", body, re.M)   # 파일 캡션은 본문이 아니다
    if af:
        body = body[:af.start()]

    bad = []
    for name, pat in NAMED:
        if name in EXEMPT:
            continue
        hits = list(re.finditer(pat, body))
        if not hits:
            continue
        cited = any(re.search(r"\[\d", body[h.start():h.start() + WINDOW]) for h in hits)
        if not cited:
            h = hits[0]
            bad.append((name, len(hits), body[max(0, h.start() - 60):h.start() + 60]
                        .replace("\n", " ")))
    return bad


def main():
    fail = 0
    for f in ("draft_v2.md", "draft_v2_ko.md"):
        p = os.path.join(M, f)
        if not os.path.exists(p):
            continue
        bad = check(p)
        print(f"\n=== {f}: 인용 없는 언급 {len(bad)}건")
        for name, n, ctx in bad:
            print(f"  - {name} ({n}회)  …{ctx.strip()}…")
        fail += len(bad)
    print(f"\n{'통과' if fail == 0 else f'미해소 {fail}건 — 투고 전 처리할 것'}")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
