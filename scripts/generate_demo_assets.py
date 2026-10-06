from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "examples" / "input"


def product(color: str, accent: str, label: str, shift: int = 0) -> Image.Image:
    image = Image.new("RGB", (920, 680), "#f5f6f7")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((230 + shift, 95, 690 + shift, 585), radius=48, fill=color, outline="#26343b", width=5)
    draw.ellipse((350 + shift, 205, 570 + shift, 425), fill=accent, outline="#26343b", width=4)
    draw.rectangle((410 + shift, 125, 510 + shift, 180), fill="#fdfdfd")
    draw.text((376 + shift, 455), label, fill="#ffffff")
    return image


def main() -> None:
    INPUT.mkdir(parents=True, exist_ok=True)
    first = product("#315c72", "#ebaa52", "DEMO A")
    first.save(INPUT / "Demo Product A.png")
    first.save(INPUT / "Demo Product A copy.png")
    product("#285f4e", "#e6c763", "DEMO B", -35).save(INPUT / "Demo Product B wide.jpg", quality=94)
    product("#6c4f74", "#78c4b4", "DEMO C", 25).resize((700, 700)).save(INPUT / "Demo Product C square.webp")


if __name__ == "__main__":
    main()
