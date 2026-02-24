"""Core conversion engine.

Three-phase pipeline: character-map -> post-rules -> output.
Post-rules are shared across all legacy fonts — only the character maps differ.

References:
- https://github.com/Shuvayatra/preeti (JS implementation)
- https://github.com/casualsnek/npttf2utf (Python implementation)
"""

import re

from nepali_converter.maps import FONT_MAPS, SUPPORTED_FONTS

# 32 ordered post-rules (regex pattern, replacement).
# These are identical across all legacy fonts.
# Order is critical — do not reorder.
POST_RULES: list[tuple[str, str]] = [
    (r"्ा", ""),                                        # 1: halanta+aa = invalid, delete
    (r"(त्र|त्त)([^उभप]+?)m", r"\1m\2"),                # 2: move m past non-उभप after त्र/त्त
    (r"त्रm", "क्र"),                                    # 3: त्र+m = क्र
    (r"त्तm", "क्त"),                                    # 4: त्त+m = क्त
    (r"([^उभप]+?)m", r"m\1"),                            # 5: move m before other chars
    (r"उm", "ऊ"),                                        # 6: उ+m = ऊ
    (r"भm", "झ"),                                        # 7: भ+m = झ
    (r"पm", "फ"),                                        # 8: प+m = फ
    (r"इ\{", "ई"),                                       # 9: इ+{ = ई
    (r"ि((.्)*[^्])", r"\1ि"),                           # 10: i-matra reorder (move after consonant cluster)
    (r"(.[ािीुूृेैोौंःँ]*?)\{", r"{\1"),                  # 11: move { before char+matras
    (r"((.्)*)\{", r"{\1"),                               # 12: move { before halanta clusters
    (r"\{", "र्"),                                        # 13: remaining { = reph
    (r"([ाीुूृेैोौंःँ]+?)(्(.्)*[^्])", r"\2\1"),        # 14: matras after halanta-consonant cluster
    (r"्([ाीुूृेैोौंःँ]+?)((.्)*[^्])", r"्\2\1"),       # 15: matras after halanta+consonant
    (r"([ंँ])([ािीुूृेैोौः]*)", r"\2\1"),                 # 16: anusvara/chandrabindu after vowel signs
    (r"ँँ", "ँ"),                                         # 17: dedup chandrabindu
    (r"ंं", "ं"),                                         # 18: dedup anusvara
    (r"ेे", "े"),                                         # 19: dedup e-matra
    (r"ैै", "ै"),                                         # 20: dedup ai-matra
    (r"ुु", "ु"),                                         # 21: dedup u-matra
    (r"ूू", "ू"),                                         # 22: dedup uu-matra
    (r"^ः", ":"),                                         # 23: visarga at line start = colon
    (r"टृ", "ट्ट"),                                       # 24: fix ट+ृ -> ट्ट
    (r"ेा", "ाे"),                                        # 25: swap wrongly-ordered e+aa
    (r"ैा", "ाै"),                                        # 26: swap wrongly-ordered ai+aa
    # Compound vowel composition — ORDER MATTERS:
    # Must compose अाे->ओ BEFORE ाे->ो, else अो instead of ओ
    (r"अाे", "ओ"),                                        # 27
    (r"अाै", "औ"),                                        # 28
    (r"अा", "आ"),                                         # 29
    (r"एे", "ऐ"),                                         # 30
    (r"ाे", "ो"),                                         # 31
    (r"ाै", "ौ"),                                         # 32
]

_COMPILED_POST_RULES = [(re.compile(p), r) for p, r in POST_RULES]


def convert(text: str, source_font: str) -> str:
    """Convert legacy-encoded Nepali text to Unicode.

    Args:
        text: Input text in legacy encoding.
        source_font: One of "preeti", "kantipur", "sagarmatha", "himalb".

    Returns:
        Unicode Nepali text.

    Raises:
        ValueError: If source_font is not recognized.
    """
    font_key = source_font.lower()
    if font_key not in FONT_MAPS:
        raise ValueError(
            f"Unknown font: {source_font!r}. "
            f"Supported: {', '.join(SUPPORTED_FONTS)}"
        )
    char_map = FONT_MAPS[font_key]

    # Process word by word (whitespace preserved)
    result = []
    for token in re.split(r"(\s+)", text):
        if not token or token.isspace():
            result.append(token)
            continue

        # Phase 1: Character map substitution
        mapped = "".join(char_map.get(ch, ch) for ch in token)

        # Phase 2: Post-rules (shared across all fonts)
        for pattern, replacement in _COMPILED_POST_RULES:
            mapped = pattern.sub(replacement, mapped)

        result.append(mapped)

    return "".join(result)
