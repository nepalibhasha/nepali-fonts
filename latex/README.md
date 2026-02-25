# LaTeX Support

This folder provides a small package, `nepali.sty`, for Nepali typesetting with XeLaTeX/LuaLaTeX.

## Requirements

- TeX engine: `xelatex` or `lualatex`
- `fontspec`
- `polyglossia`

`pdfLaTeX` is not supported.

## Usage

From a `.tex` file:

```latex
\usepackage{nepali}
\textnepali{नमस्ते संसार}
```

For local repo fonts, override the default font with `\setnepalifont`:

```latex
\setnepalifont[
  Path=../../fonts/sources/noto-sans-devanagari/,
  Extension=.ttf,
  UprightFont=NotoSansDevanagari-Regular,
  BoldFont=NotoSansDevanagari-Bold
]{NotoSansDevanagari-Regular}
```

## Examples

- `examples/basic-nepali.tex`
- `examples/mixed-script.tex`
- `examples/font-specimen.tex`
- `examples/advanced-usage.tex` (bold/slanted emphasis, mixed fonts, mixed scripts)

Compile from `latex/examples/` with:

```bash
TEXINPUTS=../: xelatex basic-nepali.tex
TEXINPUTS=../: lualatex mixed-script.tex
TEXINPUTS=../: xelatex font-specimen.tex
TEXINPUTS=../: xelatex advanced-usage.tex
```
