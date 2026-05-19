#!/usr/bin/env python3
"""Extract figure panels from a PDF page.

Dependencies:
  python3 -m pip install pymupdf pillow

Typical use:
  python3 skills/full-figure/scripts/extract_panels.py papers/paper.pdf \
    --page 5 --figure Figure2 --figure-bbox 72,120,540,650 \
    --out analysis/Paper/figures

For difficult layouts, pass a JSON spec with explicit panel boxes:
  python3 skills/full-figure/scripts/extract_panels.py papers/paper.pdf \
    --spec figure2-panels.json --out analysis/Paper/figures
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

fitz = None
Image = None
ImageDraw = None


@dataclass(frozen=True)
class Box:
    x0: int
    y0: int
    x1: int
    y1: int

    @property
    def width(self) -> int:
        return self.x1 - self.x0

    @property
    def height(self) -> int:
        return self.y1 - self.y0

    @property
    def area(self) -> int:
        return max(0, self.width) * max(0, self.height)

    def pad(self, px: int, max_w: int, max_h: int) -> "Box":
        return Box(
            max(0, self.x0 - px),
            max(0, self.y0 - px),
            min(max_w, self.x1 + px),
            min(max_h, self.y1 + px),
        )

    def as_list(self) -> list[int]:
        return [self.x0, self.y0, self.x1, self.y1]


def parse_box(value: str) -> list[float]:
    parts = [p.strip() for p in value.split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("bbox must be x0,y0,x1,y1")
    try:
        coords = [float(p) for p in parts]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("bbox values must be numbers") from exc
    if coords[2] <= coords[0] or coords[3] <= coords[1]:
        raise argparse.ArgumentTypeError("bbox must satisfy x1>x0 and y1>y0")
    return coords


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_") or "figure"


def render_page(pdf: Path, page_number: int, dpi: int) -> tuple[Image.Image, Any, float]:
    ensure_image_dependencies()
    doc = fitz.open(pdf)
    if page_number < 1 or page_number > len(doc):
        raise SystemExit(f"--page must be in 1..{len(doc)}")
    page = doc[page_number - 1]
    zoom = dpi / 72.0
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return image, page.rect, zoom


def ensure_image_dependencies() -> None:
    global Image, ImageDraw, fitz
    if Image is not None and ImageDraw is not None and fitz is not None:
        return
    try:
        import fitz as fitz_module  # PyMuPDF
        from PIL import Image as image_module
        from PIL import ImageDraw as image_draw_module
    except ImportError as exc:
        print(
            "Missing dependency. Install with: python3 -m pip install pymupdf pillow",
            file=sys.stderr,
        )
        raise SystemExit(2) from exc
    fitz = fitz_module
    Image = image_module
    ImageDraw = image_draw_module


def convert_box(
    coords: Iterable[float],
    coords_mode: str,
    page_rect: Any,
    zoom: float,
    image_size: tuple[int, int],
    origin_box: Box | None = None,
) -> Box:
    x0, y0, x1, y1 = coords
    width, height = image_size
    if coords_mode == "pdf":
        box = Box(
            int(round(x0 * zoom)),
            int(round(y0 * zoom)),
            int(round(x1 * zoom)),
            int(round(y1 * zoom)),
        )
    elif coords_mode == "normalized":
        box = Box(
            int(round(x0 * width)),
            int(round(y0 * height)),
            int(round(x1 * width)),
            int(round(y1 * height)),
        )
    elif coords_mode == "pixels":
        box = Box(int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1)))
    else:
        raise SystemExit(f"Unknown coords mode: {coords_mode}")

    if origin_box is not None:
        box = Box(
            origin_box.x0 + box.x0,
            origin_box.y0 + box.y0,
            origin_box.x0 + box.x1,
            origin_box.y0 + box.y1,
        )

    max_x = int(round(page_rect.width * zoom))
    max_y = int(round(page_rect.height * zoom))
    return Box(
        max(0, min(max_x, box.x0)),
        max(0, min(max_y, box.y0)),
        max(0, min(max_x, box.x1)),
        max(0, min(max_y, box.y1)),
    )


def ink_bbox(image: Image.Image, threshold: int = 245) -> Box:
    gray = image.convert("L")
    width, height = gray.size
    pix = gray.load()
    x0, y0, x1, y1 = width, height, 0, 0
    for y in range(height):
        for x in range(width):
            if pix[x, y] < threshold:
                x0 = min(x0, x)
                y0 = min(y0, y)
                x1 = max(x1, x + 1)
                y1 = max(y1, y + 1)
    if x1 <= x0 or y1 <= y0:
        return Box(0, 0, width, height)
    return Box(x0, y0, x1, y1)


def projection(image: Image.Image, box: Box, threshold: int, axis: str) -> list[int]:
    gray = image.convert("L")
    pix = gray.load()
    if axis == "x":
        counts = []
        for x in range(box.x0, box.x1):
            ink = 0
            for y in range(box.y0, box.y1):
                if pix[x, y] < threshold:
                    ink += 1
            counts.append(ink)
        return counts
    counts = []
    for y in range(box.y0, box.y1):
        ink = 0
        for x in range(box.x0, box.x1):
            if pix[x, y] < threshold:
                ink += 1
        counts.append(ink)
    return counts


def gutter_runs(
    counts: list[int],
    max_ink: int,
    min_gutter: int,
    margin: int,
) -> list[tuple[int, int]]:
    runs: list[tuple[int, int]] = []
    start: int | None = None
    end_limit = len(counts) - margin
    for idx, count in enumerate(counts):
        inside = margin <= idx < end_limit
        if inside and count <= max_ink:
            if start is None:
                start = idx
        elif start is not None:
            if idx - start >= min_gutter:
                runs.append((start, idx))
            start = None
    if start is not None and len(counts) - start >= min_gutter:
        runs.append((start, len(counts)))
    return runs


def best_split(image: Image.Image, box: Box, threshold: int, min_gutter: int) -> tuple[str, int] | None:
    candidates: list[tuple[int, str, int]] = []
    for axis in ("x", "y"):
        counts = projection(image, box, threshold, axis)
        span = box.height if axis == "x" else box.width
        max_ink = max(2, int(span * 0.01))
        margin = max(6, min(len(counts) // 20, min_gutter))
        for start, end in gutter_runs(counts, max_ink, min_gutter, margin):
            center = (start + end) // 2
            left = center
            right = len(counts) - center
            if min(left, right) < min_gutter * 2:
                continue
            candidates.append((end - start, axis, center))
    if not candidates:
        return None
    _, axis, offset = max(candidates)
    if axis == "x":
        return axis, box.x0 + offset
    return axis, box.y0 + offset


def split_panels(
    image: Image.Image,
    box: Box,
    threshold: int,
    min_panel: int,
    min_gutter: int,
    max_panels: int,
) -> list[Box]:
    pending = [box]
    changed = True
    while changed and len(pending) < max_panels:
        changed = False
        next_boxes: list[Box] = []
        for current in pending:
            if current.width < min_panel * 2 and current.height < min_panel * 2:
                next_boxes.append(current)
                continue
            split = best_split(image, current, threshold, min_gutter)
            if split is None:
                next_boxes.append(current)
                continue
            axis, pos = split
            if axis == "x":
                a = Box(current.x0, current.y0, pos, current.y1)
                b = Box(pos, current.y0, current.x1, current.y1)
            else:
                a = Box(current.x0, current.y0, current.x1, pos)
                b = Box(current.x0, pos, current.x1, current.y1)
            if a.width < min_panel or a.height < min_panel or b.width < min_panel or b.height < min_panel:
                next_boxes.append(current)
                continue
            next_boxes.extend([a, b])
            changed = True
            if len(next_boxes) + len(pending) >= max_panels:
                next_boxes.extend(pending[pending.index(current) + 1 :])
                break
        pending = next_boxes
    return sorted(pending, key=lambda b: (b.y0 // max(1, min_panel), b.x0))


def load_spec(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def panel_entries_from_spec(spec: dict[str, Any]) -> list[dict[str, Any]]:
    panels = spec.get("panels")
    if not isinstance(panels, list) or not panels:
        raise SystemExit("Spec must contain a non-empty panels list")
    return panels


def draw_debug(image: Image.Image, boxes: list[tuple[str, Box]], output: Path) -> None:
    debug = image.copy()
    draw = ImageDraw.Draw(debug)
    for label, box in boxes:
        draw.rectangle(box.as_list(), outline="red", width=4)
        draw.text((box.x0 + 6, box.y0 + 6), label, fill="red")
    debug.save(output)


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract one image per figure panel from a PDF.")
    parser.add_argument("pdf", type=Path, help="Source PDF")
    parser.add_argument("--out", type=Path, required=True, help="Output directory")
    parser.add_argument("--page", type=int, help="1-based page number")
    parser.add_argument("--figure", default="figure", help="Figure identifier used in filenames")
    parser.add_argument("--figure-bbox", type=parse_box, help="Figure crop bbox: x0,y0,x1,y1")
    parser.add_argument("--spec", type=Path, help="JSON spec with page, figure_bbox, and panels")
    parser.add_argument(
        "--coords",
        choices=["pdf", "pixels", "normalized"],
        default="pdf",
        help="Coordinate system for bboxes. pdf uses page points at 72 dpi.",
    )
    parser.add_argument("--dpi", type=int, default=300)
    parser.add_argument("--threshold", type=int, default=245)
    parser.add_argument("--padding", type=int, default=12, help="Panel crop padding in rendered pixels")
    parser.add_argument("--min-panel", type=int, default=160)
    parser.add_argument("--min-gutter", type=int, default=28)
    parser.add_argument("--max-panels", type=int, default=12)
    args = parser.parse_args()

    spec = load_spec(args.spec) if args.spec else {}
    page_number = int(spec.get("page") or args.page or 0)
    if page_number < 1:
        raise SystemExit("Provide --page or spec.page")

    figure_name = str(spec.get("figure") or args.figure)
    figure_bbox = spec.get("figure_bbox") or args.figure_bbox
    if not figure_bbox:
        raise SystemExit("Provide --figure-bbox or spec.figure_bbox")

    page_image, page_rect, zoom = render_page(args.pdf, page_number, args.dpi)
    figure_box = convert_box(figure_bbox, args.coords, page_rect, zoom, page_image.size)
    figure_image = page_image.crop(figure_box.as_list())

    args.out.mkdir(parents=True, exist_ok=True)
    prefix = slugify(figure_name)
    figure_path = args.out / f"{prefix}_crop.png"
    figure_image.save(figure_path)

    panel_boxes: list[tuple[str, Box]]
    if spec.get("panels"):
        panel_boxes = []
        for idx, panel in enumerate(panel_entries_from_spec(spec), start=1):
            label = str(panel.get("label") or idx)
            coords = panel.get("bbox")
            if not coords or len(coords) != 4:
                raise SystemExit(f"Panel {label} is missing bbox")
            coords_mode = str(panel.get("coords") or spec.get("coords") or args.coords)
            box = convert_box(coords, coords_mode, page_rect, zoom, page_image.size)
            box = Box(
                max(0, box.x0 - figure_box.x0),
                max(0, box.y0 - figure_box.y0),
                min(figure_image.width, box.x1 - figure_box.x0),
                min(figure_image.height, box.y1 - figure_box.y0),
            )
            panel_boxes.append((label, box))
    else:
        content = ink_bbox(figure_image, args.threshold).pad(args.padding, *figure_image.size)
        auto_boxes = split_panels(
            figure_image,
            content,
            args.threshold,
            args.min_panel,
            args.min_gutter,
            args.max_panels,
        )
        panel_boxes = [(f"{idx:02d}", box) for idx, box in enumerate(auto_boxes, start=1)]

    manifest = {
        "source_pdf": str(args.pdf),
        "page": page_number,
        "figure": figure_name,
        "dpi": args.dpi,
        "figure_crop": str(figure_path),
        "panels": [],
    }

    debug_boxes: list[tuple[str, Box]] = []
    for idx, (label, box) in enumerate(panel_boxes, start=1):
        clean_label = slugify(label)
        crop_box = box.pad(args.padding, *figure_image.size)
        output = args.out / f"{prefix}_panel_{idx:02d}_{clean_label}.png"
        figure_image.crop(crop_box.as_list()).save(output)
        debug_boxes.append((label, crop_box))
        manifest["panels"].append(
            {
                "label": label,
                "path": str(output),
                "bbox_pixels_in_figure_crop": crop_box.as_list(),
                "bbox_pixels_on_page": [
                    figure_box.x0 + crop_box.x0,
                    figure_box.y0 + crop_box.y0,
                    figure_box.x0 + crop_box.x1,
                    figure_box.y0 + crop_box.y1,
                ],
                "bbox_pdf_points_on_page": [
                    round((figure_box.x0 + crop_box.x0) / zoom, 2),
                    round((figure_box.y0 + crop_box.y0) / zoom, 2),
                    round((figure_box.x0 + crop_box.x1) / zoom, 2),
                    round((figure_box.y0 + crop_box.y1) / zoom, 2),
                ],
            }
        )

    debug_path = args.out / f"{prefix}_debug.png"
    draw_debug(figure_image, debug_boxes, debug_path)
    manifest["debug_image"] = str(debug_path)
    manifest_path = args.out / f"{prefix}_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"manifest": str(manifest_path), "panels": len(panel_boxes)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
