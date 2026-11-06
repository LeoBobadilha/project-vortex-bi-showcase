#!/usr/bin/env python3
"""Compare the public Power BI screenshot assets in the BI and website repositories."""
from __future__ import annotations

import argparse
import hashlib
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIX = {
    "01-Knowledge.png", "02-Research.png", "03-Executive.png",
    "12-W06-Win.png", "13-L01-Loss.png", "14-L02-Loss.png",
}
ALL = SIX | {
    "04-Performance.png", "05-Risk.png", "06-Trade-Explorer.png", "07-Validation.png",
    "08-W02-Win.png", "09-W03-Win.png", "10-W04-Win.png", "11-W05-Win.png",
}
KNOWN_BAD_BLOB = "a8eca13931878c6b686c30f3b4890e0398d977ce"


def image_info(path: Path) -> tuple[tuple[int, int], str, str]:
    raw = path.read_bytes()
    if len(raw) < 24 or raw[:8] != b"\x89PNG\r\n\x1a\n" or raw[12:16] != b"IHDR":
        raise ValueError(f"Invalid PNG header: {path}")
    size = struct.unpack(">II", raw[16:24])
    digest = hashlib.sha256(raw).hexdigest()
    blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    if blob == KNOWN_BAD_BLOB:
        raise ValueError(f"Known contaminated historical image blob: {path.name}")
    return size, digest, blob


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--website-root", type=Path, default=ROOT.parent / "project-vortex-portfolio")
    args = parser.parse_args()
    bi_dir = ROOT / "images" / "powerbi"
    site_dir = args.website_root.resolve() / "public" / "images" / "powerbi"
    bi = {p.name: p for p in bi_dir.glob("[0-9][0-9]-*.png")}
    site = {p.name: p for p in site_dir.glob("[0-9][0-9]-*.png")}
    if set(bi) != set(site):
        print(f"Screenshot filename mismatch: BI-only={sorted(set(bi)-set(site))}; website-only={sorted(set(site)-set(bi))}")
        return 1
    names = set(bi)
    if names not in (SIX, ALL):
        print(f"Expected the exact reviewed six-image set or all 14 page images; found {sorted(names)}")
        return 1
    hashes = set()
    sizes = set()
    try:
        for name in sorted(names):
            bi_size, bi_hash, _ = image_info(bi[name])
            site_size, site_hash, _ = image_info(site[name])
            if bi_hash != site_hash or bi_size != site_size:
                raise ValueError(f"Repository copies differ for {name}")
            if bi_hash in hashes:
                raise ValueError(f"Duplicate screenshot content under distinct page filenames: {name}")
            hashes.add(bi_hash)
            sizes.add(bi_size)
    except ValueError as exc:
        print(exc)
        return 1
    if len(sizes) != 1:
        print(f"Screenshot dimensions are inconsistent: {sorted(sizes)}")
        return 1
    print(f"Screenshot parity passed: {len(names)} matching PNGs at {next(iter(sizes))}; complete={len(names)==14}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
