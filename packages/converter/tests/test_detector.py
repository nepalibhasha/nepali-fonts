"""Tests for legacy font auto-detection."""

from nepali_converter.detector import detect_font


def test_unicode_nepali_returns_none():
    assert detect_font("नेपाल") is None


def test_english_returns_none():
    assert detect_font("Hello World") is None


def test_empty_returns_none():
    assert detect_font("") is None


def test_whitespace_returns_none():
    assert detect_font("   ") is None


def test_pure_numbers_returns_none():
    assert detect_font("12345") is None


def test_preeti_with_special_chars():
    # Typical Preeti: brackets/pipes used as matras
    result = detect_font("g]kfn sf7df08\"")
    assert result == "preeti"


def test_preeti_with_non_ascii():
    # Preeti extended chars (non-ASCII range)
    result = detect_font("6]\u00abS;")  # ट्रेक्स
    assert result == "preeti"


def test_sagarmatha_signature_chars():
    # Sagarmatha has unique chars like ƒ (U+0192) -> द्र
    result = detect_font("g]kfn \u0192")
    assert result == "sagarmatha"
