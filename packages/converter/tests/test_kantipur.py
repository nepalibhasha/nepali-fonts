"""Tests for Kantipur font conversion."""

import pytest

from nepali_converter.converter import convert

KANTIPUR_VECTORS = [
    # Basic words (shared lowercase mappings)
    ("g]kfn", "नेपाल"),
    ("g]kfnL", "नेपाली"),
    ("rGb", "चन्द"),
    ("lxdfn", "हिमाल"),
    ("gd:t]", "नमस्ते"),
    (";/sf/", "सरकार"),
    ("ljBfno", "विद्यालय"),
    # Digits (same row as Preeti: symbols → Nepali digits)
    ("!@#$%^&*()", "१२३४५६७८९०"),
    # Punctuation
    (".", "।"),
    (",", ","),
    # Post-rules: reph
    ("ug{", "गर्न"),
    ("ug{]", "गर्ने"),
    # Post-rules: m-modifier
    ("eQm", "भक्त"),
    ("em/gf", "झरना"),
    # Kantipur-specific: F → ा (Preeti/Sagarmatha F → ँ)
    ("sFd", "काम"),
    ("gFd", "नाम"),
    # Compound vowels
    ("cf]vtL", "ओखती"),
    ("P]gf", "ऐना"),
    # Kantipur chandrabindu via \u201c
    ("hfp\u201cm", "जाऊँ"),
]


@pytest.mark.parametrize("input_text,expected", KANTIPUR_VECTORS)
def test_kantipur_conversion(input_text, expected):
    assert convert(input_text, "kantipur") == expected


def test_kantipur_F_differs_from_preeti():
    """Kantipur F → ा, while Preeti F → ँ."""
    assert convert("F", "kantipur") == "ा"
    assert convert("F", "preeti") == "ँ"


def test_kantipur_digits_same_as_preeti():
    """Kantipur digit keys 1-9,0 map to conjuncts (same as Preeti)."""
    assert convert("1", "kantipur") == "ज्ञ"
    assert convert("3", "kantipur") == "घ"


def test_kantipur_extended_chars():
    """Kantipur-specific extended character mappings."""
    assert convert("\u2122", "kantipur") == "र"
    assert convert("\u00ba", "kantipur") == "फ्"
    assert convert("\u00f8", "kantipur") == "य्"
