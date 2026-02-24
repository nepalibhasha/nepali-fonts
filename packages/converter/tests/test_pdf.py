"""Tests for PDF rescue flow."""

from __future__ import annotations

from pathlib import Path

from nepali_converter.pdf import rescue_pdf


class _FakePage:
    def __init__(self, spans: list[tuple[str, str]]):
        self._spans = spans

    def get_text(self, _mode: str):
        return {
            "blocks": [
                {
                    "lines": [
                        {
                            "spans": [
                                {"text": text, "font": font}
                                for text, font in self._spans
                            ]
                        }
                    ]
                }
            ]
        }


class _FakeDoc:
    def __init__(self, pages: list[_FakePage]):
        self._pages = pages

    def __len__(self):
        return len(self._pages)

    def __getitem__(self, idx: int):
        return self._pages[idx]

    def close(self):
        return None


def test_rescue_pdf_converts_legacy_spans(monkeypatch):
    doc = _FakeDoc(
        [
            _FakePage([("g]kfn", "Preeti"), (" Hello ", "Arial"), ("sf7df08\"", "Preeti")]),
        ]
    )

    monkeypatch.setattr("nepali_converter.pdf.fitz.open", lambda _path: doc)
    out = rescue_pdf("dummy.pdf")

    assert "नेपाल" in out
    assert "काठमाण्डू" in out
    assert " Hello " in out


def test_rescue_pdf_page_range(monkeypatch):
    doc = _FakeDoc(
        [
            _FakePage([("g]kfn", "Preeti")]),
            _FakePage([("sf7df08\"", "Preeti")]),
        ]
    )
    monkeypatch.setattr("nepali_converter.pdf.fitz.open", lambda _path: doc)

    out = rescue_pdf("dummy.pdf", pages=(2, 2))
    assert "काठमाण्डू" in out
    assert "नेपाल" not in out


def test_rescue_pdf_writes_output_file(monkeypatch, tmp_path: Path):
    doc = _FakeDoc([_FakePage([("g]kfn", "Preeti")])])
    monkeypatch.setattr("nepali_converter.pdf.fitz.open", lambda _path: doc)

    output_path = tmp_path / "rescued.txt"
    out = rescue_pdf("dummy.pdf", output_path=str(output_path))

    assert output_path.read_text(encoding="utf-8") == out
    assert "नेपाल" in out
