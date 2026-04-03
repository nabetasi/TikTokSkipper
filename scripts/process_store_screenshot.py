#!/usr/bin/env python3
"""
Chrome Web Store 用スクリーンショット加工:
- 中央の動画コンテンツ帯のみ強いぼかし（左の TikTok ロゴ・メニュー、右の UI は鮮明）
- 切り抜きは行わず、アスペクト比を維持してキャンバス内に全体を収め、余白はレターボックスで埋める
- 1280×800 または 640×400、RGB PNG（アルファなし）

使用例:
  python3 scripts/process_store_screenshot.py path/to/screenshot.png
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image, ImageFilter


# 元画像幅に対する比率: 左端〜この位置まで「ぼかさない」（サイドバー・ロゴ）
LEFT_SHARP_END_FRAC = 0.24
# この位置から右端まで「ぼかさない」（いいね等・拡張ボタン）
RIGHT_SHARP_START_FRAC = 0.70
# その間が中央コンテンツ（ぼかし対象）

BLUR_RADIUS = 22
# レターボックスの背景（TikTok ダークに近いグレー）
PAD_BG = (18, 18, 18)


def contain_pad(
    im: Image.Image, out_w: int, out_h: int, bg: tuple[int, int, int] = PAD_BG
) -> Image.Image:
    """
    アスペクト比を維持したまま out_w×out_h の箱に全体が収まるよう縮小・拡大し、
    不足分は上下または左右に余白（レターボックス）を付ける。クロップしない。
    """
    im = im.convert("RGB")
    w, h = im.size
    scale = min(out_w / w, out_h / h)
    nw = max(1, int(round(w * scale)))
    nh = max(1, int(round(h * scale)))
    resized = im.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (out_w, out_h), bg)
    left = (out_w - nw) // 2
    top = (out_h - nh) // 2
    canvas.paste(resized, (left, top))
    return canvas


def anonymize_for_store(im: Image.Image) -> Image.Image:
    """
    画面全体をぼかしたうえで、左ストリップと右ストリップに元画像を貼り戻す。
    中央の動画エリアのみぼかしが残る。
    """
    im = im.convert("RGB")
    w, h = im.size
    x_left = int(w * LEFT_SHARP_END_FRAC)
    x_right = int(w * RIGHT_SHARP_START_FRAC)
    if x_left >= x_right:
        raise ValueError(
            "LEFT_SHARP_END_FRAC は RIGHT_SHARP_START_FRAC より小さくしてください。"
        )

    blurred = im.filter(ImageFilter.GaussianBlur(BLUR_RADIUS))
    out = blurred.copy()

    # 左サイドバー（ロゴ・メニュー）
    if x_left > 0:
        strip_l = im.crop((0, 0, x_left, h))
        out.paste(strip_l, (0, 0))

    # 右側（操作列・拡張ボタン）
    if x_right < w:
        strip_r = im.crop((x_right, 0, w, h))
        out.paste(strip_r, (x_right, 0))

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

    fit1280 = contain_pad(processed, 1280, 800)
    fit1280.save(out_1280, format="PNG", optimize=True)

    fit640 = contain_pad(processed, 640, 400)
    fit640.save(out_640, format="PNG", optimize=True)

    print(f"Wrote {out_1280}")
    print(f"Wrote {out_640}")
    print("Mode: RGB, no alpha (PNG 24-bit); layout: contain + letterbox, no crop")


if __name__ == "__main__":
    main()
