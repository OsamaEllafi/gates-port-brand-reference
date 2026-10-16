"""Rebuild high-resolution brand lockups from the approved reference artwork."""

from __future__ import annotations

import base64
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[2]
REFERENCE = ROOT / "hero-concepts" / "approved-brand-reference.png"
FONT_FILE = ROOT / "brand-reference" / "assets" / "fonts" / "Montserrat.ttf"
OUTPUT = ROOT / "brand-reference" / "assets" / "logos"

COLOURS = {
    "gold": "#B39567",
    "burgundy": "#48151D",
    "cream": "#F0E5D2",
    "white": "#FFFFFF",
    "black": "#111111",
}

# Holding company first, then its subsidiaries. Each brand shares the GP emblem
# and the GATESPORT wordmark; only the descriptor line changes.
BRANDS = {
    "aviation": ("AVIATION", "GatesPort Aviation"),
    "cargo": ("CARGO", "GatesPort Cargo"),
    "catering": ("CATERING", "GatesPort Catering"),
    "vip": ("VIP", "GatesPort VIP"),
}


def tracked_text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, font: ImageFont.FreeTypeFont, fill: str, tracking: int) -> int:
    x, y = xy
    for character in text:
        draw.text((x, y), character, font=font, fill=fill, anchor="lt")
        x += int(draw.textlength(character, font=font)) + tracking
    return x


def get_emblem_mask() -> Image.Image:
    image = Image.open(REFERENCE).convert("RGB")
    crop = image.crop((590, 135, 940, 315))
    pixels = np.array(crop)
    # The selected reference area contains only the cream canvas and burgundy mark.
    mask = np.where(np.mean(pixels, axis=2) < 175, 255, 0).astype(np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    ys, xs = np.where(mask > 0)
    mask = mask[ys.min() : ys.max() + 1, xs.min() : xs.max() + 1]
    pil_mask = Image.fromarray(mask, mode="L")
    return pil_mask.resize((1500, 650), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(0.35))


def build_emblem_svg(mask: Image.Image, colour: str, destination: Path) -> None:
    small = np.array(mask.resize((600, 260), Image.Resampling.LANCZOS))
    _, binary = cv2.threshold(small, 128, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    path_parts: list[str] = []
    for contour in contours:
        if cv2.contourArea(contour) < 16:
            continue
        points = cv2.approxPolyDP(contour, 0.7, True).reshape(-1, 2)
        path_parts.append("M " + " L ".join(f"{x} {y}" for x, y in points) + " Z")
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 260" role="img" '
        'aria-label="Gates Port emblem">'
        f'<path fill="{colour}" fill-rule="evenodd" d="{" ".join(path_parts)}"/>'
        "</svg>"
    )
    destination.write_text(svg, encoding="utf-8")


def build_lockup(mask: Image.Image, colour: str, descriptor: str = "AVIATION") -> Image.Image:
    canvas = Image.new("RGBA", (3000, 650), (0, 0, 0, 0))
    emblem = Image.new("RGBA", mask.size, colour)
    emblem.putalpha(mask)
    canvas.alpha_composite(emblem, (0, 0))

    draw = ImageDraw.Draw(canvas)
    main_font = ImageFont.truetype(FONT_FILE, 190)
    main_font.set_variation_by_name("Bold")
    descriptor_font = ImageFont.truetype(FONT_FILE, 86)
    descriptor_font.set_variation_by_name("Medium")
    tracked_text(draw, (1660, 82), "GATESPORT", main_font, colour, 4)
    tracked_text(draw, (1666, 345), descriptor, descriptor_font, colour, 42)
    return canvas


def build_lockup_svg(mask: Image.Image, colour: str, destination: Path, descriptor: str = "AVIATION", label: str = "GatesPort Aviation") -> None:
    png = build_lockup(mask, colour, descriptor)
    buffer = __import__("io").BytesIO()
    png.save(buffer, format="PNG", optimize=True)
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 3000 650" role="img" '
        f'aria-label="{label}">'
        f'<image width="3000" height="650" href="data:image/png;base64,{encoded}"/>'
        "</svg>"
    )
    destination.write_text(svg, encoding="utf-8")


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    mask = get_emblem_mask()
    for name, colour in COLOURS.items():
        emblem = Image.new("RGBA", mask.size, colour)
        emblem.putalpha(mask)
        emblem.save(OUTPUT / f"gates-port-emblem-{name}.png", optimize=True)
        build_emblem_svg(mask, colour, OUTPUT / f"gates-port-emblem-{name}.svg")
        for brand, (descriptor, label) in BRANDS.items():
            # Aviation keeps its original file names; subsidiaries add the brand slug.
            stem = f"gates-port-logo-{name}" if brand == "aviation" else f"gates-port-{brand}-logo-{name}"
            build_lockup(mask, colour, descriptor).save(OUTPUT / f"{stem}.png", optimize=True)
            build_lockup_svg(mask, colour, OUTPUT / f"{stem}.svg", descriptor, label)

    # Primary aliases intentionally use the flat antique-gold production artwork.
    (OUTPUT / "gates-port-logo-primary.png").write_bytes((OUTPUT / "gates-port-logo-gold.png").read_bytes())
    (OUTPUT / "gates-port-logo-primary-4x.png").write_bytes((OUTPUT / "gates-port-logo-gold.png").read_bytes())
    (OUTPUT / "gates-port-emblem-primary.png").write_bytes((OUTPUT / "gates-port-emblem-gold.png").read_bytes())
    (OUTPUT / "gates-port-emblem-primary-6x.png").write_bytes((OUTPUT / "gates-port-emblem-gold.png").read_bytes())


if __name__ == "__main__":
    main()
