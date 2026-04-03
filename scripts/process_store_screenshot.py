#!/usr/bin/env python3
"""
Chrome Web Store 用スクリーンショット加工:
- 顔・ユーザー名・動画内容を強いぼかしで匿名化
- 拡張の操作ボタン部分のみ鮮明に残す（領域は定数で調整可）
- 1280×800 または 640×400、RGB PNG（アルファなし）

使用例:
  python3 scripts/process_store_screenshot.py path/to/screenshot.png
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image, ImageFilter


# 元画像上で「拡張のボタンだけ鮮明に残す」矩形（比率で指定、右寄せクロップ後も破綻しにくいようやや広め）
PATCH_X0_FRAC = 0.74
PATCH_X1_FRAC = 1.0
PATCH_Y0_FRAC = 0.22
PATCH_Y1_FRAC = 0.68

BLUR_RADIUS = 22


def cover_crop_right(
    im: Image.Image, out_w: int, out_h: int
) -> Image.Image:
    """アスペクト比を保って拡大し、横方向は右端優先で out_w×out_h に切り出す。"""
    w, h = im.size
    scale = max(out_w / w, out_h / h)
    nw, nh = math.ceil(w * scale), math.ceil(h * scale)
    resized = im.resize((nw, nh), Image.Resampling.LANCZOS)

    if nw >= out_w:
        left = nw - out_w
    else:
        left = 0
    if nh >= out_h:
        top = (nh - out_h) // 2
    else:
        top = 0

    return resized.crop((left, top, left + out_w, top + out_h))


def anonymize_for_store(im: Image.Image) -> Image.Image:
    """全体を強くぼかし、拡張 UI 付近だけ元の解像度で貼り戻す。"""
    im = im.convert("RGB")
    w, h = im.size
    blurred = im.filter(ImageFilter.GaussianBlur(BLUR_RADIUS))
    bx0 = int(w * PATCH_X0_FRAC)
    bx1 = int(w * PATCH_X1_FRAC)
    by0 = int(h * PATCH_Y0_FRAC)
    by1 = int(h * PATCH_Y1_FRAC)
    patch = im.crop((bx0, by0, bx1, by1))
    out = blurred.copy()
    out.paste(patch, (bx0, by0))
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input",
        type=Path,
        nargs="?",
        default=None,
        help="入力 PNG/JPEG（未指定時は store-assets/screenshots/source-screenshot.png）",
    )
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    src = args.input or (root / "store-assets/screenshots/source-screenshot.png")
    if not src.is_file():
        raise SystemExit(f"入力が見つかりません: {src}")

    out_dir = root / "store-assets/screenshots"
    out_dir.mkdir(parents=True, exist_ok=True)

    im = Image.open(src)
    processed = anonymize_for_store(im)

    out_1280 = out_dir / "chrome-web-store-1280x800.png"
    out_640 = out_dir / "chrome-web-store-640x400.png"

    cover1280 = cover_crop_right(processed, 1280, 800)
    cover1280.save(out_1280, format="PNG", optimize=True)

    cover640 = cover1280.resize((640, 400), Image.Resampling.LANCZOS)
    cover640.save(out_640, format="PNG", optimize=True)

    print(f"Wrote {out_1280}")
    print(f"Wrote {out_640}")
    print("Mode: RGB, no alpha (PNG 24-bit)")


if __name__ == "__main__":
    main()
