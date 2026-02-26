# nepali-fonts

Curated OFL-1.1 Devanagari fonts and offline tooling for Nepali digital typography.

**[Live Demo & Docs](https://nepalibhasha.github.io/nepali-fonts/)** — compare fonts, convert legacy text, view specimens

Definitions and interface contracts: [`DEFINITIONS.md`](DEFINITIONS.md)

## What's included

- **Curated fonts** — OFL-1.1 Devanagari fonts validated for Nepali use (Noto Sans/Serif Devanagari, Mukta, Hind)
- **Legacy converter** — Convert Preeti, Kantipur, Sagarmatha, Himalb to Unicode (Python CLI + JS/TS)
- **PDF rescue** — Extract and convert legacy-encoded text from PDFs (non-OCR)
- **Web fonts** — Pre-subsetted WOFF2 with layout closure preserved, distributed as npm package
- **LaTeX package** — `nepali.sty` for XeLaTeX/LuaLaTeX academic typesetting

## Published packages

| Package | Registry | Size | Install |
|---------|----------|------|---------|
| [`@nepalibhasha/fonts`](https://www.npmjs.com/package/@nepalibhasha/fonts) | npm | 3.1 MB | `npm install @nepalibhasha/fonts` |
| [`@nepalibhasha/converter`](https://www.npmjs.com/package/@nepalibhasha/converter) | npm | 13 kB | `npm install @nepalibhasha/converter` |
| [`nepali-converter`](https://pypi.org/project/nepali-converter/) | PyPI | 15 kB | `pip install nepali-converter` |

## Quick start

### Legacy-to-Unicode converter (Python)

```bash
pip install nepali-converter
nepali-convert input.txt --font preeti --output output.txt
```

Auto-detect the legacy font:

```bash
nepali-convert input.txt --output output.txt
```

Rescue text from a legacy-font PDF (requires `[pdf]` extra):

```bash
pip install nepali-converter[pdf]
nepali-convert --pdf document.pdf --output rescued.txt
```

### Web fonts (npm)

```bash
npm install @nepalibhasha/fonts
```

```css
@import '@nepalibhasha/fonts/css/noto-sans-devanagari.css';

body {
  font-family: 'Noto Sans Devanagari', sans-serif;
}
```

### LaTeX

```latex
\usepackage{nepali}

\textnepali{नमस्ते संसार}

\begin{nepali}
नेपाल दक्षिण एशियाको एक सुन्दर देश हो।
\end{nepali}
```

Requires XeLaTeX or LuaLaTeX (not pdfLaTeX).

## Repository structure

```
nepali-fonts/
├── fonts/                   # Curated font collection
│   ├── sources/             # Original TTF/OTF from upstream
│   └── metadata/            # Provenance JSON per family
├── packages/
│   ├── font-tools/          # Python: subsetting, QA
│   ├── converter/           # Python: legacy-to-Unicode + PDF rescue
│   ├── converter-js/        # TS/JS: legacy-to-Unicode for web
│   └── web-fonts/           # npm: @nepalibhasha/fonts
├── latex/                   # nepali.sty + examples
├── site/                    # Demo site (GitHub Pages)
├── qa/                      # Test strings and specimens
└── scripts/                 # Font download, build, QA scripts
```

## Supported legacy fonts

| Font | Status |
|---|---|
| Preeti | Supported |
| Kantipur | Supported |
| Sagarmatha | Supported |
| Himalb | Supported |

## License

- **Tools and code**: [MIT](LICENSE)
- **Fonts**: [OFL-1.1](https://openfontlicense.org/) (SIL Open Font License)
