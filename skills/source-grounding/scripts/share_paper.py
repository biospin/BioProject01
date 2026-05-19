#!/usr/bin/env python3
"""Copy a paper PDF to a share location with a human-friendly filename.

Sources/ keeps short paper-id-based names (li-2023-multivelo.pdf). When sharing
the PDF with someone outside the project, you want a more descriptive filename.
This script reads paper-info.yaml and copies the PDF using either the explicit
`citation.share_filename` field, or an auto-generated name.

Usage:
    python3 share_paper.py <paper-folder>                    # copies to ~/Downloads
    python3 share_paper.py <paper-folder> --to <dir>
    python3 share_paper.py <paper-folder> --name "Custom.pdf"
    python3 share_paper.py <paper-folder> --print            # dry-run, just print the path
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

try:
    from ruamel.yaml import YAML
except ImportError:
    print(
        "ruamel.yaml required. Install with: "
        "pip install -r skills/source-grounding/scripts/requirements.txt",
        file=sys.stderr,
    )
    sys.exit(1)


yaml_io = YAML(typ="rt")


def sanitize_filename(name: str) -> str:
    """Replace characters that are awkward in filenames (cross-platform)."""
    name = re.sub(r'[\\/:*?"<>|]', "-", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name


def auto_share_filename(data: dict) -> str:
    """Generate a default share filename from yaml when share_filename is unset."""
    authors = data.get("authors") or []
    lastname = ""
    if authors:
        first = authors[0]
        lastname = first.split(",")[0].strip() if "," in first else first.split()[-1]
    year = data.get("year", "")
    short_id = (data.get("citation") or {}).get("short_id") or ""
    title = data.get("title") or ""
    # take first 6-8 words of title
    title_short = " ".join(title.split()[:8])
    parts = [p for p in [lastname, str(year), title_short] if p]
    base = " - ".join(parts)
    if short_id:
        base += f" ({short_id})"
    return sanitize_filename(base + ".pdf")


def main() -> int:
    parser = argparse.ArgumentParser(description="Copy a paper PDF to a share location")
    parser.add_argument("paper_folder", type=Path, help="path to analysis/<topic>/<paper-id>/")
    parser.add_argument("--to", type=Path, default=Path.home() / "Downloads",
                        help="Destination directory (default: ~/Downloads)")
    parser.add_argument("--name", type=str, default=None,
                        help="Override share filename (otherwise yaml's share_filename or auto)")
    parser.add_argument("--print", dest="print_only", action="store_true",
                        help="Print the resulting path without copying")
    args = parser.parse_args()

    folder = args.paper_folder.resolve()
    yaml_path = folder / "paper-info.yaml"
    if not yaml_path.exists():
        print(f"not found: {yaml_path}", file=sys.stderr)
        return 1

    with yaml_path.open("r", encoding="utf-8") as f:
        data = yaml_io.load(f)

    paper_block = (data.get("sources") or {}).get("paper") or {}
    local_rel = paper_block.get("local")
    if not local_rel:
        print("paper-info.yaml has no sources.paper.local", file=sys.stderr)
        return 1
    src = folder / local_rel
    if not src.exists():
        print(f"PDF not found at {src}. Did you download it yet?", file=sys.stderr)
        return 1

    # decide share filename
    if args.name:
        share_name = sanitize_filename(args.name)
    else:
        explicit = (data.get("citation") or {}).get("share_filename")
        share_name = sanitize_filename(explicit) if explicit else auto_share_filename(data)
        if not share_name.endswith(".pdf"):
            share_name += ".pdf"

    dest = args.to.expanduser().resolve() / share_name
    if args.print_only:
        print(f"would copy: {src}")
        print(f"        →: {dest}")
        return 0

    args.to.expanduser().mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    print(f"copied: {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
