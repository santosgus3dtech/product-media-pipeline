from __future__ import annotations

import hashlib
import re
import unicodedata
from pathlib import Path

from PIL import Image, ImageChops, ImageOps


VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", normalized.lower()).strip("-")
    return slug or "product"


def exact_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def difference_hash(image: Image.Image, size: int = 9) -> str:
    gray = ImageOps.grayscale(image).resize((size, size - 1), Image.Resampling.LANCZOS)
    pixels = list(gray.get_flattened_data())
    bits = []
    for row in range(size - 1):
        offset = row * size
        bits.extend(pixels[offset + column] > pixels[offset + column + 1] for column in range(size - 1))
    value = sum(bit << index for index, bit in enumerate(bits))
    return f"{value:0{len(bits) // 4}x}"


def visible_bbox(image: Image.Image) -> tuple[int, int, int, int] | None:
    rgba = image.convert("RGBA")
    alpha = rgba.getchannel("A")
    if alpha.getextrema() != (255, 255):
        return alpha.getbbox()
    background = Image.new("RGB", rgba.size, rgba.convert("RGB").getpixel((0, 0)))
    return ImageChops.difference(rgba.convert("RGB"), background).getbbox()


def normalize(image: Image.Image, canvas: int = 1200, margin: int = 110) -> Image.Image:
    rgba = image.convert("RGBA")
    bbox = visible_bbox(rgba)
    if bbox:
        rgba = rgba.crop(bbox)
    available = canvas - margin * 2
    rgba.thumbnail((available, available), Image.Resampling.LANCZOS)
    output = Image.new("RGBA", (canvas, canvas), (248, 249, 250, 255))
    position = ((canvas - rgba.width) // 2, (canvas - rgba.height) // 2)
    output.alpha_composite(rgba, position)
    return output.convert("RGB")
