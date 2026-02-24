# Contributing to nepali-fonts

Thank you for your interest in contributing! This project curates Devanagari fonts and builds tooling for the Nepali digital typography ecosystem.

## Getting started

### Prerequisites

- Python 3.11+ with [uv](https://docs.astral.sh/uv/) for package management
- Node.js 22+ with npm
- Git

### Setup

```bash
# Clone the repo
git clone https://github.com/nepalibhasha/nepali-fonts.git
cd nepali-fonts

# Install Python dependencies
cd packages/font-tools && uv sync && cd ../..
cd packages/converter && uv sync && cd ../..

# Install JavaScript dependencies
npm install
```

### Running tests

```bash
# Python converter tests
cd packages/converter && uv run pytest

# JavaScript converter tests
cd packages/converter-js && npx vitest run

# Font QA
uv run python scripts/run-qa.py
```

## How to contribute

### Reporting issues

- Font rendering bugs: include browser/OS, font name, and the specific text that renders incorrectly.
- Converter bugs: include the input text, the legacy font used, and the expected vs actual output.

### Adding a font

All fonts must be **OFL-1.1** (SIL Open Font License) licensed. To add a new font:

1. Add the download entry to `scripts/download-fonts.sh`.
2. Create a metadata JSON in `fonts/metadata/<family>.json` with provenance info.
3. Run the download script and verify the font passes QA: `uv run python scripts/run-qa.py`.
4. Submit a PR with the font files and metadata.

### Improving converter mappings

Legacy font mappings live in:
- Python: `packages/converter/src/nepali_converter/maps/`
- TypeScript: `packages/converter-js/src/maps/`

Both implementations must stay in sync. If you fix a mapping in one, update the other. Add test cases for any mapping changes.

### Code style

- Python: standard library conventions, type hints where practical.
- TypeScript: strict mode, no `any` types.
- Commits: concise messages describing the change.

## Licensing

- Code contributions are licensed under MIT.
- Font contributions must be OFL-1.1. Do not submit fonts with incompatible licenses.
