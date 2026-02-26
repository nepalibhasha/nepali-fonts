"""Tests for Himalb (Fontasy Himali TT) font conversion."""

import pytest

from nepali_converter.converter import convert

HIMALB_VECTORS = [
    # Basic words (shared lowercase mappings)
    ("g]kfn", "नेपाल"),
    ("g]kfnL", "नेपाली"),
    ("rGb", "चन्द"),
    ("lxdfn", "हिमाल"),
    ("gd:t]", "नमस्ते"),
    (";/sf/", "सरकार"),
    ("ljBfno", "विद्यालय"),
    # Himalb-specific: digit keys map directly to Nepali digits
    ("1234567890", "१२३४५६७८९०"),
    # Himalb-specific: symbol row maps to conjuncts (not digits!)
    ("^&*(", "टठडढ"),
    ("%", "छ"),
    # Punctuation
    (".", "।"),
    (",", ","),
    # Post-rules: reph, m-modifier
    ("ug{", "गर्न"),
    ("ug{]", "गर्ने"),
    ("eQm", "भक्त"),
    ("em/gf", "झरना"),
    # Himalb ~ → ञ (other fonts: ञ्)
    ("~", "ञ"),
    # Himalb ` → ञ् (other fonts: ञ)
    ("`", "ञ्"),
    # Himalb F → ा (same as Kantipur)
    ("sFd", "काम"),
    ("gFd", "नाम"),
    # Himalb chandrabindu via ¤ (\u00a4)
    ("hfp\u00a4m", "जाऊँ"),
    # Compound vowels
    ("cf]vtL", "ओखती"),
    ("P]gf", "ऐना"),
]


@pytest.mark.parametrize("input_text,expected", HIMALB_VECTORS)
def test_himalb_conversion(input_text, expected):
    assert convert(input_text, "himalb") == expected


def test_himalb_digits_differ_from_preeti():
    """Himalb digit keys map directly to Nepali digits (unlike Preeti)."""
    assert convert("1", "himalb") == "१"
    assert convert("9", "himalb") == "९"
    assert convert("0", "himalb") == "०"
    # Preeti digits map to conjuncts instead
    assert convert("1", "preeti") == "ज्ञ"


def test_himalb_symbols_to_conjuncts():
    """Himalb symbol row maps to conjuncts (not digits like Preeti)."""
    assert convert("!", "himalb") == "ज्ञ"
    assert convert("@", "himalb") == "द्द"
    assert convert("#", "himalb") == "घ"
    assert convert("$", "himalb") == "द्ध"
    # Preeti symbols map to digits instead
    assert convert("!", "preeti") == "१"


def test_himalb_tilde_backtick_swapped():
    """Himalb swaps ~ and ` compared to other fonts."""
    assert convert("~", "himalb") == "ञ"
    assert convert("`", "himalb") == "ञ्"
    # Other fonts are opposite
    assert convert("~", "preeti") == "ञ्"
    assert convert("`", "preeti") == "ञ"


def test_himalb_extended_chars():
    """Himalb-specific extended character mappings."""
    assert convert("\u00a4", "himalb") == "ँ"
    assert convert("\u00e9", "himalb") == "ङ्ग"
    assert convert("\u00d1", "himalb") == "ङ"
    assert convert("\u00ed", "himalb") == "ष"
