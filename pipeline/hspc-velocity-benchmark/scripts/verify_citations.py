#!/usr/bin/env python3
"""verify_citations.py — self-built citation verifier (BIOP01·BIOP02 공용) (stdlib only).

Why this exists
---------------
The public medsci `verify-refs` skill catches ONLY first-author hallucination
(1 of our 5 real citation errors). Worse, it has a structural bug we must never
reproduce: when the DOI lookup fails it falls back to a weak PubMed title search
and returns `OK` if *anything* comes back (L557-560) -- so a fabricated DOI
passes more easily than no DOI at all.

Design rules enforced here:
  * stdlib only (urllib/json/re). `habanero` is not installed in this env.
  * A lookup FAILURE IS NEVER A PASS. DOI 404, 0 search hits, or 0 source
    authors can never yield VERIFIED.
  * Verdicts are explicit. There is no silent `OK`. Anything undecidable is
    NEEDS_HUMAN, which is a surfaced result, not a quiet pass.

Verdicts
--------
  VERIFIED           DOI resolved + first author matches + year matches
  AUTHOR_MISMATCH    cited first author != source first author
  YEAR_MISMATCH      |cited year - source year| >= 2
  NOT_FOUND          fabrication suspected: no DOI / DOI failed to resolve, and
                     the claimed first author is absent from the top-N search
  CLAIM_UNSUPPORTED  abstract does not support the attached claim
  NEEDS_HUMAN        undecidable (no abstract, 0 authors, year off by exactly 1)

Usage
-----
    python3 verify_citations.py cases.json [--cache cache.json] [--json out.json]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

UA = "velocity-verify-citations/1.0 (mailto:cytogenai@gmail.com)"
CROSSREF = "https://api.crossref.org/works"
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

VERIFIED = "VERIFIED"
AUTHOR_MISMATCH = "AUTHOR_MISMATCH"
YEAR_MISMATCH = "YEAR_MISMATCH"
NOT_FOUND = "NOT_FOUND"
CLAIM_UNSUPPORTED = "CLAIM_UNSUPPORTED"
NEEDS_HUMAN = "NEEDS_HUMAN"

# Year tolerance. Rationale (README §Year tolerance): epub-ahead-of-print vs
# issue year legitimately differ by 1 -- we hit this ourselves with Koudijs,
# which we cited as 2023 while CrossRef `issued` says 2022. A 1-year gap is
# therefore ambiguous, not an error -> NEEDS_HUMAN. Our real error (#2,
# Sharifi-Noghabi cited 2024 vs actual 2021) is off by 3, well clear of it.
YEAR_TOLERANCE = 1

TITLE_SIM_THRESHOLD = 0.6
SEARCH_ROWS = 5

# Metric lexicon for numeric-claim checking. Our real error #4 said "Spearman"
# where the source reports Pearson -- the metric NAME is the discriminator, not
# just the number.
METRIC_LEXICON = [
    "spearman", "pearson", "kendall", "auroc", "auprc", "auc", "c-index",
    "concordance", "accuracy", "f1", "sensitivity", "specificity",
    "precision", "recall", "r2", "rmse", "mae", "hazard ratio", "odds ratio",
]


# --------------------------------------------------------------------------
# HTTP + cache
# --------------------------------------------------------------------------
class Cache:
    """Caches raw API responses -- never verdicts.

    A cache hit replays what the API said, including negative results (404s are
    cached as {"__error__": 404}). It is NOT evidence of verification: verdicts
    are always recomputed from the payload.
    """

    def __init__(self, path=None):
        self.path = path
        self.data = {}
        self.dirty = False
        if path:
            try:
                with open(path, "r", encoding="utf-8") as fh:
                    self.data = json.load(fh)
            except (OSError, ValueError):
                self.data = {}

    def get(self, key):
        return self.data.get(key)

    def put(self, key, value):
        self.data[key] = value
        self.dirty = True

    def save(self):
        if self.path and self.dirty:
            with open(self.path, "w", encoding="utf-8") as fh:
                json.dump(self.data, fh, indent=2, sort_keys=True)


def _fetch(url, cache, is_json=True, retries=2):
    """GET with cache. Returns dict/str, or {"__error__": code} on HTTP error."""
    hit = cache.get(url) if cache else None
    if hit is not None:
        return hit
    last = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read().decode("utf-8", "replace")
            out = json.loads(raw) if is_json else raw
            if cache:
                cache.put(url, out)
            return out
        except urllib.error.HTTPError as exc:
            out = {"__error__": exc.code}
            if cache:
                cache.put(url, out)
            return out
        except Exception as exc:  # network flake
            last = exc
            time.sleep(1.5 * (attempt + 1))
    return {"__error__": f"network: {last}"}


def _is_err(payload):
    return not isinstance(payload, (dict, str)) or (
        isinstance(payload, dict) and "__error__" in payload
    )


# --------------------------------------------------------------------------
# Text normalisation
# --------------------------------------------------------------------------
def norm_name(s):
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z]", "", s.lower())


def norm_title(s):
    if not s:
        return ""
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"[^a-z0-9 ]", " ", s.lower())


def title_sim(a, b):
    """Jaccard over word sets -- no external deps."""
    wa = set(norm_title(a).split())
    wb = set(norm_title(b).split())
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / len(wa | wb)


def clean_abstract(s):
    if not s:
        return ""
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    return re.sub(r"\s+", " ", s).strip()


def has_term(term, text):
    """Word-boundary match. Plain substring matching gives false hits -- e.g.
    'er' matches inside 'other'. Verified during design probing."""
    if not term:
        return False
    pat = r"(?<![a-z0-9])" + re.escape(term.lower()).replace(r"\ ", r"\s+") + r"(?![a-z0-9])"
    return re.search(pat, text.lower()) is not None


# --------------------------------------------------------------------------
# Source lookup
# --------------------------------------------------------------------------
def _authors_of(msg):
    out = []
    for a in msg.get("author") or []:
        fam = a.get("family") or a.get("name") or ""
        if fam:
            out.append(fam)
    return out


def _year_of(msg):
    for field in ("issued", "published-print", "published-online", "created"):
        parts = (msg.get(field) or {}).get("date-parts") or []
        if parts and parts[0] and parts[0][0]:
            return int(parts[0][0])
    return None


def fetch_by_doi(doi, cache):
    """Resolve a DOI via CrossRef. Returns (record|None, note)."""
    url = f"{CROSSREF}/{urllib.parse.quote(doi)}"
    payload = _fetch(url, cache)
    if _is_err(payload):
        return None, f"doi_lookup_failed:{payload.get('__error__')}"
    msg = payload.get("message") or {}
    if not msg:
        return None, "doi_lookup_empty"
    return {
        "doi": msg.get("DOI"),
        "title": (msg.get("title") or [""])[0],
        "authors": _authors_of(msg),
        "year": _year_of(msg),
        "abstract": clean_abstract(msg.get("abstract", "")),
    }, "doi_resolved"


def search_crossref(title, first_author, cache, rows=SEARCH_ROWS):
    """Bibliographic search. Returns list of candidate records."""
    q = " ".join(x for x in [title or "", first_author or ""] if x).strip()
    if not q:
        return []
    url = (
        f"{CROSSREF}?query.bibliographic={urllib.parse.quote(q)}"
        f"&rows={rows}&select=DOI,title,author,issued,abstract"
    )
    payload = _fetch(url, cache)
    if _is_err(payload):
        return []
    items = ((payload.get("message") or {}).get("items")) or []
    out = []
    for it in items:
        out.append({
            "doi": it.get("DOI"),
            "title": (it.get("title") or [""])[0],
            "authors": _authors_of(it),
            "year": _year_of(it),
            "abstract": clean_abstract(it.get("abstract", "")),
        })
    return out


def fetch_abstract_pubmed(doi, cache):
    """PubMed efetch fallback -- CrossRef lacks abstracts for many publishers
    (confirmed: Cell and Modern Pathology records return none)."""
    if not doi:
        return ""
    url = f"{EUTILS}/esearch.fcgi?db=pubmed&retmode=json&term={urllib.parse.quote(doi + '[DOI]')}"
    payload = _fetch(url, cache)
    if _is_err(payload):
        return ""
    ids = ((payload.get("esearchresult") or {}).get("idlist")) or []
    if not ids:
        return ""
    xml = _fetch(
        f"{EUTILS}/efetch.fcgi?db=pubmed&retmode=xml&rettype=abstract&id={ids[0]}",
        cache, is_json=False,
    )
    if _is_err(xml) or not isinstance(xml, str):
        return ""
    chunks = re.findall(r"<AbstractText[^>]*>(.*?)</AbstractText>", xml, re.S)
    return clean_abstract(" ".join(chunks))


def get_abstract(record, cache):
    if record.get("abstract"):
        return record["abstract"]
    return fetch_abstract_pubmed(record.get("doi"), cache)


# --------------------------------------------------------------------------
# Checks (module-level so mutation_check.py can monkeypatch them)
# --------------------------------------------------------------------------
def check_author(cited_first_author, record):
    """Returns (ok, note). 0 source authors is NEVER a pass (medsci let
    actual_authors=0 through as OK)."""
    src = record.get("authors") or []
    if not src:
        return None, "source_has_zero_authors"
    if not cited_first_author:
        return None, "no_cited_author"
    if norm_name(cited_first_author) == norm_name(src[0]):
        return True, f"first_author_match:{src[0]}"
    return False, f"first_author cited={cited_first_author} source={src[0]}"


def check_year(cited_year, record):
    """Returns (ok, note). ok=None -> ambiguous (NEEDS_HUMAN)."""
    src = record.get("year")
    if cited_year is None or src is None:
        return None, "year_unavailable"
    diff = abs(int(cited_year) - int(src))
    if diff == 0:
        return True, f"year_match:{src}"
    if diff <= YEAR_TOLERANCE:
        return None, f"year_off_by_{diff} cited={cited_year} source={src} (epub/issue?)"
    return False, f"year cited={cited_year} source={src} (diff={diff})"


def extract_numbers(text):
    return re.findall(r"\d+(?:\.\d+)?", text or "")


def extract_metrics(text):
    low = (text or "").lower()
    return [m for m in METRIC_LEXICON if has_term(m, low)]


def extract_metrics_near_numbers(text, window=60):
    """Metric names used in a *quantitative* sense, i.e. near a number.

    Bare lexicon matching is too noisy to report back: the bbab294 abstract hits
    'sensitivity' via "drug sensitivity" and 'precision' via "precision
    oncology" -- neither is a statistic. Requiring a nearby numeral keeps the
    advisory note honest. (Only affects the note; never the verdict.)"""
    low = (text or "").lower()
    out = []
    for m in METRIC_LEXICON:
        for mt in re.finditer(
            r"(?<![a-z0-9])" + re.escape(m).replace(r"\ ", r"\s+") + r"(?![a-z0-9])", low
        ):
            lo = max(0, mt.start() - window)
            if re.search(r"\d+(?:\.\d+)?", low[lo:mt.end() + window]):
                out.append(m)
                break
    return out


def check_claim(claim, abstract):
    """Returns (verdict, notes). Abstract-grounded claim check."""
    notes = []
    text = claim.get("text", "")
    if not abstract:
        return NEEDS_HUMAN, ["no_abstract_available: cannot check claim"]

    # -- scope layer (#5 type): did we assert a keyword the abstract lacks?
    scope_terms = claim.get("scope_terms") or []
    missing_scope = [t for t in scope_terms if not has_term(t, abstract)]
    if missing_scope:
        notes.append(f"scope_terms_absent_from_abstract: {missing_scope}")
        contra = [t for t in (claim.get("contradicting_terms") or []) if has_term(t, abstract)]
        if contra:
            notes.append(f"abstract_instead_centres_on: {contra}")
        return CLAIM_UNSUPPORTED, notes

    # -- numeric layer (#4 type)
    nums = [n for n in extract_numbers(text) if not re.fullmatch(r"(19|20)\d{2}", n)]
    claimed_metrics = extract_metrics(text)
    abstract_metrics = extract_metrics_near_numbers(abstract)

    if claimed_metrics:
        wrong_metric = [m for m in claimed_metrics if not has_term(m, abstract)]
        if wrong_metric:
            notes.append(f"claimed_metric_absent_from_abstract: {wrong_metric}")
            others = [m for m in abstract_metrics if m not in claimed_metrics]
            if others:
                notes.append(f"abstract_reports_different_metric: {others}")
            return CLAIM_UNSUPPORTED, notes

    if nums:
        abs_nums = set(extract_numbers(abstract))
        missing = []
        for n in nums:
            if n in abs_nums:
                continue
            if any(abs(float(n) - float(a)) < 1e-9 for a in abs_nums):
                continue
            missing.append(n)
        if missing:
            notes.append(f"claimed_values_absent_from_abstract: {missing}")
            if not abs_nums:
                notes.append("abstract_reports_no_numeric_values_at_all")
            return CLAIM_UNSUPPORTED, notes
        notes.append(f"claimed_values_present_in_abstract: {nums}")

    if not nums and not claimed_metrics and not scope_terms:
        return NEEDS_HUMAN, ["claim_has_no_checkable_assertion"]

    notes.append("claim_supported_by_abstract")
    return VERIFIED, notes


# --------------------------------------------------------------------------
# Main verification
# --------------------------------------------------------------------------
def resolve_source(entry, cache):
    """Find the source record. Returns (record|None, notes list).

    THE CRITICAL PATH: if the DOI fails to resolve we do NOT quietly fall back
    to a weak title search that passes. We search, but a search hit only counts
    if the claimed first author actually appears in the top-N.
    """
    notes = []
    doi = entry.get("doi")
    if doi:
        rec, note = fetch_by_doi(doi, cache)
        notes.append(note)
        if rec:
            return rec, notes
        notes.append("falling back to search (DOI did NOT resolve -- cannot be VERIFIED)")

    cands = search_crossref(entry.get("title"), entry.get("first_author"), cache)
    if not cands:
        notes.append("search_returned_zero_results")
        return None, notes

    cited = norm_name(entry.get("first_author"))
    top_first = [c["authors"][0] for c in cands if c.get("authors")]
    notes.append(f"search_top{len(cands)}_first_authors: {top_first}")

    for c in cands:
        auths = [norm_name(a) for a in (c.get("authors") or [])]
        sim = title_sim(entry.get("title"), c.get("title"))
        if cited and cited in auths and sim >= TITLE_SIM_THRESHOLD:
            notes.append(f"search_match doi={c['doi']} title_sim={sim:.2f}")
            return c, notes

    notes.append(
        f"claimed first author {entry.get('first_author')!r} not found among "
        f"top-{len(cands)} search results -> fabrication suspected"
    )
    return None, notes


def verify_one(entry, cache):
    notes = []
    record, rnotes = resolve_source(entry, cache)
    notes += rnotes

    if record is None:
        return {"id": entry.get("id"), "verdict": NOT_FOUND, "notes": notes}

    doi_resolved = any(n.startswith("doi_resolved") for n in notes)

    a_ok, a_note = check_author(entry.get("first_author"), record)
    notes.append(a_note)
    if a_ok is False:
        return {"id": entry.get("id"), "verdict": AUTHOR_MISMATCH, "notes": notes}

    y_ok, y_note = check_year(entry.get("year"), record)
    notes.append(y_note)
    if y_ok is False:
        return {"id": entry.get("id"), "verdict": YEAR_MISMATCH, "notes": notes}

    # Bibliography is clean-ish; now check any attached claims.
    claims = entry.get("claims") or []
    if claims:
        abstract = get_abstract(record, cache)
        for claim in claims:
            cv, cnotes = check_claim(claim, abstract)
            notes += [f"claim[{claim.get('text','')[:60]}]: {n}" for n in cnotes]
            if cv == CLAIM_UNSUPPORTED:
                return {"id": entry.get("id"), "verdict": CLAIM_UNSUPPORTED, "notes": notes}
            if cv == NEEDS_HUMAN:
                return {"id": entry.get("id"), "verdict": NEEDS_HUMAN, "notes": notes}

    # A pass requires everything to be affirmatively true. Ambiguity != pass.
    if a_ok is None:
        return {"id": entry.get("id"), "verdict": NEEDS_HUMAN, "notes": notes}
    if y_ok is None:
        return {"id": entry.get("id"), "verdict": NEEDS_HUMAN, "notes": notes}
    if not doi_resolved:
        notes.append("matched via search, not a resolved DOI")
        return {"id": entry.get("id"), "verdict": NEEDS_HUMAN, "notes": notes}

    return {"id": entry.get("id"), "verdict": VERIFIED, "notes": notes}


def verify_all(entries, cache):
    return [verify_one(e, cache) for e in entries]


def main():
    ap = argparse.ArgumentParser(description="citation verifier (stdlib only)")
    ap.add_argument("cases", help="JSON file: list of citation entries")
    ap.add_argument("--cache", default=None, help="local JSON cache of raw API responses")
    ap.add_argument("--json", dest="out", default=None, help="write results JSON")
    args = ap.parse_args()

    with open(args.cases, "r", encoding="utf-8") as fh:
        doc = json.load(fh)
    entries = doc["entries"] if isinstance(doc, dict) else doc

    cache = Cache(args.cache)
    results = verify_all(entries, cache)
    cache.save()

    width = max(len(str(r["id"])) for r in results) if results else 10
    print(f"{'id'.ljust(width)}  verdict")
    print("-" * (width + 22))
    for r in results:
        print(f"{str(r['id']).ljust(width)}  {r['verdict']}")
    print()
    for r in results:
        print(f"== {r['id']} -> {r['verdict']}")
        for n in r["notes"]:
            print(f"     - {n}")

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(results, fh, indent=2)

    bad = [r for r in results if r["verdict"] != VERIFIED]
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
