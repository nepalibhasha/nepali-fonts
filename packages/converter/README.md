# nepali-converter

Convert legacy Nepali font encodings (Preeti, Kantipur, Sagarmatha, Himalb) to Unicode Devanagari. Also rescues legacy-encoded text from PDFs (non-OCR).

**Package size:** 15 kB (wheel) / 20 kB (sdist)

Part of the [nepali-fonts](https://github.com/nepalibhasha/nepali-fonts) project.

## Installation

```bash
pip install nepali-converter
```

For PDF rescue support:

```bash
pip install nepali-converter[pdf]
```

## CLI usage

Convert a legacy-encoded text file:

```bash
nepali-convert input.txt --font preeti --output output.txt
```

Auto-detect the legacy font:

```bash
nepali-convert input.txt --output output.txt
```

Read from stdin:

```bash
echo "g]kfn" | nepali-convert - --font preeti
```

Rescue text from a legacy-font PDF:

```bash
nepali-convert --pdf document.pdf --output rescued.txt
nepali-convert --pdf document.pdf --pages 1-5 --output rescued.txt
```

## Python API

```python
from nepali_converter import convert, detect_font

# Convert with a known font
text = convert("g]kfn", "preeti")  # → "नेपाल"

# Auto-detect the font
font = detect_font(legacy_text)
if font:
    text = convert(legacy_text, font)

# Rescue text from a PDF (requires nepali-converter[pdf])
from nepali_converter import rescue_pdf
rescued = rescue_pdf("document.pdf", pages=(1, 10))
```

## Supported fonts

| Font | Encoding |
|---|---|
| Preeti | Windows-1252 (cp1252) |
| Kantipur | Windows-1252 (cp1252) |
| Sagarmatha | Windows-1252 (cp1252) |
| Himalb (Fontasy Himali TT) | Windows-1252 (cp1252) |

## License

MIT
