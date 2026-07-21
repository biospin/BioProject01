#!/usr/bin/env python
"""
참고문헌 표기를 집안 양식으로 통일한다 (BIOP01-61).

문제: 신규 편입분은 CrossRef 원문 그대로라 `La Manno Gioele, Soldatov Ruslan, …
"RNA velocity of single cells." *Nature* …` 형태인데, 기존 항목은 Vancouver 약자
`Li C, Virgilio MC, Collins KL, Welch JD. Multi-omic single-cell velocity models …`
형태다. 두 양식이 섞여 목록이 눈에 띄게 어긋나 보인다.

해결: DOI로 CrossRef를 **다시 조회해** family/given을 제대로 받아 약자로 만든다.
후보 파일에서 파싱한 문자열은 family와 given이 이미 뭉개져 있어 되돌릴 수 없다.

집안 양식 (기존 항목에서 관찰된 규칙):
  저자 6명 이하 = 전원, 7명 이상 = 앞 3명 + et al.
  제목은 따옴표 없이, 저널은 *이탤릭*, `vol(issue), pages (year). doi:…`

DOI로 조회되지 않는 항목(preprint 등)은 **건드리지 않고** 그대로 두고 보고한다.
숫자·번호는 바꾸지 않는다 — 표기만 손댄다.
"""
import json
import os
import re
import subprocess
import sys
import time

M = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "manuscript")
UA = "BioProject01 refs normalizer (cytogenai@gmail.com)"


def crossref(doi):
    try:
        out = subprocess.run(
            ["curl", "-s", "-H", f"User-Agent: {UA}", f"https://api.crossref.org/works/{doi}"],
            capture_output=True, text=True, timeout=30).stdout
        return json.loads(out)["message"]
    except Exception:
        return None


def initials(given):
    return "".join(p[0] for p in re.split(r"[\s\-\.]+", given or "") if p and p[0].isalpha())


def fmt_authors(auths):
    names = []
    for a in auths or []:
        fam, giv = a.get("family"), initials(a.get("given", ""))
        if not fam:
            continue
        names.append(f"{fam} {giv}".strip())
    if not names:
        return None
    return ", ".join(names) if len(names) <= 6 else ", ".join(names[:3]) + ", et al."


def fmt_entry(m, doi):
    au = fmt_authors(m.get("author"))
    if not au:
        return None
    title = re.sub(r"\s+", " ", (m.get("title") or [""])[0]).strip().rstrip(".")
    jr = (m.get("container-title") or [""])[0]
    vol, iss = m.get("volume"), m.get("issue")
    pg = m.get("page") or m.get("article-number")
    yr = (m.get("published", {}).get("date-parts") or [[None]])[0][0]
    loc = f"*{jr}*" if jr else ""
    if vol:
        loc += f" **{vol}**" if False else f" {vol}"
        if iss:
            loc += f"({iss})"
    if pg:
        loc += f", {pg}"
    if yr:
        loc += f" ({yr})"
    return f"{au}. {title}. {loc.strip()}. doi:{doi}."


def main():
    changed = total = skipped = 0
    report = []
    # 영문 정본에서 표준형을 만들고, 같은 번호의 한글본 항목에 그대로 복사한다
    p_en, p_ko = os.path.join(M, "draft_v2.md"), os.path.join(M, "draft_v2_ko.md")
    en, ko = open(p_en).read(), open(p_ko).read()
    m = re.search(r"^\[1\] ", en, re.M)
    body_en, ref_en = en[:m.start()], en[m.start():]
    m = re.search(r"^\[1\] ", ko, re.M)
    body_ko, ref_ko = ko[:m.start()], ko[m.start():]

    def fix(block):
        nonlocal changed, total, skipped
        out = []
        for line in block.split("\n"):
            mm = re.match(r"^\[(\d+)\] (.*)$", line)
            if not mm:
                out.append(line)
                continue
            n, text = mm.groups()
            total += 1
            # 이미 집안 양식이면(제목에 따옴표가 없으면) 건드리지 않는다
            if '"' not in text:
                out.append(line)
                continue
            d = re.search(r"doi:(10\.\S+?)\.?\s*$|doi:(10\.\S+)", text)
            doi = (d.group(1) or d.group(2)).rstrip(".") if d else None
            if not doi:
                skipped += 1
                report.append(f"[{n}] DOI 없음 — 수동 확인 필요: {text[:70]}")
                out.append(line)
                continue
            msg = crossref(doi)
            time.sleep(0.15)
            new = fmt_entry(msg, doi) if msg else None
            if not new:
                skipped += 1
                report.append(f"[{n}] CrossRef 조회 실패 — 그대로 둠: {doi}")
                out.append(line)
                continue
            changed += 1
            out.append(f"[{n}] {new}")
        return "\n".join(out)

    new_ref_en = fix(ref_en)
    # 한글본은 영문 정본의 최종 문자열을 번호로 맞춰 그대로 반영(서지는 언어 무관)
    std = dict(re.findall(r"^\[(\d+)\] (.*)$", new_ref_en, re.M))
    new_ref_ko = "\n".join(
        (f"[{mm.group(1)}] {std[mm.group(1)]}" if (mm := re.match(r"^\[(\d+)\] ", l)) and mm.group(1) in std else l)
        for l in ref_ko.split("\n"))

    open(p_en, "w").write(body_en + new_ref_en)
    open(p_ko, "w").write(body_ko + new_ref_ko)
    print(f"항목 {total}개 중 {changed}개를 집안 양식으로 통일, {skipped}개는 손대지 않음")
    for r in report:
        print("  !", r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
