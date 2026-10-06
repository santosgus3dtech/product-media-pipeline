from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

from .images import VALID_EXTENSIONS, difference_hash, exact_hash, normalize, slugify


def process_directory(source: Path, destination: Path, canvas: int = 1200) -> dict:
    destination.mkdir(parents=True, exist_ok=True)
    files = sorted(path for path in source.iterdir() if path.is_file() and path.suffix.lower() in VALID_EXTENSIONS)
    records = []
    seen_exact: dict[str, str] = {}
    seen_visual: dict[str, str] = {}
    for index, path in enumerate(files, start=1):
        with Image.open(path) as opened:
            opened.load()
            visual_hash = difference_hash(opened)
            width, height = opened.size
            normalized = normalize(opened, canvas=canvas)
        digest = exact_hash(path)
        output_name = f"{index:02d}-{slugify(path.stem)}.jpg"
        output_path = destination / output_name
        normalized.save(output_path, "JPEG", quality=91, optimize=True, progressive=True)
        duplicate_of = seen_exact.get(digest) or seen_visual.get(visual_hash)
        records.append(
            {
                "source": path.name,
                "output": output_name,
                "source_size": [width, height],
                "output_size": [canvas, canvas],
                "sha256": digest,
                "difference_hash": visual_hash,
                "duplicate_of": duplicate_of,
            }
        )
        seen_exact.setdefault(digest, output_name)
        seen_visual.setdefault(visual_hash, output_name)
    manifest = {
        "schema": 1,
        "source_count": len(files),
        "duplicate_count": sum(record["duplicate_of"] is not None for record in records),
        "canvas": [canvas, canvas],
        "records": records,
    }
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_contact_sheet(destination, records)
    return manifest


def write_contact_sheet(destination: Path, records: list[dict]) -> None:
    if not records:
        return
    thumb_size = 250
    padding = 24
    columns = 3
    rows = (len(records) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * (thumb_size + padding) + padding, rows * (thumb_size + 62 + padding) + padding), "#eef1f2")
    draw = ImageDraw.Draw(sheet)
    for index, record in enumerate(records):
        row, column = divmod(index, columns)
        x = padding + column * (thumb_size + padding)
        y = padding + row * (thumb_size + 62 + padding)
        with Image.open(destination / record["output"]) as image:
            thumb = ImageOps.contain(image, (thumb_size, thumb_size), Image.Resampling.LANCZOS)
            sheet.paste(thumb, (x + (thumb_size - thumb.width) // 2, y + (thumb_size - thumb.height) // 2))
        draw.text((x, y + thumb_size + 12), record["output"], fill="#1d2a30")
        state = f"Duplicate of {record['duplicate_of']}" if record["duplicate_of"] else "Unique asset"
        draw.text((x, y + thumb_size + 32), state, fill="#627079")
    sheet.save(destination / "contact-sheet.png", optimize=True)
