"""Tests for Preeti font conversion.

Test vectors sourced from:
- https://github.com/Shuvayatra/preeti (preeti.vector.json)
"""

import pytest

from nepali_converter.converter import convert

# (preeti_input, expected_unicode) pairs from Shuvayatra/preeti test vectors
PREETI_VECTORS = [
    ("g]kfn", "नेपाल"),
    ("g]kfnL", "नेपाली"),
    ("rGb", "चन्द"),
    ("lxdfn", "हिमाल"),
    ("/fli6«o", "राष्ट्रिय"),
    ("ljz]if0f", "विशेषण"),
    ("u0f]z", "गणेश"),
    ("kfl0f", "पाणि"),
    ("ug{", "गर्न"),
    ("ug{]", "गर्ने"),
    ("ug]{", "गर्ने"),
    ("lgdfrf]{s", "निमार्चोक"),
    ("rGb|f]bo", "चन्द्रोदय"),
    ("O{Zj/", "ईश्वर"),
    ("k|mfO{", "फ्राई"),
    (":ofk|m'a]zL", "स्याफ्रुबेशी"),
    ("cfkm\\gf]", "आफ्नो"),
    ("cfk\\mgf}", "आफ्नौ"),
    ("eQm", "भक्त"),
    ("em/gf", "झरना"),
    ("s|'/", "क्रुर"),
    ("qm'/", "क्रुर"),
    ("q'm/", "क्रुर"),
    ("k|ltlqmof", "प्रतिक्रिया"),
    ("hfpm", "जाऊ"),
    ("hfpFm", "जाऊँ"),
    ("e]mNg'", "झेल्नु"),
    ("em]Ng'", "झेल्नु"),
    ("emfs|L", "झाक्री"),
    ("kf}jf", "पौवा"),
    ("If]qkf6L", "क्षेत्रपाटी"),
    ("iff]8zL", "षोडशी"),
    ("cf]vtL", "ओखती"),
    ("P]gf", "ऐना"),
    ("hfcf}+", "जाऔं"),
    ("hfcf+}", "जाऔं"),
    ("3/d+}", "घरमैं"),
    ("-s_", "(क)"),
    ("!@#$%^&*()", "१२३४५६७८९०"),
    ("k\u00a5of]", "पर्\u200dयो"),
    ("x]Yof{]", "हेर्थ्यो"),
    ("x]Yof]{", "हेर्थ्यो"),
    ("d2t", "मद्दत"),
    ("Clif", "ऋषि"),
    ("6]\u00abS;", "ट्रेक्स"),
    ("k|:'tt", "प्रस्तुत"),
    ("ad]flhd", "बमोजिम"),
    ("a]d}f;dL", "बेमौसमी"),
]


@pytest.mark.parametrize("input_text,expected", PREETI_VECTORS)
def test_preeti_conversion(input_text, expected):
    assert convert(input_text, "preeti") == expected


def test_unmapped_chars_passthrough():
    # Characters not in Preeti's char-map pass through unchanged.
    # Note: most ASCII letters ARE in the char-map (they map to Devanagari),
    # so "English passthrough" is the detector's job, not the converter's.
    # Test with chars that have no mapping.
    assert convert("\n", "preeti") == "\n"
    assert convert("\t", "preeti") == "\t"


def test_empty_string():
    assert convert("", "preeti") == ""


def test_whitespace_preserved():
    result = convert("g]kfn  g]kfnL", "preeti")
    assert result == "नेपाल  नेपाली"


def test_digits_to_nepali():
    assert convert("!@#$%^&*()", "preeti") == "१२३४५६७८९०"


def test_punctuation():
    assert convert(".", "preeti") == "।"
    assert convert(",", "preeti") == ","
