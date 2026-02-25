"""Devanagari-aware font subsetting with layout closure.

Wraps fonttools Subsetter with Nepali-optimized defaults.
CRITICAL: Never disable layout closure. It is required to preserve
GSUB/GPOS lookup chains for conjunct formation.
"""

from __future__ import annotations

from pathlib import Path

from fontTools.subset import Options, Subsetter
from fontTools.ttLib import TTFont

# Unicode ranges for subsetting
NEPALI_FULL = (
    "U+0900-097F,"  # Core Devanagari
    "U+A8E0-A8FF,"  # Devanagari Extended
    "U+1CD0-1CFF,"  # Vedic Extensions
    "U+0000-00FF,"  # Basic Latin (for mixed-script)
    "U+2000-206F"  # General Punctuation
)

NEPALI_LITE = (
    "U+0900-097F,"  # Core Devanagari only
    "U+0000-007F,"  # ASCII only
    "U+2000-206F"  # General Punctuation
)

# OpenType features to preserve (split by table for clarity)
GSUB_FEATURES = [
    "locl", "nukt", "akhn", "rphf", "rkrf", "pref",
    "blwf", "abvf", "half", "pstf", "vatu", "cjct",
    "ccmp", "calt", "liga",
]
GPOS_FEATURES = ["mark", "mkmk", "kern"]
ALL_LAYOUT_FEATURES = GSUB_FEATURES + GPOS_FEATURES


def _parse_unicode_range(range_str: str) -> list[int]:
    """Parse 'U+0900-097F,U+0000-00FF' into a list of codepoints."""
    codepoints: list[int] = []
    for part in range_str.split(","):
        part = part.strip().replace("U+", "").replace("u+", "")
        if not part:
            continue
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            for cp in range(int(start_s, 16), int(end_s, 16) + 1):
                codepoints.append(cp)
        else:
            codepoints.append(int(part, 16))
    return codepoints


def subset_font(
    input_path: str | Path,
    output_path: str | Path,
    unicode_range: str = NEPALI_FULL,
    woff2: bool = True,
) -> int:
    """Subset a font with Devanagari layout closure.

    Args:
        input_path: Source TTF/OTF file.
        output_path: Destination path (typically .woff2).
        unicode_range: Comma-separated U+XXXX-XXXX ranges.
        woff2: If True, output WOFF2 format.

    Returns:
        Output file size in bytes.
    """
    font = TTFont(str(input_path))

    options = Options()
    options.layout_features = ALL_LAYOUT_FEATURES
    # layout_closure is ON by default — do not disable it
    options.flavor = "woff2" if woff2 else None

    subsetter = Subsetter(options=options)
    subsetter.populate(unicodes=_parse_unicode_range(unicode_range))
    subsetter.subset(font)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    font.save(str(output_path))

    return output_path.stat().st_size
