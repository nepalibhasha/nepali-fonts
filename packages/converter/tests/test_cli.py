"""Tests for the nepali-convert CLI."""

import subprocess
import sys
import textwrap
from pathlib import Path

import pytest


def run_cli(*args, input_text=None):
    """Run nepali-convert CLI and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        [sys.executable, "-m", "nepali_converter.cli", *args],
        input=input_text,
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr


# --- File input / output ---


def test_convert_file_to_stdout(tmp_path):
    """Convert a file and write to stdout."""
    infile = tmp_path / "input.txt"
    infile.write_text("g]kfn", encoding="utf-8")
    rc, stdout, stderr = run_cli(str(infile), "--font", "preeti", "--encoding", "utf-8")
    assert rc == 0
    assert stdout == "नेपाल"


def test_convert_file_to_output_file(tmp_path):
    """Convert a file and write to an output file."""
    infile = tmp_path / "input.txt"
    outfile = tmp_path / "output.txt"
    infile.write_text("g]kfn", encoding="utf-8")
    rc, stdout, stderr = run_cli(
        str(infile), "--font", "preeti", "--encoding", "utf-8", "-o", str(outfile)
    )
    assert rc == 0
    assert stdout == ""
    assert outfile.read_text(encoding="utf-8") == "नेपाल"


# --- Stdin ---


def test_convert_stdin(tmp_path):
    """Read from stdin when input is '-'."""
    rc, stdout, stderr = run_cli("-", "--font", "preeti", input_text="g]kfn")
    assert rc == 0
    assert stdout == "नेपाल"


# --- Font selection ---


def test_explicit_font():
    """Explicit --font flag works for each supported font."""
    rc, stdout, _ = run_cli("-", "--font", "kantipur", input_text="g]kfn")
    assert rc == 0
    assert stdout == "नेपाल"


def test_auto_detect_font():
    """Auto-detect works when input has signature chars."""
    # Preeti signature chars mixed with text
    preeti_text = "g]kfn \u02c6 \u203a"
    rc, stdout, _ = run_cli("-", "--font", "auto", input_text=preeti_text)
    assert rc == 0
    # Should detect as Preeti and convert
    assert "नेपाल" in stdout


def test_auto_detect_fails_for_plain_english():
    """Auto-detect exits with error for unrecognizable text."""
    rc, stdout, stderr = run_cli("-", input_text="hello world")
    assert rc == 1
    assert "Could not detect" in stderr


# --- Encoding ---


def test_cp1252_encoding(tmp_path):
    """Default cp1252 encoding reads legacy files correctly."""
    infile = tmp_path / "legacy.txt"
    # Write raw cp1252 bytes: "g]kfn" is pure ASCII so works in cp1252 too
    infile.write_bytes("g]kfn".encode("cp1252"))
    rc, stdout, _ = run_cli(str(infile), "--font", "preeti")
    assert rc == 0
    assert stdout == "नेपाल"


# --- Page range parsing ---


def test_pages_without_pdf_errors():
    """--pages without --pdf should error."""
    rc, _, stderr = run_cli("-", "--pages", "1-5", input_text="test")
    assert rc != 0
    assert "--pages can only be used with --pdf" in stderr


# --- PDF mode ---


def test_pdf_missing_pymupdf_message(monkeypatch, tmp_path):
    """PDF mode shows helpful error when PyMuPDF is not installed."""
    # We test this by running a subprocess that patches the import
    # Create a script that simulates the ImportError
    script = tmp_path / "test_pdf_import.py"
    script.write_text(textwrap.dedent("""\
        import sys
        import unittest.mock

        # Block fitz import to simulate missing PyMuPDF
        with unittest.mock.patch.dict(sys.modules, {"fitz": None}):
            # Also need to remove cached pdf module if present
            sys.modules.pop("nepali_converter.pdf", None)
            sys.argv = ["nepali-convert", "dummy.pdf", "--pdf"]
            from nepali_converter.cli import main
            main()
    """))
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "pip install nepali-converter[pdf]" in result.stderr


# --- Edge cases ---


def test_empty_file(tmp_path):
    """Empty input file produces empty output."""
    infile = tmp_path / "empty.txt"
    infile.write_text("", encoding="utf-8")
    rc, stdout, _ = run_cli(str(infile), "--font", "preeti", "--encoding", "utf-8")
    assert rc == 0
    assert stdout == ""


def test_multiline_input():
    """Multiline input is converted correctly."""
    text = "g]kfn\nlxdfn"
    rc, stdout, _ = run_cli("-", "--font", "preeti", input_text=text)
    assert rc == 0
    assert stdout == "नेपाल\nहिमाल"


def test_nonexistent_file():
    """Non-existent input file produces an error with the file path."""
    rc, _, stderr = run_cli("/nonexistent/file.txt", "--font", "preeti")
    assert rc != 0
    assert "No such file" in stderr or "/nonexistent/file.txt" in stderr
