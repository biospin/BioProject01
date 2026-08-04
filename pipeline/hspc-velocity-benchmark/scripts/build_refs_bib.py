#!/usr/bin/env python3
"""build_refs_bib.py — draft_v2.md의 손수 작성 참고문헌 목록([1]~[N])을 refs.bib로 재생성.

왜 필요한가
-----------
manuscript/README.md는 refs.bib를 "paper_analysis/*/<paper-id>/*.bib에서 모은다"고
적었으나, method 논문(scVelo·MultiVelo·chromVAR…)은 paper_analysis .bib가 없어 그 과정은
구조적으로 71개를 만들 수 없다(26에서 멈춤, BIOP01-52 jamie 지적). 진리원천은 본문
참고문헌 목록이며 jamie가 in-text [1]~[N]과 1:1(고아·누락 0)임을 확인했다. 그래서
목록을 파싱해 refs.bib를 만든다. 인용은 수동 번호 [27] 방식이라 cite key는 [N]에
맞출 필요가 없고, verify_citations.py가 쓰는 first_author·year·doi만 정확하면 된다.

형식 가정(목록 한 줄):
    [N] AUTHORS. TITLE. *JOURNAL* VOL(ISSUE), PAGES (YEAR). doi:DOI. [optional note]

사용:
    python3 build_refs_bib.py draft_v2.md > refs.bib
    # 검증: python3 bib_to_cites.py refs.bib | python3 verify_citations.py /dev/stdin
"""
import sys, re


def fmt_authors(s):
    """프로즈 저자열('Wu Y, Kong C, et al')을 BibTeX('Wu, Y and Kong, C and others')로.

    verify_citations는 first author family만 비교하므로 마지막 공백토큰=이니셜로 보고
    'Family, Initials'로 뒤집는다. 다어절 성(La Manno G)도 마지막 토큰만 이니셜로 처리.
    """
    s = re.sub(r'\bet\s+al\.?', 'et al', s)
    s = s.replace(' et al', ', et al')  # 콤마 구분 보장
    out = []
    for p in [x.strip() for x in s.split(',') if x.strip()]:
        if p.lower() == 'et al':
            out.append('others'); continue
        toks = p.split()
        # 마지막 토큰이 이니셜형(짧은 대문자 시작)일 때만 'Family, Initials'로 분리.
        # 'Open Science Collaboration' 같은 단체저자는 통째로 둔다.
        if len(toks) >= 2 and re.match(r'^[A-Z][A-Za-z.]{0,3}$', toks[-1]):
            out.append("%s, %s" % (' '.join(toks[:-1]), toks[-1]))
        else:
            out.append(p)  # 성 하나 또는 단체저자(Zhang, Wang, Open Science Collaboration)
    return ' and '.join(out)


def parse_reference_list(md_text):
    entries = []
    for line in md_text.splitlines():
        m = re.match(r'^\[(\d+)\]\s+(.*)$', line.strip())
        if not m:
            continue
        num, rest = int(m.group(1)), m.group(2).strip()
        # DOI: doi:10.xxx (공백·대괄호·괄호 앞에서 끊음 — 뒤따르는 (GSE…)·[note] 배제)
        doi = ''
        md = re.search(r'doi:\s*(10\.[^\s\[\]()]+)', rest)
        if md:
            doi = md.group(1).rstrip('.')
        # year: 괄호 안 4자리 중 마지막(발행연도가 보통 doi 앞 괄호)
        years = re.findall(r'\((\d{4})\)', rest)
        year = years[-1] if years else ''
        # authors: 첫 '. ' 앞까지 (제목 시작 전)
        idx = rest.find('. ')
        authors = rest[:idx].strip() if idx > 0 else rest
        after = rest[idx + 2:] if idx > 0 else ''
        # journal: *…* 이탤릭
        journal = ''
        mj = re.search(r'\*([^*]+)\*', rest)
        if mj:
            journal = mj.group(1).strip()
        # title: authors 뒤 ~ 저널(*) 또는 연도 괄호 앞
        title = after
        if mj:
            title = after[:after.find('*')]
        else:
            title = re.split(r'\s*\(\d{4}\)', after)[0]
        title = title.rstrip(' .').strip()
        # first author: 첫 콤마/ et al/ and 앞
        first_author = re.split(r',| et al| and ', authors)[0].strip()
        entries.append(dict(num=num, authors=fmt_authors(authors), first_author=first_author,
                            title=title, journal=journal, year=year, doi=doi))
    return entries


def to_bibtex(e):
    key = "ref%02d" % e['num']
    fields = [('author', e['authors']), ('title', e['title']),
              ('journal', e['journal']), ('year', e['year']), ('doi', e['doi'])]
    body = ",\n".join("  %s = {%s}" % (k, v) for k, v in fields if v)
    return "@article{%s,\n%s\n}" % (key, body)


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: build_refs_bib.py <draft_v2.md>")
    text = open(sys.argv[1], encoding='utf-8').read()
    entries = parse_reference_list(text)
    # 무결성: 번호가 1..N 연속인지, doi 결측이 몇 개인지 stderr로 보고
    nums = [e['num'] for e in entries]
    expected = list(range(1, (max(nums) if nums else 0) + 1))
    missing = sorted(set(expected) - set(nums))
    no_doi = [e['num'] for e in entries if not e['doi']]
    print("# generated from %s — %d entries (refs [1]..[%d])"
          % (sys.argv[1].split('/')[-1], len(entries), max(nums) if nums else 0))
    for e in entries:
        print(to_bibtex(e))
        print()
    sys.stderr.write("parsed %d entries; missing nums=%s; entries without doi=%s\n"
                     % (len(entries), missing or "none", no_doi or "none"))


if __name__ == '__main__':
    main()
