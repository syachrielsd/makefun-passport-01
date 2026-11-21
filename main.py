#!/usr/bin/env python3
"""Copy passport.png (pre-rendered by render.py at 1024x724, already
inside the 1024x1024 / 1 MiB gate) verbatim to entry.png in the output
directory. Standard library only, deterministic, no network."""
import os
from pathlib import Path

LIMIT = 1_048_576


def main():
    src = Path(__file__).resolve().parent / "passport.png"
    data = src.read_bytes()
    assert len(data) <= LIMIT, f"passport.png is {len(data)} bytes, over the 1 MiB gate"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    os.makedirs(out_dir, exist_ok=True)
    out = out_dir / "entry.png"
    out.write_bytes(data)
    print(out, out.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
