#!/usr/bin/env python3
"""Entrypoint for the make.fun news-image-20261125 submission.

Standard library only. Copies the pre-rendered front page
(entry.png, 1024x1024, drawn by draw.py at build time) to the
output directory and verifies the copy byte for byte.

Run:  MAKEFUN_OUTPUT_DIR=out python3 main.py
Without MAKEFUN_OUTPUT_DIR the image goes to /output/entry.png.
"""
import hashlib
import os
import shutil
import struct
import sys

OUT_DIR = "/output"
IMAGE = "entry.png"
EXPECT_W, EXPECT_H = 1024, 1024


def here():
    return os.path.dirname(os.path.abspath(__file__))


def read_header(path):
    with open(path, "rb") as fh:
        head = fh.read(33)
    if len(head) < 33 or head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path}: not a PNG file")
    if head[12:16] != b"IHDR":
        raise ValueError(f"{path}: PNG without IHDR")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    src = os.path.join(here(), IMAGE)
    if not os.path.isfile(src):
        print(f"error: {src} missing", file=sys.stderr)
        return 1
    w, h = read_header(src)
    if (w, h) != (EXPECT_W, EXPECT_H):
        print(f"error: {src} is {w}x{h}, want 1024x1024", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or OUT_DIR
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, IMAGE)
    shutil.copyfile(src, dst)
    if read_header(dst) != (EXPECT_W, EXPECT_H):
        print(f"error: {dst} failed verification", file=sys.stderr)
        return 1
    if digest(dst) != digest(src):
        print("error: copy differs from source (sha256)", file=sys.stderr)
        return 1
    print(f"wrote {dst}: {os.path.getsize(dst)} bytes, sha256 {digest(dst)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
