#!/usr/bin/env python3
"""Copy passport.png (rendered by render.py) to /output/entry.png,
fitted within 1024x1024. PNG unless over 1 MiB, then JPEG quality 90.
Deterministic, no network."""
import io
import os
from pathlib import Path

from PIL import Image

LIMIT = 1_048_576


def main():
    src = Path(__file__).resolve().parent / "passport.png"
    img = Image.open(src).convert("RGB")
    img.thumbnail((1024, 1024), Image.LANCZOS)
    os.makedirs("/output", exist_ok=True)
    out = Path("/output/entry.png")
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    if buf.tell() <= LIMIT:
        out.write_bytes(buf.getvalue())
    else:
        img.save(out, format="JPEG", quality=90)
    print(out, out.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
