# @nepalibhasha/fonts

Optimized WOFF2 web fonts for Nepali and Devanagari text, with ready-to-use CSS `@font-face` declarations.

**Package size:** 3.1 MB (compressed) / 6.1 MB (unpacked) — 60 WOFF2 files + 8 CSS files

## Included Fonts

| Font | Weights | Variants |
|------|---------|----------|
| Hind | 300–700 | Full, Nepali subset |
| Mukta | 200–800 | Full, Nepali subset |
| Noto Sans Devanagari | 100–900 | Full, Nepali subset |
| Noto Serif Devanagari | 100–900 | Full, Nepali subset |

**Full** variants include Devanagari + Latin + extended Unicode ranges.
**Nepali subset** variants are smaller, covering only Nepali Devanagari + Basic Latin.

## Installation

```bash
npm install @nepalibhasha/fonts
```

## Usage

Import the CSS for the font you need:

```css
/* Full Devanagari + Latin range */
@import '@nepalibhasha/fonts/css/noto-sans-devanagari.css';

/* Smaller Nepali-only subset */
@import '@nepalibhasha/fonts/css/noto-sans-devanagari-nepali.css';
```

Then use the font family in your styles:

```css
body {
  font-family: 'Noto Sans Devanagari', sans-serif;
}
```

### Available CSS files

- `css/hind.css` / `css/hind-nepali.css`
- `css/mukta.css` / `css/mukta-nepali.css`
- `css/noto-sans-devanagari.css` / `css/noto-sans-devanagari-nepali.css`
- `css/noto-serif-devanagari.css` / `css/noto-serif-devanagari-nepali.css`

## License

Font files are licensed under the [SIL Open Font License 1.1](https://openfontlicense.org/).
