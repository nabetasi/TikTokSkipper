#!/usr/bin/env python3
"""PNG icons without third-party deps (Manifest / Chrome Web Store)."""
from __future__ import annotations

import struct
import zlib
from pathlib import Path


def _chunk(chunk_type: bytes, data: bytes) -> bytes:
    crc = zlib.crc32(chunk_type + data) & 0xFFFFFFFF
    return struct.pack(">I", len(data)) + chunk_type + data + struct.pack(">I", crc)


def write_png_rgba(path: Path, size: int, rgba: tuple[int, int, int, int]) -> None:
    r, g, b, a = rgba
    # Each scanline: filter 0 + RGBA pixels
    row = bytes([0]) + bytes([r, g, b, a]) * size
    raw = row * size
    compressed = zlib.compress(raw, 9)

    ihdr = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)
    png = (
        b"\x89PNG\r\n\x1a\n"
        + _chunk(b"IHDR", ihdr)
        + _chunk(b"IDAT", compressed)
        + _chunk(b"IEND", b"")
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(png)


def main() -> None:
    root = Path(__file__).resolve().parents[1] / "icons"
    # TikTok-like accent (approx): #fe2c55
    color = (254, 44, 85, 255)
    for name, size in (("icon16.png", 16), ("icon48.png", 48), ("icon128.png", 128)):
        write_png_rgba(root / name, size, color)
    print(f"Wrote icons under {root}")


if __name__ == "__main__":
    main()
