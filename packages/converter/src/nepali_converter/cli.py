"""CLI entry point: nepali-convert"""

import argparse
import sys

from nepali_converter.converter import convert
from nepali_converter.detector import detect_font
from nepali_converter.maps import SUPPORTED_FONTS


def main():
    parser = argparse.ArgumentParser(
        description="Convert legacy Nepali font text to Unicode"
    )
    parser.add_argument("input", help="Input file path, or - for stdin")
    parser.add_argument(
        "--font",
        default="auto",
        choices=["auto"] + SUPPORTED_FONTS,
        help="Source font (default: auto-detect)",
    )
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    parser.add_argument(
        "--encoding",
        default="cp1252",
        help="Input file encoding (default: cp1252 for legacy fonts)",
    )
    args = parser.parse_args()

    # Read input — legacy files are typically Windows-1252 encoded
    if args.input == "-":
        text = sys.stdin.read()
    else:
        with open(args.input, encoding=args.encoding) as f:
            text = f.read()

    # Detect font if needed
    font = args.font
    if font == "auto":
        font = detect_font(text)
        if font is None:
            print(
                "Could not detect legacy font. Use --font to specify.",
                file=sys.stderr,
            )
            sys.exit(1)

    # Convert
    result = convert(text, font)

    # Write output
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
    else:
        sys.stdout.write(result)
