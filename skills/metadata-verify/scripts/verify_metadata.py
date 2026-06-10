#!/usr/bin/env python3
"""
verify_metadata.py
paper-info.yaml의 DOI·제목·연도·저널을 Crossref API + PubMed Eutils로 검증.

Usage:
  python3 verify_metadata.py analysis/<topic>/<paper-id>/        # 단일 paper
  python3 verify_metadata.py analysis/<topic>/<paper-id>/ --patch  # 자동 수정
  python3 verify_metadata.py --all                               # 전체 검증
  python3 verify_metadata.py --all --topic ctc-adc-liquid-biopsy # 토픽별
"""

import sys
import re
import argparse
import time
from pathlib import Path
from difflib import SequenceMatcher

import requests
import yaml

CROSSREF_BASE = "https://api.crossref.org/works"
PUBMED_ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_ESUMMARY = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
HEADERS = {"User-Agent": "PaperLens/1.0 (mailto:cytogenai@gmail.com)"}
REQUEST_DELAY = 0.5  # Crossref polite pool rate limit


def sim(a, b):
    return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()


def clean_doi(raw):
    """URL 형태의 DOI에서 순수 DOI 부분만 추출."""
    if not raw:
        return ""
    raw = str(raw).strip()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi.org/"):
        if raw.startswith(prefix):
            return raw[len(prefix):]
    return raw


def query_crossref_doi(doi):
    """DOI로 Crossref 조회. 성공 시 message dict, 실패 시 None."""
    try:
        time.sleep(REQUEST_DELAY)
        r = requests.get(f"{CROSSREF_BASE}/{doi}", headers=HEADERS, timeout=15)
        if r.status_code == 200:
            return r.json().get("message")
        return None
    except Exception:
        return None


def search_crossref_title(title, rows=5):
    """제목으로 Crossref 검색. 후보 item 리스트 반환."""
    try:
        time.sleep(REQUEST_DELAY)
        params = {
            "query.title": title,
            "rows": rows,
            "select": "DOI,title,author,published,container-title,type",
        }
        r = requests.get(CROSSREF_BASE, headers=HEADERS, params=params, timeout=15)
        if r.status_code == 200:
            return r.json().get("message", {}).get("items", [])
        return []
    except Exception:
        return []


def search_pubmed_by_doi(doi):
    """PubMed에서 DOI로 PMID + 메타데이터 조회."""
    try:
        time.sleep(REQUEST_DELAY)
        r = requests.get(PUBMED_ESEARCH, params={
            "db": "pubmed", "term": f'"{doi}"[AID]',
            "retmode": "json", "retmax": 3,
        }, headers=HEADERS, timeout=15)
        if r.status_code != 200:
            return None
        ids = r.json().get("esearchresult", {}).get("idlist", [])
        if not ids:
            return None
        pmid = ids[0]
        r2 = requests.get(PUBMED_ESUMMARY, params={
            "db": "pubmed", "id": pmid, "retmode": "json",
        }, headers=HEADERS, timeout=15)
        if r2.status_code == 200:
            rec = r2.json().get("result", {}).get(pmid, {})
            return {
                "pmid": pmid,
                "title": rec.get("title", ""),
                "source": rec.get("source", ""),
                "pubdate": rec.get("pubdate", ""),
            }
        return None
    except Exception:
        return None


def extract_crossref_fields(msg):
    """Crossref message에서 검증에 필요한 필드 추출."""
    titles = msg.get("title") or []
    title = titles[0] if titles else ""

    authors = msg.get("author") or []
    first_author = ""
    if authors:
        fa = authors[0]
        family = fa.get("family", "")
        given = fa.get("given", "")
        first_author = f"{family}, {given[0]}." if given else family

    date_parts = (msg.get("published") or {}).get("date-parts", [[None]])
    year = date_parts[0][0] if date_parts and date_parts[0] else None

    journals = msg.get("container-title") or []
    journal = journals[0] if journals else ""

    return {
        "doi": msg.get("DOI", ""),
        "title": title,
        "first_author": first_author,
        "year": year,
        "journal": journal,
        "doc_type": msg.get("type", ""),
    }


def load_yaml_safe(path):
    """헤더 주석(#)을 제거하고 YAML 파싱."""
    text = path.read_text(encoding="utf-8")
    lines = [l for l in text.split("\n") if not l.startswith("#")]
    return yaml.safe_load("\n".join(lines)) or {}


def verify_paper(paper_dir, auto_patch=False, quiet=False):
    paper_dir = Path(paper_dir)
    yaml_path = paper_dir / "paper-info.yaml"

    if not yaml_path.exists():
        return {"paper_id": paper_dir.name, "status": "error",
                "issues": [{"severity": "❌ error", "field": "yaml", "msg": "paper-info.yaml 없음"}]}

    data = load_yaml_safe(yaml_path)
    paper_id = data.get("paper_id", paper_dir.name)
    doi = clean_doi(data.get("doi") or data.get("doi_or_url", ""))
    title = data.get("title", "")
    year = data.get("year")
    venue = data.get("venue", "")

    issues = []
    suggestions = {}
    cf_fields = None

    # ── 1. DOI 검증 ──────────────────────────────────────────────
    if not doi:
        issues.append({"severity": "🟡 warning", "field": "doi", "msg": "DOI 없음 — title 검색으로 후보 DOI 탐색"})
        if title:
            candidates = search_crossref_title(title)
            for c in candidates:
                c_title = (c.get("title") or [""])[0]
                score = sim(title, c_title)
                if score >= 0.85:
                    cf_fields = extract_crossref_fields(c)
                    suggestions["doi"] = cf_fields["doi"]
                    suggestions["doi_confidence"] = round(score, 3)
                    issues.append({"severity": "🟡 suggestion", "field": "doi",
                                   "msg": f"후보 DOI (similarity={score:.2f}): {cf_fields['doi']}\n    제목: {c_title[:90]}"})
                    break
    else:
        cf_msg = query_crossref_doi(doi)

        if cf_msg is None:
            # Crossref에 없으면 PubMed 시도
            pm = search_pubmed_by_doi(doi)
            if pm:
                issues.append({"severity": "🟡 warning", "field": "doi",
                                "msg": f"Crossref 미등록, PubMed 확인됨 (PMID {pm['pmid']})"})
            else:
                issues.append({"severity": "🔴 critical", "field": "doi",
                                "msg": f"DOI Crossref·PubMed 모두 404: {doi}"})
                # 제목으로 역검색
                if title:
                    candidates = search_crossref_title(title)
                    for c in candidates:
                        c_title = (c.get("title") or [""])[0]
                        score = sim(title, c_title)
                        if score >= 0.80:
                            cf_fields = extract_crossref_fields(c)
                            suggestions["doi"] = cf_fields["doi"]
                            suggestions["doi_confidence"] = round(score, 3)
                            suggestions["title"] = cf_fields["title"]
                            if cf_fields["year"]:
                                suggestions["year"] = cf_fields["year"]
                            if cf_fields["journal"]:
                                suggestions["venue"] = cf_fields["journal"]
                            issues.append({"severity": "🟡 suggestion", "field": "doi",
                                           "msg": f"유사 논문 발견 (similarity={score:.2f}): DOI={cf_fields['doi']}\n    제목: {c_title[:90]}"})
                            break
        else:
            cf_fields = extract_crossref_fields(cf_msg)

            # ── 2. 제목 비교 ────────────────────────────────────
            cf_title = cf_fields["title"]
            if cf_title:
                title_sim = sim(title, cf_title)
                if title_sim < 0.85:
                    sev = "🔴 critical" if title_sim < 0.50 else "🟡 warning"
                    issues.append({"severity": sev, "field": "title",
                                   "msg": f"제목 불일치 (similarity={title_sim:.2f})\n    yaml    : {title[:90]}\n    crossref: {cf_title[:90]}"})
                    if title_sim < 0.85:
                        suggestions["title"] = cf_title

            # ── 3. 연도 비교 ────────────────────────────────────
            if cf_fields["year"] and year:
                if int(year) != int(cf_fields["year"]):
                    issues.append({"severity": "🟡 warning", "field": "year",
                                   "msg": f"연도 불일치: yaml={year}, crossref={cf_fields['year']}"})
                    suggestions["year"] = cf_fields["year"]

            # ── 4. 저널 비교 ────────────────────────────────────
            cf_journal = cf_fields["journal"]
            if cf_journal and venue:
                journal_sim = sim(venue, cf_journal)
                if journal_sim < 0.60:
                    issues.append({"severity": "🟡 warning", "field": "venue",
                                   "msg": f"저널 불일치: yaml={venue}, crossref={cf_journal}"})
                    suggestions["venue"] = cf_journal

    # ── 결과 정리 ──────────────────────────────────────────────────
    has_critical = any("critical" in i["severity"] for i in issues)
    has_warning = any("warning" in i["severity"] or "suggestion" in i["severity"] for i in issues)
    status = "critical" if has_critical else ("warning" if has_warning else "pass")

    result = {
        "paper_id": paper_id,
        "status": status,
        "issues": issues,
        "suggestions": {k: v for k, v in suggestions.items() if not k.endswith("_confidence")},
        "crossref": cf_fields,
    }

    if not quiet or status != "pass":
        _print_result(paper_id, status, issues, suggestions)

    if auto_patch and suggestions:
        patched = _patch_yaml(yaml_path, suggestions)
        if patched:
            result["patched"] = patched

    return result


def _print_result(paper_id, status, issues, suggestions):
    icons = {"pass": "✅", "warning": "🟡", "critical": "🔴", "error": "❌"}
    icon = icons.get(status, "❓")
    print(f"\n{'─'*60}")
    print(f"{icon} [{status.upper()}]  {paper_id}")
    if not issues:
        print("   메타데이터 검증 통과")
        return
    for iss in issues:
        for line_i, line in enumerate(iss["msg"].split("\n")):
            prefix = f"   {iss['severity']} [{iss['field']}] " if line_i == 0 else "      "
            print(f"{prefix}{line}")
    non_conf = {k: v for k, v in suggestions.items() if not k.endswith("_confidence")}
    if non_conf:
        print("   💡 수정 제안:")
        for k, v in non_conf.items():
            v_str = str(v)[:80] + ("..." if len(str(v)) > 80 else "")
            print(f"      {k}: {v_str}")


def _patch_yaml(yaml_path, suggestions):
    """paper-info.yaml 필드 자동 수정. 수정된 필드 목록 반환."""
    content = yaml_path.read_text(encoding="utf-8")
    patched = []

    field_patterns = {
        "doi": (r'^(doi:\s*)(.+)$', lambda v: v),
        "doi_or_url": (r'^(doi_or_url:\s*)(.+)$', lambda v: v),
        "year": (r'^(year:\s*)(\d+)', lambda v: str(v)),
        "venue": (r'^(venue:\s*)(.+)$', lambda v: v),
    }

    for field, value in suggestions.items():
        if field.endswith("_confidence"):
            continue

        if field == "doi":
            for pat_key in ("doi", "doi_or_url"):
                pattern, fmt = field_patterns[pat_key]
                new_val = fmt(value)
                new_content, n = re.subn(pattern, lambda m, nv=new_val: f"{m.group(1)}{nv}", content, flags=re.MULTILINE)
                if n:
                    content = new_content
            patched.append(f"doi → {value}")

        elif field == "title":
            m = re.search(r'^title:\s*(.+)$', content, re.MULTILINE)
            if m:
                safe_val = value.replace('"', '\\"')
                content = content[:m.start()] + f'title: "{safe_val}"' + content[m.end():]
                patched.append(f"title → {value[:60]}...")

        elif field in field_patterns:
            pattern, fmt = field_patterns[field]
            new_val = fmt(value)
            new_content, n = re.subn(pattern, lambda m, nv=new_val: f"{m.group(1)}{nv}", content, flags=re.MULTILINE)
            if n:
                content = new_content
                patched.append(f"{field} → {new_val}")

    if patched:
        yaml_path.write_text(content, encoding="utf-8")
        print(f"   ✏️  자동 수정: {', '.join(patched)}")

    return patched


def main():
    parser = argparse.ArgumentParser(
        description="PaperLens paper-info.yaml 메타데이터 검증 (Crossref + PubMed)"
    )
    parser.add_argument("target", nargs="?", help="paper directory 경로")
    parser.add_argument("--all", action="store_true", help="전체 analysis/ 일괄 검증")
    parser.add_argument("--topic", help="토픽 디렉토리명 (--all과 함께 사용)")
    parser.add_argument("--patch", action="store_true", help="불일치 자동 수정")
    parser.add_argument("--quiet", action="store_true", help="pass 항목 출력 생략")
    args = parser.parse_args()

    # analysis root 결정
    script_path = Path(__file__).resolve()
    analysis_root = script_path.parents[3] / "analysis"
    if not analysis_root.exists():
        analysis_root = Path.cwd() / "analysis"

    if args.all or (not args.target):
        # 전체 또는 토픽별 일괄 검증
        if args.topic:
            topic_dirs = [analysis_root / args.topic]
        else:
            topic_dirs = sorted(
                d for d in analysis_root.iterdir()
                if d.is_dir() and not d.name.startswith("_")
            )

        counts = {"pass": [], "warning": [], "critical": [], "error": []}
        total = 0
        for topic_dir in topic_dirs:
            if not topic_dir.is_dir():
                print(f"토픽 디렉토리 없음: {topic_dir}", file=sys.stderr)
                continue
            print(f"\n{'='*60}")
            print(f"토픽: {topic_dir.name}")
            for paper_dir in sorted(topic_dir.iterdir()):
                if not (paper_dir / "paper-info.yaml").exists():
                    continue
                total += 1
                r = verify_paper(paper_dir, auto_patch=args.patch, quiet=args.quiet)
                counts[r.get("status", "error")].append(r["paper_id"])

        print(f"\n{'='*60}")
        print(f"검증 완료: 총 {total}편")
        print(f"  ✅ pass    : {len(counts['pass'])}편")
        print(f"  🟡 warning : {len(counts['warning'])}편" +
              (f"  — {', '.join(counts['warning'])}" if counts['warning'] else ""))
        print(f"  🔴 critical: {len(counts['critical'])}편" +
              (f"  — {', '.join(counts['critical'])}" if counts['critical'] else ""))
        print(f"  ❌ error   : {len(counts['error'])}편" +
              (f"  — {', '.join(counts['error'])}" if counts['error'] else ""))

    elif args.target:
        target = Path(args.target)
        if not target.is_absolute():
            target = Path.cwd() / args.target
        verify_paper(target, auto_patch=args.patch, quiet=False)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
