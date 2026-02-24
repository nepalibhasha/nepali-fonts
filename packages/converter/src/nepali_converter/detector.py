"""Auto-detect which legacy font was used to encode text.

Uses character frequency analysis against known per-font profiles.
Returns None for standard Unicode Devanagari or English text.
"""

from nepali_converter.maps import FONT_MAPS

# Characters that uniquely identify specific fonts.
# Built from the differences in character maps across fonts.
_FONT_SIGNATURES: dict[str, set[str]] = {
    # Preeti: F=ँ (chandrabindu), X=ह्, digits map to conjuncts
    "preeti": {"\u02c6", "\u203a", "\u00cb", "\u00cc", "\u00cd", "\u00ce"},
    # Kantipur: F=ा (aa-matra), X=हृ, has ™ ® Â µ mapping to र
    "kantipur": {"\u2122", "\u00c2", "\u00b5", "\u00ba", "\u00cf", "\u00f8"},
    # Sagarmatha: has ƒ Š ‡ · ¸ Ç É Þ è unique chars
    "sagarmatha": {"\u0192", "\u0160", "\u2021", "\u00b7", "\u00b8",
                   "\u00c7", "\u00c9", "\u00de", "\u00e8"},
    # Himalb: has Ñ é í ú unique chars
    "himalb": {"\u00d1", "\u00e9", "\u00ed", "\u00fa"},
}

# Bracket/matra characters that are strong indicators of legacy encoding.
# These appear frequently in legacy text but rarely in normal English.
_LEGACY_SPECIAL = set("{}[]|\\")


def _is_devanagari(text: str) -> bool:
    """Check if text contains Devanagari Unicode characters."""
    for ch in text:
        if "\u0900" <= ch <= "\u097f" or "\ua8e0" <= ch <= "\ua8ff":
            return True
    return False


def _has_non_ascii_legacy(text: str) -> bool:
    """Check if text contains non-ASCII characters used by legacy fonts."""
    for ch in text:
        code = ord(ch)
        if 0x80 <= code <= 0xFF or code in (
            0x0152, 0x0153, 0x0160, 0x0192, 0x02C6, 0x02DC,
            0x2018, 0x2019, 0x201A, 0x201C, 0x201D, 0x201E,
            0x2020, 0x2021, 0x2022, 0x2026, 0x2030, 0x2039,
            0x203A, 0x2122,
        ):
            return True
    return False


def detect_font(text: str) -> str | None:
    """Detect which legacy font was used to encode the text.

    Args:
        text: Input text to analyze.

    Returns:
        Font name ("preeti", "kantipur", "sagarmatha", "himalb")
        or None if text appears to be standard Unicode or English.
    """
    if not text or not text.strip():
        return None

    # If text already contains Devanagari Unicode, it's not legacy-encoded
    if _is_devanagari(text):
        return None

    text_chars = set(text)

    # Score each font by how many of its signature characters appear
    scores: dict[str, int] = {}
    for font_name, signatures in _FONT_SIGNATURES.items():
        scores[font_name] = len(text_chars & signatures)

    # If any font has unique signature matches, prefer it
    max_score = max(scores.values()) if scores else 0
    if max_score > 0:
        best = max(scores, key=lambda k: scores[k])
        return best

    # No signature chars found. Look for structural evidence of legacy encoding:
    # 1. Non-ASCII chars in the Windows-1252 / Mac Roman range (legacy fonts use these)
    # 2. High frequency of bracket/pipe chars used as matras in legacy encoding

    if _has_non_ascii_legacy(text):
        return "preeti"  # default to most common legacy font

    # Check for legacy special characters (brackets, pipes used as matras)
    special_count = sum(1 for ch in text if ch in _LEGACY_SPECIAL)
    non_space = sum(1 for ch in text if not ch.isspace())

    if non_space > 0 and special_count / non_space > 0.05:
        return "preeti"

    # No strong evidence of legacy encoding
    return None
