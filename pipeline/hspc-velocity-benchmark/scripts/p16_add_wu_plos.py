#!/usr/bin/env python
"""
Wu 2026(GB) + Ancheta 2026(PLOS Comput Biol) 두 참고문헌을 본문에 이미 박아 둔
{{W1}}·{{P1}} 토큰 위치에 넣고, 전체를 첫-등장-순으로 재번호한다 (스쿱 반영).

p15와 동일 로직(현재 상태에서 [n]→토큰 되돌려 재번호). NEW dict만 교체.
서지는 CrossRef 조회로 확정한 값, 집안 양식(6인 이하 전원 / 초과 et al.).
"""
import json
import os
import re
import sys

M = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "manuscript")

NEW = {
    "W1": "Wu Y, Kong C, Liao X, Lin Z, Sun X, Liu J. Comprehensive benchmarking of RNA "
          "velocity methods across single-cell datasets. *Genome Biology* 27(1), 242 (2026). "
          "doi:10.1186/s13059-026-04182-z.",
    "P1": "Ancheta S, Dorman L, Le Treut G, et al. Challenges and progress in RNA velocity: "
          "comparative analysis across multiple biological contexts. *PLoS Computational "
          "Biology* 22(6), e1014303 (2026). doi:10.1371/journal.pcbi.1014303.",
}


def process(path):
    s = open(path).read()
    m = re.search(r"^\[1\] ", s, re.M)
    assert m, f"{path}: 참고문헌 목록 없음"
    body, reflist = s[:m.start()], s[m.start():]
    old = dict(re.findall(r"^\[(\d+)\] (.*?)$", reflist, re.M))

    def tok(mm):
        return "".join("{{R%s}}" % x for x in re.split(r"\s*,\s*", mm.group(1)))
    body = re.sub(r"\[(\d+(?:\s*,\s*\d+)*)\]", tok, body)

    order = []
    for t in re.findall(r"\{\{(\w+)\}\}", body):
        if t not in order:
            order.append(t)
    mapping = {t: i + 1 for i, t in enumerate(order)}

    def render(mm):
        nums = sorted({mapping[t] for t in re.findall(r"\{\{(\w+)\}\}", mm.group(0))})
        return "[" + ",".join(map(str, nums)) + "]"
    body = re.sub(r"(?:\{\{\w+\}\})+", render, body)

    lines = [f"[{n}] {(old[t[1:]] if t.startswith('R') else NEW[t])}"
             for t, n in sorted(mapping.items(), key=lambda kv: kv[1])]
    tail = re.search(r"\n\n(?!\[)(.*)$", reflist, re.S)
    open(path, "w").write(body + "\n\n".join(lines) + ("\n" + tail.group(1) if tail else "\n"))
    return mapping


def main():
    res = {t: process(os.path.join(M, f))
           for t, f in (("EN", "draft_v2.md"), ("KO", "draft_v2_ko.md"))}
    n = len(res["EN"])
    print(f"최종 참고문헌 {n}편 (EN) / {len(res['KO'])}편 (KO)")
    same = res["EN"] == res["KO"]
    print("영/한 번호 매핑 동일:", "OK" if same else "불일치")
    if not same:
        for k in sorted(set(res["EN"]) | set(res["KO"])):
            if res["EN"].get(k) != res["KO"].get(k):
                print(f"  {k}: EN={res['EN'].get(k)} KO={res['KO'].get(k)}")
    json.dump(res, open(os.path.join(M, "refs_number_map.json"), "w"), indent=1)
    return 0 if same else 1


if __name__ == "__main__":
    sys.exit(main())
