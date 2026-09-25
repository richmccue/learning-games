"""
Generates the Meditation Timer icon set.

Motif: a simple singing-bowl glyph (a wide shallow arc "bowl" with two thin
soundwave ripples above it) rendered in brass on a deep dusk gradient. The
same glyph is reused for every icon size so the ripple/bowl idea stays the
single consistent mark across the whole app (favicon-style icons, the
progress ring on the session screen, and the app-install icon all share it).

Run: python3 make_icons.py
"""

import math
from PIL import Image, ImageDraw

# Palette (matches the CSS custom properties in index.html)
DUSK_TOP = (28, 31, 41)      # #1C1F29
DUSK_BOTTOM = (18, 20, 27)   # #12141B
BRASS = (176, 141, 78)       # #B08D4E
BRASS_LIGHT = (214, 188, 138)  # lighter brass for the ripple lines


def radial_gradient(size):
    """Soft diagonal gradient background, dusk top-left to darker bottom-right."""
    img = Image.new("RGB", (size, size))
    px = img.load()
    for y in range(size):
        for x in range(size):
            t = (x + y) / (2 * size)
            r = int(DUSK_TOP[0] + (DUSK_BOTTOM[0] - DUSK_TOP[0]) * t)
            g = int(DUSK_TOP[1] + (DUSK_BOTTOM[1] - DUSK_TOP[1]) * t)
            b = int(DUSK_TOP[2] + (DUSK_BOTTOM[2] - DUSK_TOP[2]) * t)
            px[x, y] = (r, g, b)
    return img


def draw_glyph(draw, cx, cy, scale):
    """Draws the bowl + two ripple arcs centered at (cx, cy). scale ~= icon size."""
    bowl_w = scale * 0.62
    bowl_h = scale * 0.30
    bowl_top = cy + scale * 0.06

    # Bowl: bottom half of an ellipse (a shallow dish), plus a thin rim line
    bbox = [cx - bowl_w / 2, bowl_top - bowl_h / 2, cx + bowl_w / 2, bowl_top + bowl_h / 2]
    draw.pieslice(bbox, start=0, end=180, fill=BRASS)
    rim_w = max(2, int(scale * 0.018))
    draw.arc(bbox, start=0, end=180, fill=BRASS_LIGHT, width=rim_w)

    # Two soundwave ripples above the bowl
    for i, frac in enumerate((0.62, 0.40)):
        w = bowl_w * frac
        h = scale * 0.16 * (1 - i * 0.15)
        y = bowl_top - scale * (0.30 + i * 0.16)
        bbox_r = [cx - w / 2, y - h / 2, cx + w / 2, y + h / 2]
        width = max(2, int(scale * (0.028 - i * 0.006)))
        draw.arc(bbox_r, start=200, end=340, fill=BRASS_LIGHT, width=width)


def make_icon(size, maskable=False, transparent=False, path="icon.png"):
    img = radial_gradient(size).convert("RGBA")

    if transparent:
        # Punch a soft circular vignette so the corners can read as transparent
        # (not used for the standard icons, kept simple/solid per iOS guidance).
        pass

    draw = ImageDraw.Draw(img)

    if maskable:
        # Keep the glyph inside the ~80% "safe zone" that OS masks won't crop.
        safe = size * 0.40
        draw_glyph(draw, size / 2, size / 2 + size * 0.02, safe * 2)
    else:
        draw_glyph(draw, size / 2, size / 2 + size * 0.02, size * 0.62)

    img.save(path, "PNG")
    print(f"wrote {path} ({size}x{size}, maskable={maskable})")


if __name__ == "__main__":
    make_icon(192, path="icons/icon-192.png")
    make_icon(512, path="icons/icon-512.png")
    make_icon(512, maskable=True, path="icons/icon-maskable-512.png")
    make_icon(180, path="icons/apple-touch-icon.png")
