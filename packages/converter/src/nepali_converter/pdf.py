"""PDF text extraction and legacy font rescue.

Uses PyMuPDF (fitz) to extract text and embedded font metadata.
Non-OCR only — requires text layer to be present in the PDF.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import fitz  # PyMuPDF

from nepali_converter.converter import convert

if TYPE_CHECKING:
    from collections.abc import Iterable


# Known legacy font names as they appear in PDF metadata/spans.
KNOWN_LEGACY_FONTS: dict[str, str] = {
    "preeti": "preeti",
    "kantipur": "kantipur",
    "sagarmatha": "sagarmatha",
    "himalb": "himalb",
    "fontasy_himali_tt": "himalb",
    "fontasy himali tt": "himalb",
}


def _detect_legacy_font(font_name: str) -> str | None:
    normalized = font_name.lower().strip()
    for key, mapped in KNOWN_LEGACY_FONTS.items():
        if key in normalized:
            return mapped
    return None


def _iter_page_indices(
    total_pages: int, pages: tuple[int, int] | None
) -> Iterable[int]:
    if pages is None:
        return range(total_pages)

    start, end = pages
    start = max(1, start)
    end = min(total_pages, end)
    if start > end:
        return range(0)
    # Convert to 0-based, inclusive end.
    return range(start - 1, end)


def rescue_pdf(
    path: str,
    output_path: str | None = None,
    pages: tuple[int, int] | None = None,
) -> str:
    """Extract and convert legacy-encoded text from a PDF.

    Reads embedded span font names to detect known legacy encodings and applies
    the matching converter. Non-legacy spans pass through unchanged.
    """
    doc = fitz.open(path)
    result_parts: list[str] = []

    try:
        for page_num in _iter_page_indices(len(doc), pages):
            page = doc[page_num]
            blocks = page.get_text("dict").get("blocks", [])

            for block in blocks:
                lines = block.get("lines")
                if not lines:
                    continue

                for line in lines:
                    for span in line.get("spans", []):
                        text = span.get("text", "")
                        font_name = span.get("font", "")

                        legacy_font = _detect_legacy_font(font_name)
                        if legacy_font and text:
                            text = convert(text, legacy_font)

                        result_parts.append(text)
                    result_parts.append("\n")
                result_parts.append("\n")
    finally:
        doc.close()

    output = "".join(result_parts)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(output)

    return output
