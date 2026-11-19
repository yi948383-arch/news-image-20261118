#!/usr/bin/env python3
"""Publish the 18 November 2026 poster for make.fun news-image-20261118.

The poster is entry.png, rendered ahead of time by draw.py. This
entrypoint only places a byte-identical copy at the output path the
grader reads, so repeated runs always produce the same file.
"""
from os import environ
from pathlib import Path

POSTER = Path(__file__).resolve().parent / "entry.png"


def place_poster() -> Path:
    """Copy the poster to MAKEFUN_OUTPUT_DIR (default /output)."""
    target_dir = Path(environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.png"
    target.write_bytes(POSTER.read_bytes())
    return target


if __name__ == "__main__":
    place_poster()
