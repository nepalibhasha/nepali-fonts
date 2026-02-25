"""Basic QA checks for Devanagari fonts."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from fontTools.ttLib import TTFont


class Severity(Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"


@dataclass
class CheckResult:
    check_id: str
    severity: Severity
    message: str


# Basic coverage for v1 checks.
REQUIRED_CODEPOINTS: list[int] = [
    # Consonants
    0x0915, 0x0916, 0x0917, 0x0918, 0x0919,
    0x091A, 0x091B, 0x091C, 0x091D, 0x091E,
    0x091F, 0x0920, 0x0921, 0x0922, 0x0923,
    0x0924, 0x0925, 0x0926, 0x0927, 0x0928,
    0x092A, 0x092B, 0x092C, 0x092D, 0x092E,
    0x092F, 0x0930, 0x0932, 0x0935, 0x0936, 0x0937, 0x0938, 0x0939,
    # Matras and signs
    0x093E, 0x093F, 0x0940, 0x0941, 0x0942, 0x0943, 0x0947, 0x0948, 0x094B, 0x094C,
    0x0901, 0x0902, 0x0903, 0x094D,
    # Digits
    0x0966, 0x0967, 0x0968, 0x0969, 0x096A, 0x096B, 0x096C, 0x096D, 0x096E, 0x096F,
]


def _script_tags(table) -> list[str]:
    return [rec.ScriptTag for rec in table.ScriptList.ScriptRecord]


def _has_nepali_langsys(table) -> bool:
    for script_record in table.ScriptList.ScriptRecord:
        if script_record.ScriptTag not in ("dev2", "deva"):
            continue
        for lang_record in script_record.Script.LangSysRecord:
            if lang_record.LangSysTag.strip() in ("NEP", "nep"):
                return True
    return False


def check_font(path: str | Path) -> list[CheckResult]:
    """Run v1 basic checks on a font file."""
    results: list[CheckResult] = []
    path = Path(path)

    try:
        font = TTFont(str(path))
    except Exception as exc:  # pragma: no cover - exact exception type varies
        return [CheckResult("valid-font", Severity.FAIL, f"Cannot load font: {exc}")]

    results.append(CheckResult("valid-font", Severity.PASS, "Font loads successfully"))

    cmap = font.getBestCmap() or {}
    missing = [cp for cp in REQUIRED_CODEPOINTS if cp not in cmap]
    if missing:
        preview = ", ".join(hex(cp) for cp in missing[:5])
        results.append(
            CheckResult(
                "devanagari-coverage",
                Severity.FAIL,
                f"Missing {len(missing)} required codepoints (examples: {preview})",
            )
        )
    else:
        results.append(
            CheckResult("devanagari-coverage", Severity.PASS, "Required codepoints present")
        )

    if "GSUB" not in font:
        results.append(CheckResult("gsub-devanagari", Severity.FAIL, "No GSUB table"))
    else:
        scripts = _script_tags(font["GSUB"].table)
        if "dev2" in scripts or "deva" in scripts:
            results.append(
                CheckResult("gsub-devanagari", Severity.PASS, "GSUB contains Devanagari script")
            )
        else:
            results.append(
                CheckResult(
                    "gsub-devanagari",
                    Severity.WARN,
                    f"GSUB found but no dev2/deva script tags: {scripts}",
                )
            )

    has_nepali = False
    for table_name in ("GSUB", "GPOS"):
        if table_name in font and _has_nepali_langsys(font[table_name].table):
            has_nepali = True
            break
    if has_nepali:
        results.append(CheckResult("nepali-lang-tag", Severity.PASS, "NEP/nep language tag found"))
    else:
        results.append(
            CheckResult(
                "nepali-lang-tag",
                Severity.WARN,
                "No NEP/nep language tag in GSUB/GPOS (locl may not localize Nepali forms)",
            )
        )

    return results
