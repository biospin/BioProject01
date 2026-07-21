#!/usr/bin/env python
"""
이미 번호가 매겨진 원고에 **새 참고문헌을 끼워 넣고 전체를 재번호**한다 (BIOP01-61).

p12는 통합 시점(번호 없던 상태)에 한 번 쓰는 도구라 처리된 파일에 다시 돌리면
항목이 중복된다(실제로 66 -> 103이 된 적 있다). 이 스크립트는 **현재 상태에서**
동작한다: 기존 `[n]`을 토큰으로 되돌리고, 본문에 이미 박아 둔 `{{E1}}` 같은 신규
토큰과 함께 첫 등장 순으로 다시 번호를 매긴다.

신규 항목의 서지는 NEW에 적는다. 영/한 두 파일에 같은 매핑이 적용됐는지 검증한다.
"""
import json
import os
import re
import sys

M = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "manuscript")

# 본문에 미리 박아 둔 토큰 -> 서지(집안 양식: 6명 이하 전원 / 7명 이상 앞 3명 + et al.)
NEW = {
    "E1": "Chen EY, Tan CM, Kou Y, et al. Enrichr: interactive and collaborative HTML5 gene "
          "list enrichment analysis tool. *BMC Bioinformatics* 14(1), 128 (2013). "
          "doi:10.1186/1471-2105-14-128.",
    "E2": "Kuleshov MV, Jones MR, Rouillard AD, et al. Enrichr: a comprehensive gene set "
          "enrichment analysis web server 2016 update. *Nucleic Acids Research* 44(W1), "
          "W90–W97 (2016). doi:10.1093/nar/gkw377.",
    "E3": "Xie Z, Bailey A, Kuleshov MV, et al. Gene Set Knowledge Discovery with Enrichr. "
          "*Current Protocols* 1(3), e90 (2021). doi:10.1002/cpz1.90.",
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
