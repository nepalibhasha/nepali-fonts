"""Tests for Sagarmatha font conversion."""

import pytest

from nepali_converter.converter import convert

SAGARMATHA_VECTORS = [
    # Basic words (shared lowercase mappings)
    ("g]kfn", "नेपाल"),
    ("g]kfnL", "नेपाली"),
    ("rGb", "चन्द"),
    ("lxdfn", "हिमाल"),
    ("gd:t]", "नमस्ते"),
    (";/sf/", "सरकार"),
    ("ljBfno", "विद्यालय"),
    # Digits (same as Preeti)
    ("!@#$%^&*()", "१२३४५६७८९०"),
    # Punctuation
    (".", "।"),
    (",", ","),
    # Post-rules: reph, m-modifier
    ("ug{", "गर्न"),
    ("ug{]", "गर्ने"),
    ("eQm", "भक्त"),
    ("em/gf", "झरना"),
    # Sagarmatha F → ँ (same as Preeti, unlike Kantipur)
    ("hfpFm", "जाऊँ"),
    # Compound vowels
    ("cf]vtL", "ओखती"),
    ("P]gf", "ऐना"),
    # Sagarmatha-specific: ƒ (\u0192) → द्र
    ("rG\u0192", "चन्द्र"),
    # Sagarmatha-specific: Š (\u0160) → र्
    ("w\u0160d", "धर्म"),
    # Sagarmatha-specific: ‡ (\u2021) → े (alternative e-matra)
    ("g\u2021kfn", "नेपाल"),
]


@pytest.mark.parametrize("input_text,expected", SAGARMATHA_VECTORS)
def test_sagarmatha_conversion(input_text, expected):
    assert convert(input_text, "sagarmatha") == expected


def test_sagarmatha_F_same_as_preeti():
    """Sagarmatha F → ँ (same as Preeti)."""
    assert convert("F", "sagarmatha") == "ँ"
    assert convert("F", "preeti") == "ँ"


def test_sagarmatha_extended_chars():
    """Sagarmatha-specific extended character mappings."""
    assert convert("\u0192", "sagarmatha") == "द्र"
    assert convert("\u0160", "sagarmatha") == "र्"
    assert convert("\u2021", "sagarmatha") == "े"
    assert convert("\u00b7", "sagarmatha") == "ङ्ग"
    assert convert("\u00b8", "sagarmatha") == "ड्ड"
    assert convert("\u00c7", "sagarmatha") == "फ्"
