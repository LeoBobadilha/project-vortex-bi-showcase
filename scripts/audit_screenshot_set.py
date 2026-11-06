#!/usr/bin/env python3
"""Validate screenshot filenames, PNG dimensions and hashes after human pixel QA."""
from __future__ import annotations

import hashlib
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = ROOT / "images" / "powerbi"
OUTPUT = ROOT / "docs" / "screenshot-manifest.json"
FILES = [
    "01-Knowledge.png", "02-Research.png", "03-Executive.png",
    "04-Performance.png", "05-Risk.png", "06-Trade-Explorer.png",
    "07-Validation.png", "08-W02-Win.png", "09-W03-Win.png",
    "10-W04-Win.png", "11-W05-Win.png", "12-W06-Win.png",
    "13-L01-Loss.png", "14-L02-Loss.png",
]


def inspect(path: Path) -> dict[str, object]:
    with path.open("rb") as stream:
        header = stream.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError(f"Not a valid PNG header: {path.name}")
    width, height = struct.unpack(">II", header[16:24])
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return {"file": path.name, "width": width, "height": height, "sha256": digest}


def main() -> int:
    missing = [name for name in FILES if not (IMAGE_DIR / name).is_file()]
    if missing:
        print("Missing screenshot(s): " + ", ".join(missing))
        return 1
    records = [inspect(IMAGE_DIR / name) for name in FILES]
    dimensions = {(row["width"], row["height"]) for row in records}
    if len(dimensions) != 1:
        print(f"Inconsistent screenshot dimensions: {sorted(dimensions)}")
        return 1
    width, height = next(iter(dimensions))
    if width < 1920 or height < 1080 or abs(width / height - 16 / 9) > 0.01:
        print(f"Screenshots must be at least 1920x1080 and close to 16:9; found {width}x{height}")
        return 1
    digests = [str(row["sha256"]) for row in records]
    if len(set(digests)) != len(digests):
        print("Duplicate image content detected across distinct report-page filenames")
        return 1
    manifest = {
        "source": "Power BI Desktop 2.159.1231.0 window captures from one refreshed session on 2026-11-06, taken with scripts/capture-powerbi-pages.ps1",
        "review": "All 14 images pixel-reviewed; see docs/screenshot-qa-2026-11-06.md. Re-review after any recapture.",
        "slicerState": "Pages 04 and 05 captured with P6 + SIZE + CE selected",
        "pages": records,
    }
    OUTPUT.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Validated {len(records)} PNG files at {next(iter(dimensions))}; wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
