# Repository Definitions

This document defines the core terminology and interfaces used in this repository.

## Scope Definitions

- `source fonts`: Upstream TTF/OTF binaries stored in `fonts/sources/`.
- `font metadata`: Provenance records in `fonts/metadata/*.json` describing source, tag/version, license, and download URL.
- `legacy encoding`: Non-Unicode ASCII/extended-ASCII byte mapping used by older Nepali fonts (for example: Preeti, Kantipur, Sagarmatha, Himalb).
- `Unicode output`: Standard Devanagari text (U+0900-U+097F and related blocks) produced by converter tools.

## Package Definitions

- `packages/converter`:
  Python library and CLI for legacy-to-Unicode conversion.
  Public API:
  - `convert(text: str, source_font: str) -> str`
  - `detect_font(text: str) -> str | None`
  - `rescue_pdf(path: str, output_path: str | None = None, pages: tuple[int, int] | None = None) -> str`

- `packages/converter-js`:
  TypeScript library for browser/Node conversion.
  Public API:
  - `convert(text: string, sourceFont: string): string`
  - `detectFont(text: string): string | null`
  - `FONT_MAPS`, `SUPPORTED_FONTS`

- `packages/font-tools`:
  Font processing utilities (subsetting and QA scripts support).

- `packages/web-fonts`:
  npm package output with WOFF2 files and generated `@font-face` CSS.

## Converter Definitions

- `character map phase`: Per-font symbol-to-Devanagari substitution.
- `post-rule phase`: Ordered normalization/reordering rules (for matras, conjunct composition, and cleanup).
- `auto-detect`: Heuristic identification of legacy font from signature characters and structural patterns.
- `pass-through character`: Input character left unchanged when no map entry applies.

## PDF Rescue Definitions

- `PDF rescue`: Extraction of text-layer content and conversion of spans tagged with known legacy font names.
- `non-OCR`: No image recognition; only works when selectable text exists in the PDF.
- `page range`: 1-based inclusive range (`start-end`) used to limit extraction.

## Web Font Definitions

- `subsetting`: Keeping only needed glyph/codepoint ranges to reduce file size.
- `layout closure`: Preserving shaping dependencies referenced by OpenType layout tables during subsetting.
- `WOFF2`: Compressed web font format used for browser delivery.

## QA Definitions

- `representative sample validation`: Practical checks against curated Nepali test strings and known shaping cases.
- `conjunct tests`: Strings validating ligature/half-form behavior in Devanagari clusters.
- `locale tests`: Strings for Nepali/Hindi localized glyph behavior (for example, digit one form under locale features).

## Directory Contracts

- `fonts/sources/`: Committed upstream binaries (authoritative local source for processing).
- `fonts/metadata/`: One JSON per family; must be updated with source changes.
- `qa/`: Test strings/specimens used by validation scripts.
- `scripts/`: Build/intake automation used by contributors and CI.
