"""Integration tests for PDF rescue with real PDF files.

Creates synthetic PDFs with legacy font names (Preeti, Kantipur, etc.)
and verifies that rescue_pdf correctly detects and converts the text.
"""

from pathlib import Path

import pytest

fitz = pytest.importorskip("fitz", reason="PyMuPDF not installed")

from nepali_converter.pdf import rescue_pdf


def _escape_pdf_string(s):
    """Escape special characters for a PDF string literal."""
    return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _build_test_pdf(entries):
    """Create minimal valid PDF bytes with custom-named fonts.

    Args:
        entries: List of (font_name, text) tuples. Each becomes a text
                 span attributed to the given font name.

    Returns:
        Raw PDF bytes.
    """
    # Content stream: one text block per entry
    lines = []
    for i, (_, text) in enumerate(entries):
        escaped = _escape_pdf_string(text)
        y = 720 - i * 20
        lines.append(f"BT /F{i} 12 Tf 72 {y} Td ({escaped}) Tj ET")
    stream = "\n".join(lines)

    # Font resource dict
    font_dict = " ".join(f"/F{i} {5 + i} 0 R" for i in range(len(entries)))

    # PDF objects (1-indexed)
    objs = [
        "1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n",
        "2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n",
        (
            f"3 0 obj\n<< /Type /Page /Parent 2 0 R"
            f" /MediaBox [0 0 612 792]"
            f" /Contents 4 0 R"
            f" /Resources << /Font << {font_dict} >> >> >>\nendobj\n"
        ),
        f"4 0 obj\n<< /Length {len(stream)} >>\nstream\n{stream}\nendstream\nendobj\n",
    ]
    for i, (font_name, _) in enumerate(entries):
        objs.append(
            f"{5 + i} 0 obj\n<< /Type /Font /Subtype /Type1"
            f" /BaseFont /{font_name} >>\nendobj\n"
        )

    # Assemble: header + objects + xref + trailer
    body = "%PDF-1.4\n"
    offsets = []
    for obj in objs:
        offsets.append(len(body))
        body += obj

    xref_pos = len(body)
    body += "xref\n"
    body += f"0 {len(objs) + 1}\n"
    body += "0000000000 65535 f \n"
    for off in offsets:
        body += f"{off:010d} 00000 n \n"
    body += "trailer\n"
    body += f"<< /Size {len(objs) + 1} /Root 1 0 R >>\n"
    body += "startxref\n"
    body += f"{xref_pos}\n"
    body += "%%EOF\n"

    return body.encode("latin-1")


def _build_multipage_pdf(pages):
    """Create a multi-page PDF.

    Args:
        pages: List of lists of (font_name, text) tuples, one list per page.

    Returns:
        Raw PDF bytes.
    """
    # First pass: compute page object numbers so Kids array is correct.
    # Each page uses: 1 page obj + 1 content stream obj + N font objs.
    next_num = 3
    page_obj_nums = []
    for page_entries in pages:
        page_obj_nums.append(next_num)
        next_num += 2 + len(page_entries)

    page_refs = " ".join(f"{n} 0 R" for n in page_obj_nums)

    objs = [
        "1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n",
        f"2 0 obj\n<< /Type /Pages /Kids [{page_refs}] /Count {len(pages)} >>\nendobj\n",
    ]

    # Second pass: build the actual objects
    next_obj = 3

    for page_entries in pages:
        page_obj_num = next_obj
        content_obj_num = next_obj + 1
        font_start = next_obj + 2

        # Content stream
        lines = []
        for i, (_, text) in enumerate(page_entries):
            escaped = _escape_pdf_string(text)
            y = 720 - i * 20
            lines.append(f"BT /F{i} 12 Tf 72 {y} Td ({escaped}) Tj ET")
        stream = "\n".join(lines)

        # Font dict
        font_dict = " ".join(
            f"/F{i} {font_start + i} 0 R" for i in range(len(page_entries))
        )

        # Page object
        objs.append(
            f"{page_obj_num} 0 obj\n<< /Type /Page /Parent 2 0 R"
            f" /MediaBox [0 0 612 792]"
            f" /Contents {content_obj_num} 0 R"
            f" /Resources << /Font << {font_dict} >> >> >>\nendobj\n"
        )

        # Content stream object
        objs.append(
            f"{content_obj_num} 0 obj\n<< /Length {len(stream)} >>\n"
            f"stream\n{stream}\nendstream\nendobj\n"
        )

        # Font objects
        for i, (font_name, _) in enumerate(page_entries):
            objs.append(
                f"{font_start + i} 0 obj\n<< /Type /Font /Subtype /Type1"
                f" /BaseFont /{font_name} >>\nendobj\n"
            )

        next_obj = font_start + len(page_entries)

    # Assemble
    body = "%PDF-1.4\n"
    offsets = []
    for obj in objs:
        offsets.append(len(body))
        body += obj

    xref_pos = len(body)
    body += "xref\n"
    body += f"0 {len(objs) + 1}\n"
    body += "0000000000 65535 f \n"
    for off in offsets:
        body += f"{off:010d} 00000 n \n"
    body += "trailer\n"
    body += f"<< /Size {len(objs) + 1} /Root 1 0 R >>\n"
    body += "startxref\n"
    body += f"{xref_pos}\n"
    body += "%%EOF\n"

    return body.encode("latin-1")


# --- Fixtures ---


@pytest.fixture
def preeti_pdf(tmp_path):
    """Single-page PDF with Preeti-encoded text."""
    path = tmp_path / "preeti.pdf"
    path.write_bytes(_build_test_pdf([("Preeti", "g]kfn")]))
    return path


@pytest.fixture
def mixed_font_pdf(tmp_path):
    """Single-page PDF with both legacy (Preeti) and standard (Helvetica) text."""
    path = tmp_path / "mixed.pdf"
    path.write_bytes(
        _build_test_pdf([
            ("Preeti", "g]kfn"),
            ("Helvetica", "Hello"),
        ])
    )
    return path


@pytest.fixture
def multipage_pdf(tmp_path):
    """Three-page PDF with legacy text on each page."""
    path = tmp_path / "multipage.pdf"
    path.write_bytes(
        _build_multipage_pdf([
            [("Preeti", "g]kfn")],       # page 1: नेपाल
            [("Preeti", "gd:t]")],        # page 2: नमस्ते
            [("Preeti", "lxdfn")],        # page 3: हिमाल
        ])
    )
    return path


# --- Tests using generated PDFs ---


def test_rescue_preeti_pdf(preeti_pdf):
    """Rescue converts Preeti text to Unicode."""
    result = rescue_pdf(str(preeti_pdf))
    assert "नेपाल" in result


def test_rescue_mixed_font_pdf(mixed_font_pdf):
    """Legacy text is converted, non-legacy text passes through."""
    result = rescue_pdf(str(mixed_font_pdf))
    assert "नेपाल" in result
    assert "Hello" in result


def test_rescue_writes_output_file(preeti_pdf, tmp_path):
    """Output is written to a file when output_path is given."""
    out = tmp_path / "output.txt"
    result = rescue_pdf(str(preeti_pdf), output_path=str(out))
    assert "नेपाल" in result
    assert out.exists()
    assert "नेपाल" in out.read_text(encoding="utf-8")


def test_rescue_multipage_all_pages(multipage_pdf):
    """All pages are processed by default."""
    result = rescue_pdf(str(multipage_pdf))
    assert "नेपाल" in result
    assert "नमस्ते" in result
    assert "हिमाल" in result


def test_rescue_multipage_page_range(multipage_pdf):
    """Page range limits which pages are processed."""
    result = rescue_pdf(str(multipage_pdf), pages=(1, 2))
    assert "नेपाल" in result
    assert "नमस्ते" in result
    assert "हिमाल" not in result


def test_rescue_multipage_single_page(multipage_pdf):
    """Single-page range works."""
    result = rescue_pdf(str(multipage_pdf), pages=(2, 2))
    assert "नेपाल" not in result
    assert "नमस्ते" in result
    assert "हिमाल" not in result


# --- Tests using committed fixture files ---

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_fixture_preeti_sample():
    """Rescue preeti_sample.pdf and validate against snapshot."""
    result = rescue_pdf(str(FIXTURES_DIR / "preeti_sample.pdf"))
    expected = (FIXTURES_DIR / "preeti_sample_rescued.txt").read_text(encoding="utf-8")
    assert result == expected


def test_fixture_multipage_sample():
    """Rescue multipage_sample.pdf and validate against snapshot."""
    result = rescue_pdf(str(FIXTURES_DIR / "multipage_sample.pdf"))
    expected = (FIXTURES_DIR / "multipage_sample_rescued.txt").read_text(encoding="utf-8")
    assert result == expected
