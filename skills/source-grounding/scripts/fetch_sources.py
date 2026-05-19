#!/usr/bin/env python3
"""Fetch source files declared in a paper-info.yaml.

See skills/source-grounding/SKILL.md Part 4 for the full spec.

This is an MVP: it covers primary-URL fetch, PMC fallback for open-access
papers, abstract auto-fetch (PubMed / Crossref), url-only stubs, and a manual
download guide. Publisher-landing-page crawling and Sci-Hub fallback are
declared as stubs so the workflow shape is visible — extend later.

Usage:
    python3 fetch_sources.py analysis/<topic>/<paper-id>/paper-info.yaml
    python3 fetch_sources.py <yaml> --use-pmc
    python3 fetch_sources.py <yaml> --fetch-abstract
    python3 fetch_sources.py <yaml> --allow-scihub      # stub; prints guidance
    python3 fetch_sources.py <yaml> --dry-run
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import sys
from pathlib import Path
from typing import Any

try:
    import requests
    from ruamel.yaml import YAML
    from ruamel.yaml.error import YAMLError
except ImportError:
    print(
        "requests and ruamel.yaml are required. Install with: "
        "pip install -r skills/source-grounding/scripts/requirements.txt",
        file=sys.stderr,
    )
    sys.exit(1)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_TIMEOUT = 30
USER_AGENT = "BioProject01-fetch-sources/0.1 (cytogenai@gmail.com)"

PUBMED_EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
CROSSREF_BASE = "https://api.crossref.org/works"
PMC_PDF_TEMPLATE = "https://www.ncbi.nlm.nih.gov/pmc/articles/{pmc}/pdf/"

# Round-trip YAML so comments inside the body survive the round-trip.
yaml_io = YAML(typ="rt")
yaml_io.preserve_quotes = True
yaml_io.width = 4096  # don't wrap long URLs
# Block-style indentation that keeps list items indented under their key:
#   key:
#     - item                 (sequence=4, offset=2)
yaml_io.indent(mapping=2, sequence=4, offset=2)


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------


def http_get(
    url: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
    params: dict[str, str] | None = None,
) -> requests.Response | None:
    try:
        r = requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=timeout,
            allow_redirects=True,
            params=params,
        )
    except requests.RequestException:
        return None
    return r


def looks_like_pdf(content: bytes) -> bool:
    return content[:4] == b"%PDF"


# ---------------------------------------------------------------------------
# YAML load / save
# ---------------------------------------------------------------------------


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return yaml_io.load(f)


def save_yaml(data: Any, path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        yaml_io.dump(data, f)


# ---------------------------------------------------------------------------
# Source item helpers
# ---------------------------------------------------------------------------


def resolve_local(yaml_dir: Path, local_rel: str | None) -> Path | None:
    if not local_rel:
        return None
    # `local` is relative to the paper folder (yaml_dir).
    return (yaml_dir / local_rel).resolve()


def set_status(item: dict, new_status: str, note: str | None = None) -> None:
    item["status"] = new_status
    if note is not None:
        item["note"] = (item.get("note") or "") + (
            f" | {note}" if item.get("note") else note
        )


# ---------------------------------------------------------------------------
# Fetch primitives
# ---------------------------------------------------------------------------


def fetch_to_file(
    url: str,
    dest: Path,
    *,
    expect_pdf: bool = False,
    dry_run: bool = False,
) -> tuple[bool, str]:
    """Return (ok, note). Writes content to dest on success."""
    if dry_run:
        return True, f"dry-run (would fetch {url})"
    r = http_get(url)
    if r is None:
        return False, "network error"
    if r.status_code != 200:
        return False, f"HTTP {r.status_code}"
    if expect_pdf and not looks_like_pdf(r.content):
        ct = r.headers.get("Content-Type", "?")
        # Many publishers redirect PDF links to a JS landing page; that's the
        # paywall signal we care about.
        return False, f"not a PDF (Content-Type={ct}) — likely paywall/landing"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(r.content)
    return True, "downloaded"


def write_url_stub(item: dict, dest: Path) -> None:
    """For status='url-only': write a small .url file that records the URL."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    body = [f"URL: {item.get('url', '')}"]
    if item.get("note"):
        body.append(f"Note: {item['note']}")
    if item.get("type"):
        body.append(f"Type: {item['type']}")
    dest.write_text("\n".join(body) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Fallback: PubMed / PMC
# ---------------------------------------------------------------------------


def doi_to_pmid(doi: str) -> str | None:
    r = http_get(
        f"{PUBMED_EUTILS}/esearch.fcgi",
        params={"db": "pubmed", "term": doi, "retmode": "json"},
    )
    if r is None or r.status_code != 200:
        return None
    try:
        ids = r.json().get("esearchresult", {}).get("idlist", [])
        return ids[0] if ids else None
    except ValueError:
        return None


def pmid_to_pmc(pmid: str) -> str | None:
    r = http_get(
        f"{PUBMED_EUTILS}/elink.fcgi",
        params={"dbfrom": "pubmed", "db": "pmc", "id": pmid, "retmode": "json"},
    )
    if r is None or r.status_code != 200:
        return None
    try:
        for ls in r.json().get("linksets", []):
            for db in ls.get("linksetdbs", []):
                if db.get("dbto") == "pmc":
                    links = db.get("links", [])
                    if links:
                        return str(links[0])
    except ValueError:
        pass
    return None


def fetch_via_pmc(doi: str, dest: Path, *, dry_run: bool = False) -> tuple[bool, str]:
    if not doi:
        return False, "no DOI for PMC lookup"
    pmid = doi_to_pmid(doi)
    if not pmid:
        return False, "no PMID found for DOI"
    pmc = pmid_to_pmc(pmid)
    if not pmc:
        return False, "no PMC ID (not open-access via PMC)"
    pmc_normalized = pmc if str(pmc).startswith("PMC") else f"PMC{pmc}"
    pdf_url = PMC_PDF_TEMPLATE.format(pmc=pmc_normalized)
    return fetch_to_file(pdf_url, dest, expect_pdf=True, dry_run=dry_run)


# ---------------------------------------------------------------------------
# Abstract auto-fetch
# ---------------------------------------------------------------------------


def fetch_abstract_pubmed(doi: str) -> str | None:
    pmid = doi_to_pmid(doi)
    if not pmid:
        return None
    r = http_get(
        f"{PUBMED_EUTILS}/efetch.fcgi",
        params={"db": "pubmed", "id": pmid, "rettype": "abstract", "retmode": "text"},
    )
    if r is None or r.status_code != 200 or not r.text.strip():
        return None
    return r.text


def fetch_abstract_crossref(doi: str) -> str | None:
    r = http_get(f"{CROSSREF_BASE}/{doi}")
    if r is None or r.status_code != 200:
        return None
    try:
        msg = r.json().get("message", {})
        abs_html = msg.get("abstract")
        if not abs_html:
            return None
        # Crossref abstracts often contain JATS XML tags; strip naively.
        import re

        return re.sub(r"<[^>]+>", "", abs_html).strip()
    except ValueError:
        return None


def fetch_abstract(doi: str) -> tuple[str, str] | None:
    """Return (source_name, text) or None."""
    text = fetch_abstract_pubmed(doi)
    if text:
        return "pubmed", text
    text = fetch_abstract_crossref(doi)
    if text:
        return "crossref", text
    return None


# ---------------------------------------------------------------------------
# Stubs: publisher landing page and Sci-Hub
# ---------------------------------------------------------------------------


def fetch_via_publisher_landing(doi: str, dest: Path) -> tuple[bool, str]:
    """STUB. Each publisher's landing page has its own structure; needs
    per-publisher selectors (Nature, Cell, Science, MDPI, eLife, ...). For
    now we just return False so the caller advances to the next fallback."""
    return False, "publisher landing page parser not implemented (stub)"


def fetch_via_scihub(doi: str, dest: Path) -> tuple[bool, str]:
    """STUB. Sci-Hub domain rotates; user must set SCIHUB_BASE env var.
    Disabled unless --allow-scihub is passed and the env var is set.
    Legality is the user's responsibility."""
    base = os.environ.get("SCIHUB_BASE")
    if not base:
        return False, "SCIHUB_BASE env var not set"
    # Conservative: we DO NOT auto-scrape Sci-Hub here. Tell the user the
    # URL to try manually.
    return False, f"manual: try {base.rstrip('/')}/{doi}"


# ---------------------------------------------------------------------------
# Per-item dispatch
# ---------------------------------------------------------------------------


def process_paper(
    item: dict,
    yaml_dir: Path,
    *,
    doi: str | None,
    use_pmc: bool,
    allow_scihub: bool,
    dry_run: bool,
) -> str:
    """Drive paper.pdf through the fallback chain. Mutates `item`."""
    local = resolve_local(yaml_dir, item.get("local"))
    if local is None:
        return "skipped (no local path)"

    if item.get("status") == "downloaded" and local.exists():
        return "skip (already downloaded)"

    if item.get("status") == "url-only":
        write_url_stub(item, local)
        return "wrote .url stub"

    # 1. primary URL
    url = item.get("url")
    if url:
        ok, note = fetch_to_file(url, local, expect_pdf=True, dry_run=dry_run)
        if ok:
            set_status(item, "downloaded")
            return f"primary URL: {note}"
        primary_note = note
    else:
        primary_note = "no primary URL"

    # 2. publisher landing page (stub)
    if doi:
        ok, note = fetch_via_publisher_landing(doi, local)
        if ok:
            set_status(item, "downloaded")
            return f"publisher landing: {note}"

    # 3. PMC (open access) if asked
    if use_pmc and doi:
        ok, note = fetch_via_pmc(doi, local, dry_run=dry_run)
        if ok:
            set_status(item, "downloaded")
            return f"PMC: {note}"
        pmc_note = note
    else:
        pmc_note = "PMC not attempted"

    # 4. Sci-Hub (opt-in stub)
    if allow_scihub and doi:
        ok, note = fetch_via_scihub(doi, local)
        if ok:
            set_status(item, "downloaded")
            return f"Sci-Hub: {note}"
        scihub_note = note
    else:
        scihub_note = "Sci-Hub skipped"

    # 5. author contact needed
    set_status(
        item,
        "author-contact-needed",
        note=f"primary: {primary_note} | pmc: {pmc_note} | scihub: {scihub_note}",
    )
    return f"all fallbacks failed → status=author-contact-needed"


def process_other(
    item: dict,
    yaml_dir: Path,
    *,
    expect_pdf: bool,
    dry_run: bool,
) -> str:
    """Supplementary / data / code items. Single-shot fetch only."""
    local = resolve_local(yaml_dir, item.get("local"))
    if local is None:
        return "skipped (no local path)"

    if item.get("status") == "downloaded" and local.exists():
        return "skip (already downloaded)"

    if item.get("status") == "url-only":
        write_url_stub(item, local)
        return "wrote .url stub"

    url = item.get("url")
    if not url:
        return "skipped (no url)"

    ok, note = fetch_to_file(url, local, expect_pdf=expect_pdf, dry_run=dry_run)
    if ok:
        set_status(item, "downloaded")
        return note
    set_status(item, "manual-needed", note=note)
    return f"failed → {note}"


# ---------------------------------------------------------------------------
# Manual download guide
# ---------------------------------------------------------------------------


def print_manual_guide(data: dict, yaml_path: Path) -> None:
    rows = []

    paper = data.get("sources", {}).get("paper")
    if paper and paper.get("status") not in ("downloaded", "url-only"):
        rows.append(("paper", paper))

    for s in data.get("sources", {}).get("supplementary", []) or []:
        if s.get("status") not in ("downloaded", "url-only"):
            rows.append((s.get("note") or "supplementary", s))

    if not rows:
        return

    print()
    print("=" * 60)
    print("수동 확보 필요 항목")
    print("=" * 60)

    doi = data.get("doi") or ""
    scihub_base = os.environ.get("SCIHUB_BASE", "https://sci-hub.se")

    for label, item in rows:
        local = item.get("local", "?")
        url = item.get("url", "(no URL)")
        note = item.get("note", "")
        print(f"\n[{label}]")
        print(f"  Primary URL: {url}")
        print(f"  Local 저장 위치: {(yaml_path.parent / local).relative_to(REPO_ROOT)}")
        if note:
            print(f"  Status note: {note}")
        if doi:
            print(f"  PubMed 검색: https://pubmed.ncbi.nlm.nih.gov/?term={doi}")
            print(f"  Sci-Hub 시도: {scihub_base.rstrip('/')}/{doi}")

    print()
    print("권장 순서: PubMed/PMC → publisher 직접 → Sci-Hub → 저자 contact")
    print("(corresponding author 이메일은 paper-info.yaml에 별도 기록 권장)")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch source files for a paper-info.yaml")
    parser.add_argument("yaml_path", type=Path, help="path to paper-info.yaml")
    parser.add_argument("--use-pmc", action="store_true", help="Try PubMed PMC fallback when primary URL fails")
    parser.add_argument("--allow-scihub", action="store_true", help="Show Sci-Hub URL in manual guide (does NOT auto-scrape)")
    parser.add_argument("--fetch-abstract", action="store_true", help="Fetch abstract.txt via PubMed/Crossref")
    parser.add_argument("--dry-run", action="store_true", help="Do not write files; show what would happen")
    parser.add_argument("--verbose", action="store_true", help="Print progress")
    args = parser.parse_args()

    yaml_path = args.yaml_path.resolve()
    if not yaml_path.exists():
        print(f"not found: {yaml_path}", file=sys.stderr)
        return 1

    try:
        data = load_yaml(yaml_path)
    except YAMLError as e:
        print(f"yaml parse error: {e}", file=sys.stderr)
        return 1

    yaml_dir = yaml_path.parent
    doi = data.get("doi")
    sources = data.get("sources") or {}

    # Paper
    if "paper" in sources:
        outcome = process_paper(
            sources["paper"],
            yaml_dir,
            doi=doi,
            use_pmc=args.use_pmc,
            allow_scihub=args.allow_scihub,
            dry_run=args.dry_run,
        )
        if args.verbose or "failed" in outcome or "author-contact" in outcome:
            print(f"paper: {outcome}")

    # Supplementary
    for i, supp in enumerate(sources.get("supplementary", []) or []):
        outcome = process_other(supp, yaml_dir, expect_pdf=False, dry_run=args.dry_run)
        if args.verbose or outcome.startswith("failed"):
            print(f"supplementary[{i}]: {outcome}")

    # Data and code: typically url-only
    for kind in ("data", "code"):
        for i, item in enumerate(sources.get(kind, []) or []):
            outcome = process_other(item, yaml_dir, expect_pdf=False, dry_run=args.dry_run)
            if args.verbose:
                print(f"{kind}[{i}]: {outcome}")

    # Abstract (optional)
    if args.fetch_abstract:
        if not doi:
            print("--fetch-abstract: no DOI in paper-info.yaml, skipping")
        else:
            abs_dir = yaml_dir / "sources"
            abs_dest = abs_dir / "abstract.txt"
            if abs_dest.exists() and not args.dry_run:
                print(f"abstract: already exists at {abs_dest.relative_to(REPO_ROOT)}")
            else:
                result = fetch_abstract(doi)
                if result is None:
                    print("abstract: not found via PubMed/Crossref")
                else:
                    source_name, text = result
                    if args.dry_run:
                        print(f"abstract: dry-run (would write via {source_name})")
                    else:
                        abs_dir.mkdir(parents=True, exist_ok=True)
                        abs_dest.write_text(text, encoding="utf-8")
                        # also reflect in yaml
                        sources.setdefault("abstract_text", {})
                        sources["abstract_text"].update(
                            {
                                "source": source_name,
                                "local": "sources/abstract.txt",
                                "status": "downloaded",
                            }
                        )
                        print(f"abstract: wrote {abs_dest.relative_to(REPO_ROOT)} (via {source_name})")

    # Update workflow.last_updated and save yaml
    if not args.dry_run:
        workflow = data.setdefault("workflow", {})
        workflow["last_updated"] = dt.date.today().isoformat()
        save_yaml(data, yaml_path)
        print(f"updated {yaml_path.relative_to(REPO_ROOT)}")

    print_manual_guide(data, yaml_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
