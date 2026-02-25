"""Build subsetted WOFF2 files for all font sources.

Run from repo root:  python scripts/build-web-fonts.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running from repo root without installing font-tools.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "packages" / "font-tools" / "src"))

from nepali_font_tools.subset import NEPALI_FULL, NEPALI_LITE, subset_font

SOURCES = Path("fonts/sources")
WEB_OUT = Path("fonts/web")


def main():
    for family_dir in sorted(SOURCES.iterdir()):
        if not family_dir.is_dir():
            continue

        family_slug = family_dir.name
        out_dir = WEB_OUT / family_slug
        out_dir.mkdir(parents=True, exist_ok=True)

        font_files = sorted(family_dir.glob("*.ttf")) + sorted(
            family_dir.glob("*.otf")
        )
        for font_file in font_files:
            stem = font_file.stem

            # Skip variable-font files (contain brackets in name)
            if "[" in font_file.name:
                continue

            # Full Devanagari+Latin subset
            full_path = out_dir / f"{stem}.woff2"
            full_size = subset_font(font_file, full_path, NEPALI_FULL)

            # Nepali-lite subset
            lite_path = out_dir / f"{stem}-nepali.woff2"
            lite_size = subset_font(font_file, lite_path, NEPALI_LITE)

            orig_size = font_file.stat().st_size
            print(
                f"  {stem}: {orig_size // 1024}KB"
                f" -> full:{full_size // 1024}KB"
                f" lite:{lite_size // 1024}KB"
            )


if __name__ == "__main__":
    main()
