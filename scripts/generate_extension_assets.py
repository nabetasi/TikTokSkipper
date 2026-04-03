#!/usr/bin/env python3
"""
Generate extension icons (16/48/128 PNG) and Chrome Web Store small promo tile (440×280, RGB PNG).
Requires: pip install -r scripts/requirements-assets.txt
"""
from __future__ import annotations

import platform
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


BG = (18, 18, 18)
TEXT_MUTED = (200, 200, 200)
TEXT_WHITE = (245, 245, 245)
ACCENT = (254, 44, 85)  # TikTok-like pink


def _font_candidates() -> list[tuple[str, int | None]]:
    """(path, index for .ttc)"""
    if platform.system() == "Darwin":
        return [
            ("/System/Library/Fonts/Supplemental/Arial Bold.ttf", None),
            ("/System/Library/Fonts/Supplemental/Arial.ttf", None),
            ("/System/Library/Fonts/Helvetica.ttc", 0),
        ]
    return [
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", None),
        ("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", None),
    ]


def load_font(size: int) -> ImageFont.FreeTypeFont:
    for path, idx in _font_candidates():
        p = Path(path)
        if not p.exists():
            continue
        try:
            if idx is not None and path.endswith(".ttc"):
                return ImageFont.truetype(path, size, index=idx)
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> tuple[int, int]:
    bbox = draw.textbbox((0, 0), text, font=font)
    return (bbox[2] - bbox[0], bbox[3] - bbox[1])


def draw_icon_128() -> Image.Image:
    w = h = 128
    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)

    font_tiktok = load_font(18)
    font_main = load_font(40)
    line1 = "TikTok"
    line2 = "±1s"

    tw1, th1 = text_size(draw, line1, font_tiktok)
    tw2, th2 = text_size(draw, line2, font_main)
    gap = 4
    total_h = th1 + gap + th2
    y0 = (h - total_h) // 2

    x1 = (w - tw1) // 2
    draw.text((x1, y0), line1, font=font_tiktok, fill=TEXT_MUTED)

    x2 = (w - tw2) // 2
    draw.text((x2, y0 + th1 + gap), line2, font=font_main, fill=ACCENT)

    return img


def draw_promo_tile_440x280() -> Image.Image:
    w, h = 440, 280
    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)

    font_title = load_font(36)
    font_sub = load_font(22)
    font_hint = load_font(15)

    title = "TikTok Skipper"
    sub = "±0.5s  ·  ±1s"
    hint = "Seek on tiktok.com"

    lines = [(title, font_title, TEXT_WHITE), (sub, font_sub, ACCENT), (hint, font_hint, TEXT_MUTED)]

    # Measure total block height
    heights = []
    widths = []
    for text, font, _ in lines:
        tw, th = text_size(draw, text, font)
        widths.append(tw)
        heights.append(th)
    gap = 12
    total_h = sum(heights) + gap * (len(lines) - 1)
    y = (h - total_h) // 2

    for i, (text, font, fill) in enumerate(lines):
        tw, th = text_size(draw, text, font)
        x = (w - tw) // 2
        draw.text((x, y), text, font=font, fill=fill)
        y += th + gap

    return img


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    icons_dir = root / "icons"
    icons_dir.mkdir(parents=True, exist_ok=True)

    master = draw_icon_128()
    master.save(icons_dir / "icon128.png", format="PNG", optimize=True)

    for size, name in ((48, "icon48.png"), (16, "icon16.png")):
        resized = master.resize((size, size), Image.Resampling.LANCZOS)
        resized.save(icons_dir / name, format="PNG", optimize=True)

    store = root / "store-assets"
    store.mkdir(parents=True, exist_ok=True)
    promo = draw_promo_tile_440x280()
    promo.save(store / "promotional-tile-small-440x280.png", format="PNG", optimize=True)

    print(f"Wrote {icons_dir}/icon16.png, icon48.png, icon128.png")
    print(f"Wrote {store}/promotional-tile-small-440x280.png")


if __name__ == "__main__":
    main()
