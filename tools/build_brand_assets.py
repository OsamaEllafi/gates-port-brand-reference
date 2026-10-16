"""Rebuild the GatesPort logo set as true vector artwork, then render the PNGs from it.

The GP emblem is traced (sub-pixel marching squares) from the approved reference image.
The wordmark and descriptor are real Montserrat glyph outlines, so every SVG is pure vector
and every PNG is rasterised from that same SVG at full resolution.

Requires: numpy, opencv-python, scikit-image, fonttools, Pillow, and ImageMagick (`magick`).
"""

from __future__ import annotations

import shutil
import subprocess
import time
from pathlib import Path

import cv2
import numpy as np
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from PIL import Image
from skimage import measure


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

CANVAS_W, CANVAS_H = 3000, 650
EMBLEM_GAP = 160  # space between the emblem and the wordmark
UPSCALE = 10  # source pixels are upscaled this much before contours are traced

# Wordmark: Montserrat Bold 190 px. Descriptor: Montserrat Medium 86 px, widely tracked.
MAIN = {"size": 190, "weight": 700, "tracking": 4, "top": 82, "text": "GATESPORT"}
DESCRIPTOR = {"size": 86, "weight": 500, "tracking": 42, "top": 345, "x_nudge": 6}


def num(value: float) -> str:
    return f"{value:.2f}".rstrip("0").rstrip(".")


# --------------------------------------------------------------------------- emblem


def trace_emblem() -> tuple[list[np.ndarray], float, float]:
    """Return closed emblem contours scaled to a 650 px tall box, plus that box's width."""
    image = Image.open(REFERENCE).convert("RGB")
    crop = np.array(image.crop((590, 135, 940, 315))).astype(np.float32).mean(axis=2)
    ink_ratio = np.clip((np.percentile(crop, 98) - crop) / (np.percentile(crop, 98) - np.percentile(crop, 2)), 0, 1)
    big = cv2.resize(ink_ratio, None, fx=UPSCALE, fy=UPSCALE, interpolation=cv2.INTER_CUBIC)
    big = cv2.GaussianBlur(big, (0, 0), UPSCALE * 0.45)

    contours = []
    for contour in measure.find_contours(big, 0.5):
        if not np.allclose(contour[0], contour[-1]):
            continue  # open contour: touches the crop edge, so it is not part of the emblem
        x, y = contour[:, 1], contour[:, 0]
        area = 0.5 * abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
        if area < 2000:
            continue  # scanner dust
        contours.append(measure.approximate_polygon(contour, tolerance=0.2))

    ys = np.concatenate([c[:, 0] for c in contours])
    xs = np.concatenate([c[:, 1] for c in contours])
    x0, y0 = xs.min(), ys.min()
    scale = CANVAS_H / (ys.max() - y0)
    scaled = [np.column_stack(((c[:, 1] - x0) * scale, (c[:, 0] - y0) * scale)) for c in contours]
    return scaled, float((xs.max() - x0) * scale), scale


def emblem_path(contours: list[np.ndarray]) -> str:
    parts = []
    for contour in contours:
        points = contour[:-1]
        parts.append("M" + "L".join(f"{num(x)} {num(y)}" for x, y in points) + "Z")
    return "".join(parts)


# --------------------------------------------------------------------------- text


class Face:
    """One Montserrat instance whose glyphs can be laid out as SVG path data."""

    def __init__(self, weight: int) -> None:
        font = instancer.instantiateVariableFont(TTFont(FONT_FILE), {"wght": weight})
        self.glyphs = font.getGlyphSet()
        self.cmap = font.getBestCmap()
        self.hmtx = font["hmtx"]
        self.upem = font["head"].unitsPerEm
        self.cap_height = font["OS/2"].sCapHeight

    def layout(self, text: str, x: float, top: float, size: float, tracking: float) -> tuple[str, float]:
        scale = size / self.upem
        baseline = top + self.cap_height * scale  # `top` is the cap line, as in the approved lockup
        paths = []
        for character in text:
            name = self.cmap[ord(character)]
            pen = SVGPathPen(self.glyphs, ntos=num)
            self.glyphs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, x, baseline)))
            paths.append(pen.getCommands())
            x += self.hmtx[name][0] * scale + tracking
        return "".join(paths), x - tracking


# --------------------------------------------------------------------------- svg


def lockup_svg(emblem: str, emblem_width: float, colour: str, descriptor: str, label: str, faces: dict[int, Face]) -> str:
    text_x = emblem_width + EMBLEM_GAP
    word, _ = faces[MAIN["weight"]].layout(MAIN["text"], text_x, MAIN["top"], MAIN["size"], MAIN["tracking"])
    sub, _ = faces[DESCRIPTOR["weight"]].layout(
        descriptor, text_x + DESCRIPTOR["x_nudge"], DESCRIPTOR["top"], DESCRIPTOR["size"], DESCRIPTOR["tracking"]
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
        f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" role="img" aria-label="{label}">'
        f'<g fill="{colour}"><path fill-rule="evenodd" d="{emblem}"/><path d="{word}"/><path d="{sub}"/></g></svg>'
    )


def emblem_svg(emblem: str, emblem_width: float, colour: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{round(emblem_width)}" height="{CANVAS_H}" '
        f'viewBox="0 0 {num(emblem_width)} {CANVAS_H}" role="img" aria-label="GatesPort emblem">'
        f'<path fill="{colour}" fill-rule="evenodd" d="{emblem}"/></svg>'
    )


def write_text(path: Path, text: str) -> None:
    """Write a file, retrying briefly: OneDrive can hold a lock on freshly written files."""
    for attempt in range(5):
        try:
            path.write_text(text, encoding="utf-8")
            return
        except OSError:
            if attempt == 4:
                raise
            time.sleep(0.5)


def render_png(svg_path: Path, png_path: Path, width: int, height: int) -> None:
    """Rasterise an SVG with ImageMagick at exactly width x height, transparent background."""
    subprocess.run(
        ["magick", "-background", "none", "-density", "96", str(svg_path), "-resize", f"{width}x{height}!", f"PNG32:{png_path}"],
        check=True,
    )


def main() -> None:
    if shutil.which("magick") is None:
        raise SystemExit("ImageMagick (`magick`) is required to render the PNG files.")

    OUTPUT.mkdir(parents=True, exist_ok=True)
    contours, emblem_width, _ = trace_emblem()
    emblem = emblem_path(contours)
    faces = {weight: Face(weight) for weight in (MAIN["weight"], DESCRIPTOR["weight"])}
    emblem_png_width = round(emblem_width)

    for name, colour in COLOURS.items():
        svg_file = OUTPUT / f"gates-port-emblem-{name}.svg"
        write_text(svg_file, emblem_svg(emblem, emblem_width, colour))
        render_png(svg_file, OUTPUT / f"gates-port-emblem-{name}.png", emblem_png_width, CANVAS_H)

        for brand, (descriptor, label) in BRANDS.items():
            # Aviation keeps its original file names; subsidiaries add the brand slug.
            stem = f"gates-port-logo-{name}" if brand == "aviation" else f"gates-port-{brand}-logo-{name}"
            svg_file = OUTPUT / f"{stem}.svg"
            write_text(svg_file, lockup_svg(emblem, emblem_width, colour, descriptor, label, faces))
            render_png(svg_file, OUTPUT / f"{stem}.png", CANVAS_W, CANVAS_H)

    # Primary aliases intentionally use the flat antique-gold production artwork.
    for alias, source in (
        ("gates-port-logo-primary.png", "gates-port-logo-gold.png"),
        ("gates-port-logo-primary-4x.png", "gates-port-logo-gold.png"),
        ("gates-port-emblem-primary.png", "gates-port-emblem-gold.png"),
        ("gates-port-emblem-primary-6x.png", "gates-port-emblem-gold.png"),
    ):
        (OUTPUT / alias).write_bytes((OUTPUT / source).read_bytes())

    print(f"emblem {emblem_png_width}x{CANVAS_H}; {len(contours)} contours; {len(emblem)//1024} KB path")


if __name__ == "__main__":
    main()
