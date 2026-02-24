"""CLI entry point: nepali-convert"""

import argparse
import sys

from nepali_converter.converter import convert
from nepali_converter.detector import detect_font
from nepali_converter.maps import SUPPORTED_FONTS
from nepali_converter.pdf import rescue_pdf


def _parse_pages(value: str) -> tuple[int, int]:
    """Parse page range in the form 'start-end' (1-based, inclusive)."""
    try:
        start_s, end_s = value.split("-", 1)
        start = int(start_s)
        end = int(end_s)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"Invalid page range {value!r}. Use format start-end (e.g. 1-5)."
        ) from exc

    if start <= 0 or end <= 0:
        raise argparse.ArgumentTypeError("Page numbers must be >= 1.")
    if start > end:
        raise argparse.ArgumentTypeError("Page range start must be <= end.")
    return (start, end)


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
    parser.add_argument(
        "--pdf",
        action="store_true",
        help="Treat input as PDF and run legacy-text rescue (non-OCR).",
    )
    parser.add_argument(
        "--pages",
        type=_parse_pages,
        help="Page range for PDF mode (1-based, inclusive), e.g. 1-5.",
    )
    args = parser.parse_args()

    if args.pages and not args.pdf:
        parser.error("--pages can only be used with --pdf.")

    if args.pdf:
        result = rescue_pdf(args.input, output_path=args.output, pages=args.pages)
        if not args.output:
            sys.stdout.write(result)
        return

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
