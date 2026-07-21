#!/usr/bin/env python3
"""bib_to_cites.py — BibTeX(.bib)를 verify_citations.py 입력 JSON으로 변환.

verify_citations.py는 JSON(인용 항목 리스트: title/first_author/all_authors/year/doi)을
받는다. 그러나 실제 원고는 대개 .bib를 쓴다(BIOP01 manuscript/refs.bib, 향후 BIOP02도).
이 어댑터가 그 간극을 메워 인용검증기를 두 프로젝트가 공유할 수 있게 한다.

여러 줄 필드·중첩 중괄호를 처리한다(앞선 조잡한 정규식이 여러 줄 author/title을 놓쳐
1저자·DOI를 빈값으로 만들어 verify_citations가 헛되이 NOT_FOUND를 냈던 문제 해결).

사용:
    python3 bib_to_cites.py refs.bib > cites.json
    python3 verify_citations.py cites.json --json verdict.json
"""
import sys, re, json


def split_entries(text):
    """@type{key, ...} 단위로 분리. 중첩 중괄호를 세어 엔트리 경계를 정확히 잡는다."""
    entries = []
    i = 0
    while True:
        at = text.find("@", i)
        if at == -1:
            break
        brace = text.find("{", at)
        if brace == -1:
            break
        depth, j = 0, brace
        while j < len(text):
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        entries.append(text[at:j + 1])
        i = j + 1
    return entries


def parse_fields(entry):
    """엔트리 본문에서 field = {value} / field = "value" 를 뽑는다. 여러 줄·중첩 중괄호 허용."""
    body = entry[entry.find("{") + 1:]           # key, 부터
    body = body[body.find(",") + 1:]              # 첫 콤마(=key 뒤) 이후가 필드
    fields = {}
    i = 0
    while i < len(body):
        m = re.match(r"\s*([A-Za-z_-]+)\s*=\s*", body[i:])
        if not m:
            break
        name = m.group(1).lower()
        i += m.end()
        if i >= len(body):
            break
        if body[i] == "{":                        # 중괄호 값: depth 세서 닫기
            depth, j = 0, i
            while j < len(body):
                if body[j] == "{":
                    depth += 1
                elif body[j] == "}":
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            val = body[i + 1:j]
            i = j + 1
        elif body[i] == '"':                      # 따옴표 값
            j = body.find('"', i + 1)
            val = body[i + 1:j]
            i = j + 1
        else:                                     # 중괄호/따옴표 없는 값(숫자 등)
            j = i
            while j < len(body) and body[j] not in ",\n":
                j += 1
            val = body[i:j]
            i = j
        fields[name] = re.sub(r"\s+", " ", val).strip()
        nxt = body.find(",", i)
        i = nxt + 1 if nxt != -1 else len(body)
    return fields


def family_name(one_author):
    """'Last, First' → Last / 'First Last' → Last."""
    a = one_author.strip()
    if not a:
        return ""
    if "," in a:
        return a.split(",")[0].strip()
    return a.split()[-1]


def convert(text):
    out = []
    for e in split_entries(text):
        if not re.match(r"\s*@\s*(article|inproceedings|incollection|book|misc|phdthesis|techreport|unpublished)", e, re.I):
            continue                              # @comment/@string 등 스킵
        f = parse_fields(e)
        authors = [a.strip() for a in re.split(r"\s+and\s+", f.get("author", "")) if a.strip()]
        y = f.get("year", "")
        ym = re.search(r"\d{4}", y)
        out.append({
            "title": f.get("title", ""),
            "first_author": family_name(authors[0]) if authors else "",
            "all_authors": authors,
            "year": int(ym.group()) if ym else None,
            "doi": f.get("doi", "").replace("https://doi.org/", "").strip(),
        })
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: bib_to_cites.py refs.bib > cites.json", file=sys.stderr)
        sys.exit(1)
    cites = convert(open(sys.argv[1], encoding="utf-8").read())
    json.dump(cites, sys.stdout, ensure_ascii=False, indent=1)
