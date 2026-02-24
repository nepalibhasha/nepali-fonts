"""General converter tests across all fonts."""

import pytest

from nepali_converter.converter import convert
from nepali_converter.maps import SUPPORTED_FONTS


def test_unknown_font_raises():
    with pytest.raises(ValueError, match="Unknown font"):
        convert("hello", "comic_sans")


@pytest.mark.parametrize("font", SUPPORTED_FONTS)
def test_empty_string_all_fonts(font):
    assert convert("", font) == ""


@pytest.mark.parametrize("font", SUPPORTED_FONTS)
def test_whitespace_only_all_fonts(font):
    assert convert("   ", font) == "   "


@pytest.mark.parametrize("font", SUPPORTED_FONTS)
def test_case_insensitive_font_name(font):
    # Should work with any casing
    convert("test", font.upper())
    convert("test", font.title())
