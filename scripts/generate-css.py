"""Generate @font-face CSS for each web font family.

Run from repo root:  python scripts/generate-css.py

Generates two CSS files per family:
  <family>.css         — full Devanagari+Latin subset
  <family>-nepali.css  — Nepali-only lite subset
"""

from __future__ import annotations

from pathlib import Path

WEB_DIR = Path("fonts/web")
CSS_OUT = Path("packages/web-fonts/css")

# Relative path from packages/web-fonts/css/ to fonts/web/
FONT_REL = "../../fonts/web"

# Map filename patterns to CSS font-weight values.
# Ordered longest-first so "extrabold" matches before "bold".
WEIGHT_MAP = [
    ("extralight", 200),
    ("extrabold", 800),
    ("semibold", 600),
    ("thin", 100),
    ("light", 300),
    ("regular", 400),
    ("medium", 500),
    ("bold", 700),
    ("black", 900),
]

UNICODE_RANGE_FULL = (
    "U+0900-097F, U+A8E0-A8FF, U+1CD0-1CFF, U+0000-00FF, U+2000-206F"
)
UNICODE_RANGE_NEPALI = "U+0900-097F, U+0000-007F, U+2000-206F"


def _font_weight(stem: str) -> int:
    """Derive CSS font-weight from filename stem."""
    lower = stem.lower()
    for name, value in WEIGHT_MAP:
        if name in lower:
            return value
    return 400


def _face_block(
    family_name: str, family_slug: str, woff2_name: str, weight: int, unicode_range: str
) -> str:
    return (
        f"@font-face {{\n"
        f"  font-family: '{family_name}';\n"
        f"  font-style: normal;\n"
        f"  font-weight: {weight};\n"
        f"  font-display: swap;\n"
        f"  src: url('{FONT_REL}/{family_slug}/{woff2_name}') format('woff2');\n"
        f"  unicode-range: {unicode_range};\n"
        f"}}\n"
    )


def generate_css(family_dir: Path) -> None:
    family_slug = family_dir.name
    family_name = family_slug.replace("-", " ").title()

    full_lines = [f"/* {family_name} — @nepalibhasha/fonts */\n"]
    lite_lines = [f"/* {family_name} (Nepali subset) — @nepalibhasha/fonts */\n"]

    for woff2 in sorted(family_dir.glob("*.woff2")):
        if "-nepali" in woff2.name:
            # Lite variant
            weight = _font_weight(woff2.stem.replace("-nepali", ""))
            lite_lines.append(
                _face_block(family_name, family_slug, woff2.name, weight, UNICODE_RANGE_NEPALI)
            )
        else:
            # Full variant
            weight = _font_weight(woff2.stem)
            full_lines.append(
                _face_block(family_name, family_slug, woff2.name, weight, UNICODE_RANGE_FULL)
            )

    CSS_OUT.mkdir(parents=True, exist_ok=True)

    full_path = CSS_OUT / f"{family_slug}.css"
    full_path.write_text("\n".join(full_lines))

    lite_path = CSS_OUT / f"{family_slug}-nepali.css"
    lite_path.write_text("\n".join(lite_lines))

    print(f"  {full_path} ({len(full_lines) - 1} faces)")
    print(f"  {lite_path} ({len(lite_lines) - 1} faces)")


def main() -> None:
    if not WEB_DIR.exists():
        print("fonts/web/ not found — run build-web-fonts.py first.")
        return

    for family_dir in sorted(WEB_DIR.iterdir()):
        if not family_dir.is_dir():
            continue
        generate_css(family_dir)


if __name__ == "__main__":
    main()
