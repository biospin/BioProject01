#!/usr/bin/env python3
"""critic #6: 업로드/로컬 PDF를 분석 폴더 sources/로 *deterministic* 복사 + checksum 기록.

source-grounding의 핵심(원문 보존)을 LLM prompt의 수동 `cp`에 맡기지 않고 이 스크립트가 책임진다.
LLM은 이 스크립트를 *호출만* 한다.

usage: python3 web/scripts/place_source.py <src_pdf> <paper_dir>
  예: python3 web/scripts/place_source.py artifacts/uploads/2026-..-x.pdf analysis/epigenomic-lag/li-2023-multivelo
"""
import datetime
import hashlib
import shutil
import sys
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    src = Path(sys.argv[1])
    paper_dir = Path(sys.argv[2])
    if not src.is_file():
        print(f"✗ source PDF 없음: {src}", file=sys.stderr)
        return 2
    if not paper_dir.is_dir():
        print(f"✗ paper_dir 없음: {paper_dir}", file=sys.stderr)
        return 2

    pid = paper_dir.name
    srcdir = paper_dir / "sources"
    srcdir.mkdir(exist_ok=True)
    dest = srcdir / f"{pid}.pdf"
    shutil.copy2(src, dest)
    digest = sha256(dest)
    today = datetime.date.today().isoformat()

    # 1) source_manifest.tsv (항상 — comment 안전)
    manifest = srcdir / "source_manifest.tsv"
    new = not manifest.exists()
    with open(manifest, "a", encoding="utf-8") as f:
        if new:
            f.write("file\tsha256\tsource\tdate\n")
        f.write(f"{dest.name}\t{digest}\t{src}\t{today}\n")

    # 2) paper-info.yaml best-effort (comment 보존 위해 append만)
    yml = paper_dir / "paper-info.yaml"
    if yml.exists():
        txt = yml.read_text(encoding="utf-8")
        if "source_sha256:" not in txt:
            yml.write_text(
                txt.rstrip() + f'\nsource_sha256: "{digest}"  # {dest.name} (place_source.py {today})\n',
                encoding="utf-8",
            )

    print(f"✓ {src} → {dest}")
    print(f"  sha256: {digest}")
    print(f"  manifest: {manifest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
