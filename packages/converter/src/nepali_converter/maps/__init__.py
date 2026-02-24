"""Legacy font character mapping tables."""

from nepali_converter.maps import himalb, kantipur, preeti, sagarmatha

FONT_MAPS: dict[str, dict[str, str]] = {
    "preeti": preeti.CHARACTER_MAP,
    "kantipur": kantipur.CHARACTER_MAP,
    "sagarmatha": sagarmatha.CHARACTER_MAP,
    "himalb": himalb.CHARACTER_MAP,
}

SUPPORTED_FONTS = list(FONT_MAPS.keys())
