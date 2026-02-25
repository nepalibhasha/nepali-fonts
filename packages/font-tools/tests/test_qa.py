from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

from nepali_font_tools.qa import REQUIRED_CODEPOINTS, Severity, check_font


class _FakeLangRec:
    def __init__(self, tag: str):
        self.LangSysTag = tag


class _FakeScript:
    def __init__(self, lang_tags: list[str]):
        self.LangSysRecord = [_FakeLangRec(t) for t in lang_tags]


class _FakeScriptRec:
    def __init__(self, script_tag: str, lang_tags: list[str]):
        self.ScriptTag = script_tag
        self.Script = _FakeScript(lang_tags)


class _FakeScriptList:
    def __init__(self, recs: list[_FakeScriptRec]):
        self.ScriptRecord = recs


class _FakeTable:
    def __init__(self, script_tags: list[str], lang_tags: list[str]):
        self.ScriptList = _FakeScriptList([_FakeScriptRec(t, lang_tags) for t in script_tags])


class _FakeTTFont:
    def __init__(
        self,
        *,
        has_gsub: bool = True,
        has_gpos: bool = True,
        script_tags: list[str] | None = None,
        lang_tags: list[str] | None = None,
        cmap: dict[int, str] | None = None,
    ):
        self._cmap = cmap if cmap is not None else {cp: "glyph" for cp in REQUIRED_CODEPOINTS}
        self._tables = {}
        script_tags = script_tags if script_tags is not None else ["dev2"]
        lang_tags = lang_tags if lang_tags is not None else ["NEP"]
        if has_gsub:
            self._tables["GSUB"] = type("GSUBWrap", (), {"table": _FakeTable(script_tags, lang_tags)})
        if has_gpos:
            self._tables["GPOS"] = type("GPOSWrap", (), {"table": _FakeTable(script_tags, lang_tags)})

    def getBestCmap(self):
        return self._cmap

    def __contains__(self, key):
        return key in self._tables

    def __getitem__(self, key):
        return self._tables[key]


def test_check_font_all_pass(monkeypatch, tmp_path: Path):
    monkeypatch.setattr("nepali_font_tools.qa.TTFont", lambda _path: _FakeTTFont())
    results = check_font(tmp_path / "dummy.ttf")
    severities = {r.check_id: r.severity for r in results}
    assert severities["valid-font"] == Severity.PASS
    assert severities["devanagari-coverage"] == Severity.PASS
    assert severities["gsub-devanagari"] == Severity.PASS
    assert severities["nepali-lang-tag"] == Severity.PASS


def test_check_font_missing_gsub_fails(monkeypatch, tmp_path: Path):
    monkeypatch.setattr("nepali_font_tools.qa.TTFont", lambda _path: _FakeTTFont(has_gsub=False))
    results = check_font(tmp_path / "dummy.ttf")
    severities = {r.check_id: r.severity for r in results}
    assert severities["gsub-devanagari"] == Severity.FAIL


def test_check_font_missing_lang_tag_warns(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(
        "nepali_font_tools.qa.TTFont",
        lambda _path: _FakeTTFont(lang_tags=["HIN "]),
    )
    results = check_font(tmp_path / "dummy.ttf")
    severities = {r.check_id: r.severity for r in results}
    assert severities["nepali-lang-tag"] == Severity.WARN


def test_check_font_bad_font_file_fails(monkeypatch, tmp_path: Path):
    def _raise(_path):
        raise RuntimeError("bad font")

    monkeypatch.setattr("nepali_font_tools.qa.TTFont", _raise)
    results = check_font(tmp_path / "bad.ttf")
    assert len(results) == 1
    assert results[0].severity == Severity.FAIL


def test_run_qa_script_missing_sources(monkeypatch):
    script_path = (
        Path(__file__).resolve().parents[3] / "scripts" / "run-qa.py"
    )
    spec = importlib.util.spec_from_file_location("run_qa_script", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)

    monkeypatch.setattr(module, "SOURCES", Path("__does_not_exist__"))
    assert module.main() == 1
