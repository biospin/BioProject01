#!/usr/bin/env python
"""
참고문헌 통합 + 첫-등장-순 재번호 (BIOP01-61).

왜 스크립트인가: 사람 손으로 재번호하면 반드시 틀린다. 그리고 영/한 두 파일에
**같은 번호 체계**가 적용돼야 한다.

동작
  1) 본문의 기존 `[n]`·`[n,m]`을 토큰 `{{Rn}}`으로 바꾼다(참고문헌 목록은 건드리지 않음).
  2) 선정한 신규 후보를 앵커 문자열 뒤에 토큰 `{{Cn}}`으로 꽂는다.
  3) 본문을 앞에서부터 훑어 **첫 등장 순서대로** 최종 번호를 배정한다(Vancouver).
  4) 인접한 토큰들은 `[3,4,5]` 한 묶음으로 렌더링한다.
  5) 참고문헌 목록을 새 번호 순서로 다시 쓴다.

실행 전후로 검증한다: 본문 인용 집합 == 목록 집합, 번호가 1..N 연속, 영/한 동일 매핑.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
M = os.path.join(os.path.dirname(HERE), "manuscript")
CAND = os.path.join(M, "REFS_EXPANSION_CANDIDATES.md")

# ── 채택 목록: Tier A 24편 전부 + Tier B 선별 16편 = 40편 (26 + 40 = 66) ──────
TIER_B_SELECTED = ["C57", "C58", "C24", "C20", "C22", "C28", "C29", "C40",
                   "C42", "C17", "C36", "C35", "C49", "C50", "C6", "C45"]

# ── 앵커: (문자열 뒤에 인용을 붙인다). 영/한 각각. 전부 실재 확인된 부분문자열. ──
ANCHORS_EN = [
    ("unspliced and spliced mRNA",                              ["C1", "C24"]),
    ("frame the landscape",                                     ["C3", "C4", "C5", "C6"]),
    ("many velocity readouts fail even this",                   ["C15"]),
    ("with no universal winner",                                ["C49"]),
    ("The second face of reliability is external",              ["C17"]),
    ("SLAM-seq half-lives for degradation)",                    ["C25", "C26"]),
    ("not as findings but as candidates to be sorted by reliability", ["C47", "C50"]),
    ("The biological motivation is",                            ["C38", "C39", "C40"]),
    ("recovered from the GEX BAM by velocyto",                  ["C1"]),   # 도구로서 재인용
    ("GEX via STARsolo Velocyto raw",                           ["C58"]),
    ("ATAC aggregation differed by dataset provenance",         ["C18", "C19", "C20"]),
    ("scrublet applied",                                        ["C57"]),
    ("an RNA-only floor (scVelo dynamical model",               ["C2"]),
    ("Schwalb 2016 K562 TT-seq, GSE75792",                      ["C25"]),
    ("α-versus-Todorovski was 3/3 positive",                    ["C27"]),
    ("Reactome neutrophil degranulation",                       ["C43", "C45", "C46"]),
    ("day0 ATAC promoter and enhancer accessibility",           ["C22"]),
    ("the α-stiff/lag-sloppy *dissociation*, its cross-method reproducibility",               ["C31", "C33"]),
    ("*relative (practical)* non-identifiability of the lag direction", ["C32", "C35", "C36"]),
    ("was tested by **preregistration**", ["C48"]),
    ("equivalent to 0 by TOST",                                 ["C52"]),
    ("permutation FDR (gene-label shuffle null",                ["C51"]),
    ("metabolic labeling could yet render the lag identifiable", ["C28", "C29"]),
    ("a perturbation ground truth is the natural next step",    ["C42"]),
    ("The weak identifiability of the velocity switch-time itself",                         ["C16"]),
    ("trajectories read from them",                             ["C13"]),
]
ANCHORS_KO = [
    ("unspliced와 spliced mRNA의 균형",                          ["C1", "C24"]),
    ("이 지형을 이룬다",                                       ["C3", "C4", "C5", "C6"]),
    ("많은 velocity 판독값이 이 기준조차 통과하지 못함을 분명히 한다", ["C15"]),
    ("보편적 승자가 없음을 확립했지만",                            ["C49"]),
    ("신뢰도의 둘째 측면은 외부적이며",                            ["C17"]),
    ("SLAM-seq 반감기)",                                         ["C25", "C26"]),
    ("신뢰도로 분류할 후보로 다룬다",                         ["C47", "C50"]),
    ("생물학적 동기는",                                           ["C38", "C39", "C40"]),
    ("spliced/unspliced는 velocyto로 GEX BAM에서 복원",                                   ["C1"]),
    ("GEX는 STARsolo Velocyto raw",                              ["C58"]),
    ("ATAC 집계는 데이터셋 출처에 따라 달랐고",                    ["C18", "C19", "C20"]),
    ("scrublet 적용",                                            ["C57"]),
    ("RNA 전용 floor(scVelo dynamical 모델",                      ["C2"]),
    ("Schwalb 2016 K562 TT-seq, GSE75792",                       ["C25"]),
    ("α 대 Todorovski는 3/3 양수",                                ["C27"]),
    ("Reactome neutrophil degranulation",                        ["C43", "C45", "C46"]),
    ("day0 ATAC promoter/enhancer 접근성",                        ["C22"]),
    ("α-stiff/lag-sloppy *분리(dissociation)*, 그 방법 간 재현성 순서",           ["C31", "C33"]),
    ("*상대적(실질적)* 비식별성",                                  ["C32", "C35", "C36"]),
    ("**사전등록(preregistration)**으로 검정했다",               ["C48"]),
    ("TOST로 0과 동등",                                           ["C52"]),
    ("순열 FDR로 검정했다(유전자 라벨 shuffle 귀무",               ["C51"]),
    ("metabolic labeling이 시간차(lag)를 식별 가능하게 만들 여지",  ["C28", "C29"]),
    ("perturbation ground truth에 대해 검증하는 것이 자연스러운 다음 단계", ["C42"]),
    ("velocity 전환 시각 자체의 약한 식별가능성",                                    ["C16"]),
    ("거기서 읽는 궤적은 감사하지 않았으며",                        ["C13"]),
]


def parse_candidates():
    txt = open(CAND).read()
    out = {}
    for b in re.split(r"\n### ", txt)[1:]:
        head = b.split("\n", 1)[0]
        m = re.match(r"(C\d+) \[([AB])\] (.*)", head)
        if not m:
            continue
        cid, tier, _ = m.groups()
        body = b.split("\n", 1)[1]
        bib = []
        for line in body.split("\n"):
            if line.startswith("- **"):
                break
            if line.startswith("- ") or (bib and line.startswith("  ")):
                bib.append(line.lstrip("- ").strip())
        out[cid] = dict(tier=tier, bib=" ".join(bib))
    return out


def tokenize_body(body):
    """본문의 [n] / [n,m]을 {{Rn}} 토큰으로."""
    def rep(m):
        return "".join("{{R%d}}" % int(x) for x in re.split(r"\s*,\s*", m.group(1)))
    return re.sub(r"\[(\d+(?:\s*,\s*\d+)*)\]", rep, body)


def render(body, mapping):
    """토큰을 최종 번호로. 인접 토큰은 한 묶음으로."""
    def rep(m):
        nums = [mapping[t] for t in re.findall(r"\{\{(\w+)\}\}", m.group(0))]
        return "[" + ",".join(str(n) for n in sorted(set(nums))) + "]"
    return re.sub(r"(?:\{\{\w+\}\})+", rep, body)


def process(path, anchors, cands, adopted):
    src = open(path).read()
    # 본문과 참고문헌 목록 분리 (목록 = 첫 "[1] "로 시작하는 줄부터)
    m = re.search(r"^\[1\] ", src, re.M)
    assert m, f"{path}: 참고문헌 목록을 찾지 못함"
    body, reflist = src[:m.start()], src[m.start():]
    old = {int(n): t.strip() for n, t in
           re.findall(r"^\[(\d+)\] (.*?)$", reflist, re.M)}

    body = tokenize_body(body)
    # Genome Biology 초록은 무인용이다. 같은 문구가 초록과 본문에 함께 있으면
    # 앞쪽(초록)이 먼저 잡히므로, 삽입 탐색은 Background 이후에서만 한다.
    bg = re.search(r"^## Background", body, re.M)
    head, rest = (body[:bg.start()], body[bg.start():]) if bg else ("", body)
    missed = []
    for anchor, cids in anchors:
        cids = [c for c in cids if c in adopted]
        if not cids:
            continue
        if anchor not in rest:
            missed.append((anchor[:45], cids))
            continue
        rest = rest.replace(anchor, anchor + "".join("{{%s}}" % c for c in cids), 1)
    body = head + rest

    order = []
    for t in re.findall(r"\{\{(\w+)\}\}", body):
        if t not in order:
            order.append(t)
    mapping = {t: i + 1 for i, t in enumerate(order)}
    body = render(body, mapping)

    lines = []
    for t, n in sorted(mapping.items(), key=lambda kv: kv[1]):
        text = old[int(t[1:])] if t.startswith("R") else cands[t]["bib"]
        lines.append(f"[{n}] {text}")
    tail = re.search(r"\n\n(?!\[)(.*)$", reflist, re.S)
    out = body + "\n\n".join(lines) + ("\n" + tail.group(1) if tail else "\n")
    open(path, "w").write(out)
    return mapping, missed, len(mapping)


def main():
    cands = parse_candidates()
    adopted = set([c for c, v in cands.items() if v["tier"] == "A"]) | set(TIER_B_SELECTED)
    print(f"채택: Tier A {sum(1 for c in adopted if cands[c]['tier']=='A')} "
          f"+ Tier B {sum(1 for c in adopted if cands[c]['tier']=='B')} = {len(adopted)}편")

    res = {}
    for path, anchors, tag in ((os.path.join(M, "draft_v2.md"), ANCHORS_EN, "EN"),
                               (os.path.join(M, "draft_v2_ko.md"), ANCHORS_KO, "KO")):
        mapping, missed, n = process(path, anchors, cands, adopted)
        res[tag] = mapping
        print(f"\n[{tag}] 최종 참고문헌 {n}편")
        if missed:
            print(f"  !! 앵커 미발견 {len(missed)}건 — 이 인용은 들어가지 못했다:")
            for a, c in missed:
                print(f"     {c} <- '{a}'")

    same = res["EN"] == res["KO"]
    print(f"\n영/한 번호 매핑 동일: {'OK' if same else '불일치 — 확인 필요'}")
    if not same:
        for k in sorted(set(res["EN"]) | set(res["KO"])):
            if res["EN"].get(k) != res["KO"].get(k):
                print(f"   {k}: EN={res['EN'].get(k)} KO={res['KO'].get(k)}")
    json.dump({k: v for k, v in res.items()},
              open(os.path.join(M, "refs_number_map.json"), "w"), indent=1)
    return 0 if same else 1


if __name__ == "__main__":
    sys.exit(main())
