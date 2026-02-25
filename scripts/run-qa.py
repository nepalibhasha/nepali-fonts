"""Run basic font QA checks on fonts/sources and copy passing files."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

# Make local package import work when run from repository root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "packages/font-tools/src"))

from nepali_font_tools.qa import Severity, check_font

SOURCES = Path("fonts/sources")
PROCESSED = Path("fonts/processed")


def main() -> int:
    if not SOURCES.exists():
        print("fonts/sources/ not found. Nothing to QA.")
        return 1

    PROCESSED.mkdir(parents=True, exist_ok=True)
    any_failures = False
    checked_fonts = 0

    for family_dir in sorted(SOURCES.iterdir()):
        if not family_dir.is_dir():
            continue

        family_fonts = sorted(family_dir.glob("*.ttf")) + sorted(family_dir.glob("*.otf"))
        if not family_fonts:
            continue

        print(f"\n== {family_dir.name} ==")
        family_pass = True
        for font_path in family_fonts:
            checked_fonts += 1
            results = check_font(font_path)
            for result in results:
                icon = {Severity.PASS: "✓", Severity.WARN: "!", Severity.FAIL: "x"}[result.severity]
                print(f"  {icon} {font_path.name} [{result.check_id}] {result.message}")
                if result.severity == Severity.FAIL:
                    family_pass = False
                    any_failures = True

        if family_pass:
            dst = PROCESSED / family_dir.name
            if dst.exists():
                shutil.rmtree(dst)
            dst.mkdir(parents=True, exist_ok=True)
            for font_path in family_fonts:
                shutil.copy2(font_path, dst / font_path.name)
            print(f"  -> copied {len(family_fonts)} files to {dst}")
        else:
            print("  -> not copied due to failures")

    print(f"\nChecked {checked_fonts} fonts.")
    return 1 if any_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
