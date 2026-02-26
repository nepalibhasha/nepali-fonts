# @nepalibhasha/converter

Convert text from legacy Nepali font encodings (Preeti, Kantipur, etc.) to Unicode. Works in both browser and Node.js.

**Package size:** 13 kB (compressed) / 141 kB (unpacked)

## Installation

```bash
npm install @nepalibhasha/converter
```

## Usage

```js
import { convert } from '@nepalibhasha/converter';

const unicode = convert('k]kfnL', 'preeti');
console.log(unicode); // नेपाली
```

## Supported Fonts

The converter handles legacy font encodings commonly used in Nepali documents, newspapers, and government systems before Unicode adoption.

## Related

- [`@nepalibhasha/fonts`](https://www.npmjs.com/package/@nepalibhasha/fonts) — Optimized WOFF2 web fonts for Nepali/Devanagari
- [`nepali-converter`](https://pypi.org/project/nepali-converter/) — Python version of this converter

## License

[MIT](./LICENSE)
