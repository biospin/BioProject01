#!/usr/bin/env python3
"""Build analysis/_index/ from all paper-info.yaml files.

See skills/source-grounding/SKILL.md Part 8 for the full spec.

Usage:
    python3 build_index.py                  # full rebuild
    python3 build_index.py --topic <name>   # rebuild a single topic markdown
    python3 build_index.py --csv-only       # only papers.csv
    python3 build_index.py --verbose        # log each yaml processed
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    from ruamel.yaml import YAML
    from ruamel.yaml.error import YAMLError
except ImportError:
    YAML = None

    class YAMLError(Exception):
        pass


# Round-trip loader so other tools (fetch_sources.py) that write back to the
# same files preserve comments. build_index.py itself only reads, so safe mode
# would also work — but we keep rt for consistency across the project.
if YAML is not None:
    yaml_io = YAML(typ="rt")
    yaml_io.preserve_quotes = True
    yaml_io.indent(mapping=2, sequence=4, offset=2)
else:
    yaml_io = None


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if value == "":
        return {}
    if value in {"null", "Null", "NULL", "~"}:
        return None
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [_parse_scalar(part.strip()) for part in inner.split(",")]
    try:
        return int(value)
    except ValueError:
        return value


def _strip_inline_comment(value: str) -> str:
    quote: str | None = None
    for i, ch in enumerate(value):
        if ch in {"'", '"'}:
            quote = None if quote == ch else ch
        if ch == "#" and quote is None:
            return value[:i].rstrip()
    return value


def _simple_yaml_load(text: str) -> dict[str, Any]:
    """Small YAML subset reader used only when ruamel.yaml is unavailable.

    It supports the project paper-info.yaml shape: nested mappings, scalar
    values, and lists of scalars or dictionaries. It is deliberately read-only.
    """
    root: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(-1, root)]
    last_key_at_indent: dict[int, tuple[Any, str]] = {}
    last_mapping_key: tuple[Any, str] | None = None

    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()

        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]

        if line.startswith("- "):
            item_text = _strip_inline_comment(line[2:].strip())
            if not isinstance(parent, list):
                holder_key = (
                    last_key_at_indent.get(indent)
                    or last_key_at_indent.get(indent + 2)
                    or last_mapping_key
                )
                if holder_key is None:
                    continue
                holder, key = holder_key
                new_list: list[Any] = []
                holder[key] = new_list
                stack.append((indent - 1, new_list))
                parent = new_list
            if ":" in item_text and not item_text.startswith(("http://", "https://")):
                key, value = item_text.split(":", 1)
                item: dict[str, Any] = {key.strip(): _parse_scalar(_strip_inline_comment(value))}
                parent.append(item)
                stack.append((indent, item))
                last_key_at_indent[indent + 2] = (item, key.strip())
            else:
                parent.append(_parse_scalar(item_text))
            continue

        while isinstance(parent, list) and stack and indent <= stack[-1][0] + 1:
            stack.pop()
            parent = stack[-1][1]

        if ":" not in line or not isinstance(parent, dict):
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        parent[key] = _parse_scalar(_strip_inline_comment(value))
        last_mapping_key = (parent, key)
        last_key_at_indent[indent + 2] = (parent, key)
        if isinstance(parent[key], dict) and value.strip() == "":
            stack.append((indent, parent[key]))

    return root


# ---------------------------------------------------------------------------
# Repository layout
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[3]
ANALYSIS_DIR = REPO_ROOT / "analysis"
INDEX_DIR = ANALYSIS_DIR / "_index"


# ---------------------------------------------------------------------------
# CSV schema (see SKILL.md Part 8.2)
# ---------------------------------------------------------------------------

CSV_COLUMNS = [
    "folder",
    "paper_id",
    "title",
    "authors_short",
    "year",
    "venue",
    "doi",
    "document_type",
    "topics",
    "use_case",
    "importance_level",
    "importance_perspective",
    "audience_primary",
    "priority_level",
    "priority_deadline",
    "analysis_status_short",
    "last_updated",
    "citation_key",
]

STATUS_ABBREV = {
    "abstract": "abs",
    "core": "core",
    "lens_academic": "la",
    "lens_industry": "li",
    "methodology_brief": "mb",
    "slides": "sl",
}
STATE_ABBREV = {
    "done": "done",
    "in-progress": "ip",
    "in_progress": "ip",        # alias (underscore variant)
    "pending": "pn",
    "skipped": "sk",
    "not-applicable": "na",
    "not_applicable": "na",     # alias (underscore variant)
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def find_paper_yamls() -> list[Path]:
    """Return all paper-info.yaml files under analysis/, excluding _index/."""
    if not ANALYSIS_DIR.exists():
        return []
    results = []
    for path in ANALYSIS_DIR.rglob("paper-info.yaml"):
        if INDEX_DIR in path.parents:
            continue
        results.append(path)
    return sorted(results)


def load_yaml(path: Path) -> dict[str, Any] | None:
    try:
        if yaml_io is not None:
            with path.open("r", encoding="utf-8") as f:
                data = yaml_io.load(f)
        else:
            try:
                raw = subprocess.check_output(
                    [
                        "ruby",
                        "-ryaml",
                        "-rjson",
                        "-e",
                        "puts YAML.load_file(ARGV[0]).to_json",
                        str(path),
                    ],
                    text=True,
                    stderr=subprocess.DEVNULL,
                )
                data = json.loads(raw)
            except Exception:
                data = _simple_yaml_load(path.read_text(encoding="utf-8"))
    except YAMLError as e:
        print(f"  yaml parse error in {path}: {e}", file=sys.stderr)
        return None
    # ruamel.yaml round-trip returns a CommentedMap (dict subclass).
    if not isinstance(data, dict):
        print(f"  not a mapping: {path}", file=sys.stderr)
        return None
    return data


def authors_short(authors: list[str] | None) -> str:
    if not authors:
        return ""
    first = authors[0]
    if len(authors) == 1:
        return first
    return f"{first} et al."


def analysis_status_short(status_block: dict[str, str] | None) -> str:
    if not status_block:
        return ""
    parts = []
    for full_key, abbrev in STATUS_ABBREV.items():
        state = status_block.get(full_key)
        if state is None:
            continue
        parts.append(f"{abbrev}:{STATE_ABBREV.get(state, state)}")
    return ",".join(parts)


def yaml_to_row(yaml_path: Path, data: dict[str, Any]) -> dict[str, str]:
    rel = yaml_path.parent.relative_to(ANALYSIS_DIR)
    folder = str(rel)
    paper_id = rel.name

    citation = data.get("citation") or {}
    categorization = data.get("categorization") or {}
    importance = categorization.get("importance") or {}
    audience = data.get("audience") or {}
    priority = data.get("priority") or {}
    workflow = data.get("workflow") or {}

    use_case = categorization.get("use_case") or []
    topics = data.get("topics") or []
    domain = categorization.get("domain") or []

    return {
        "folder": folder,
        "paper_id": paper_id,
        "title": str(data.get("title") or ""),
        "authors_short": authors_short(data.get("authors")),
        "year": str(data.get("year") or ""),
        "venue": str(data.get("venue") or ""),
        "doi": str(data.get("doi") or ""),
        "document_type": str(data.get("document_type") or ""),
        "topics": ";".join(str(t) for t in topics),
        "use_case": ";".join(str(u) for u in use_case),
        "importance_level": str(importance.get("level") or ""),
        "importance_perspective": str(importance.get("perspective") or ""),
        "audience_primary": str(audience.get("primary") or ""),
        "priority_level": str(priority.get("level") or ""),
        "priority_deadline": str(priority.get("deadline") or ""),
        "analysis_status_short": analysis_status_short(workflow.get("analysis_status")),
        "last_updated": str(workflow.get("last_updated") or ""),
        "citation_key": str(citation.get("key") or ""),
    }


# ---------------------------------------------------------------------------
# Output: papers.csv
# ---------------------------------------------------------------------------


def write_papers_csv(rows: list[dict[str, str]]) -> Path:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    out = INDEX_DIR / "papers.csv"
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=CSV_COLUMNS,
            quoting=csv.QUOTE_MINIMAL,
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return out


# ---------------------------------------------------------------------------
# Output: _index/<topic>.md
# ---------------------------------------------------------------------------


def collect_topic_buckets(
    yamls: list[tuple[Path, dict[str, Any]]],
) -> dict[str, dict[str, list[tuple[Path, dict[str, Any]]]]]:
    """Return { topic -> { 'primary': [...], 'secondary': [...] } }."""
    buckets: dict[str, dict[str, list[tuple[Path, dict[str, Any]]]]] = {}
    for path, data in yamls:
        topics = data.get("topics") or []
        if not topics:
            continue
        primary = str(topics[0])
        buckets.setdefault(primary, {"primary": [], "secondary": []})["primary"].append(
            (path, data)
        )
        for t in topics[1:]:
            t_str = str(t)
            buckets.setdefault(t_str, {"primary": [], "secondary": []})["secondary"].append(
                (path, data)
            )
    return buckets


def render_topic_md(
    topic: str,
    bucket: dict[str, list[tuple[Path, dict[str, Any]]]],
) -> str:
    today = dt.date.today().isoformat()
    lines = [
        f"# Topic: {topic}",
        "",
        f"마지막 갱신: {today}",
        "",
        "## Papers (primary topic으로 등록된 것)",
        "",
        "| Paper | Year | Venue | Importance | Use case | Status |",
        "|---|---|---|---|---|---|",
    ]
    for path, data in bucket["primary"]:
        rel = path.parent.relative_to(ANALYSIS_DIR)
        paper_id = rel.name
        importance = (data.get("categorization") or {}).get("importance") or {}
        level = importance.get("level") or ""
        use_case = (data.get("categorization") or {}).get("use_case") or []
        status_short = analysis_status_short(
            (data.get("workflow") or {}).get("analysis_status")
        )
        lines.append(
            f"| [{paper_id}](../{rel}/) "
            f"| {data.get('year', '')} "
            f"| {data.get('venue', '')} "
            f"| {level} "
            f"| {'; '.join(str(u) for u in use_case)} "
            f"| {status_short} |"
        )

    if bucket["secondary"]:
        lines += [
            "",
            "## Related (secondary topic으로만 등록된 것)",
            "",
            "| Paper | Primary topic | Year | Venue | Importance |",
            "|---|---|---|---|---|",
        ]
        for path, data in bucket["secondary"]:
            rel = path.parent.relative_to(ANALYSIS_DIR)
            paper_id = rel.name
            topics = data.get("topics") or []
            primary = str(topics[0]) if topics else ""
            importance = (data.get("categorization") or {}).get("importance") or {}
            level = importance.get("level") or ""
            lines.append(
                f"| [{paper_id}](../{rel}/) "
                f"| {primary} "
                f"| {data.get('year', '')} "
                f"| {data.get('venue', '')} "
                f"| {level} |"
            )

    lines.append("")
    return "\n".join(lines)


def write_topic_mds(
    buckets: dict[str, dict[str, list[tuple[Path, dict[str, Any]]]]],
    only_topic: str | None = None,
) -> list[Path]:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    written = []
    for topic, bucket in sorted(buckets.items()):
        if only_topic and topic != only_topic:
            continue
        out = INDEX_DIR / f"{topic}.md"
        out.write_text(render_topic_md(topic, bucket), encoding="utf-8")
        written.append(out)
    return written


# ---------------------------------------------------------------------------
# Output: paper-info.yaml first-line header
# ---------------------------------------------------------------------------

# Marker that closes the auto-managed header block. build_index.py finds this
# line and replaces everything from the top of the file up to and including it.
# If the marker is missing (legacy yaml), update_yaml_header falls back to
# sweeping the leading comment block.
HEADER_END_MARKER = "# ─── end of header (auto-managed by build_index.py; do not edit this block manually) ───"


def build_header_lines(data: dict[str, Any]) -> list[str]:
    authors = authors_short(data.get("authors"))
    year = data.get("year", "")
    venue = data.get("venue", "")
    doi = data.get("doi") or ""

    citation = data.get("citation") or {}
    short_id = citation.get("short_id") or ""
    keyword = short_id or (str(data.get("title") or "")[:40])

    line1 = f"# {authors}, {year} — {keyword} — {venue}".rstrip(" —")
    line2 = f"# DOI: {doi}" if doi else "# DOI: (없음)"

    topics = data.get("topics") or []
    primary = str(topics[0]) if topics else ""
    secondary = ", ".join(str(t) for t in topics[1:])
    importance = (data.get("categorization") or {}).get("importance") or {}
    level = importance.get("level") or "-"
    topics_str = f"{primary} (primary)" + (f", {secondary}" if secondary else "")
    line3 = f"# Topics: {topics_str}  |  Importance: {level}"

    # Blank line + marker close out the header block visually.
    return [line1, line2, line3, "", HEADER_END_MARKER]


_MARKER_PREFIX = "# ─── end of header"


def _find_header_end_idx(lines: list[str]) -> int:
    """Return the index of the first line that is yaml body (not header).

    Strategy:
    1. If the explicit HEADER_END_MARKER is present in the first ~20 lines, the
       header ends just after it (plus any trailing blank lines).
    2. Otherwise (legacy file), sweep contiguous leading `#`-prefixed comment
       lines and blank lines until we hit the first non-comment yaml line.
    """
    # 1. Marker-based detection
    scan_limit = min(len(lines), 30)
    for i in range(scan_limit):
        if lines[i].startswith(_MARKER_PREFIX):
            end_idx = i + 1
            while end_idx < len(lines) and lines[end_idx].strip() == "":
                end_idx += 1
            return end_idx

    # 2. Fallback: sweep leading comment/blank block
    end_idx = 0
    while end_idx < len(lines):
        line = lines[end_idx]
        if line.startswith("#") or line.strip() == "":
            end_idx += 1
            continue
        break
    return end_idx


def update_yaml_header(yaml_path: Path, data: dict[str, Any]) -> bool:
    """Replace the leading comment header block (if present) with a freshly rendered one.

    The header block ends at the HEADER_END_MARKER if present (preferred for
    new files), otherwise at the first non-comment yaml line (legacy fallback).
    Comments inside the yaml body are not touched.
    """
    text = yaml_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    end_idx = _find_header_end_idx(lines)

    new_header = build_header_lines(data)
    new_text = "\n".join(new_header) + "\n\n" + "\n".join(lines[end_idx:]).lstrip("\n")
    if not new_text.endswith("\n"):
        new_text += "\n"

    if new_text == text:
        return False
    yaml_path.write_text(new_text, encoding="utf-8")
    return True


# ---------------------------------------------------------------------------
# Output: _index/README.md
# ---------------------------------------------------------------------------


README_TEMPLATE = """# Index

`build_index.py`가 자동 생성하는 디렉토리입니다. **직접 편집하지 마세요.**

## 파일

- `papers.csv` — 모든 분석된 자료의 통합 표. Excel/Numbers/Google Sheets에서 정렬·필터.
- `<topic>.md` — topic별 markdown 목록. *primary topic*과 *secondary topic*으로 등록된 자료를 분리.

## 갱신

paper-info.yaml이 변경되었거나 새 자료가 추가되었으면 다음을 실행:

```bash
python3 skills/source-grounding/scripts/build_index.py
```

옵션:
- `--topic <name>` — 특정 topic만 다시 빌드
- `--csv-only` — papers.csv만 갱신
- `--verbose` — 처리 중인 yaml 경로 출력
"""


def write_readme() -> Path:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    out = INDEX_DIR / "README.md"
    out.write_text(README_TEMPLATE, encoding="utf-8")
    return out


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description="Build analysis/_index/ from paper-info.yaml files")
    parser.add_argument("--topic", help="Rebuild a single topic markdown only")
    parser.add_argument("--csv-only", action="store_true", help="Only regenerate papers.csv")
    parser.add_argument("--verbose", action="store_true", help="Print progress")
    parser.add_argument(
        "--no-header-update",
        action="store_true",
        help="Do not rewrite paper-info.yaml first-line headers",
    )
    args = parser.parse_args()

    yaml_paths = find_paper_yamls()
    if not yaml_paths:
        print(f"No paper-info.yaml found under {ANALYSIS_DIR}.")
        return 0

    rows: list[dict[str, str]] = []
    loaded: list[tuple[Path, dict[str, Any]]] = []
    for path in yaml_paths:
        if args.verbose:
            print(f"  reading {path}")
        data = load_yaml(path)
        if data is None:
            continue
        if not data.get("topics"):
            print(f"  warning: {path} has no 'topics' field, skipping", file=sys.stderr)
            continue
        loaded.append((path, data))
        rows.append(yaml_to_row(path, data))

    csv_out = write_papers_csv(rows)
    print(f"wrote {csv_out} ({len(rows)} rows)")

    if not args.csv_only:
        buckets = collect_topic_buckets(loaded)
        topic_outs = write_topic_mds(buckets, only_topic=args.topic)
        for p in topic_outs:
            print(f"wrote {p}")
        readme = write_readme()
        print(f"wrote {readme}")

        if not args.no_header_update:
            changed = 0
            for path, data in loaded:
                try:
                    if update_yaml_header(path, data):
                        changed += 1
                except Exception as e:  # noqa: BLE001
                    print(f"  header update failed for {path}: {e}", file=sys.stderr)
            print(f"updated header in {changed} paper-info.yaml file(s)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
