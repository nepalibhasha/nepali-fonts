# Test fixtures

## PDF files

These are synthetic PDFs created for integration testing of `rescue_pdf`.

The PDFs contain legacy-encoded text (e.g. `g]kfn` in Preeti encoding) with
font metadata that identifies the legacy font. However, the actual font programs
are **not embedded** in the PDFs, so the legacy text will be invisible when
opened in a PDF viewer — only standard fonts like Helvetica will render.

This is expected. The `rescue_pdf` function works at the text-extraction layer,
reading font names and raw text from the PDF structure. Visual rendering is
not required.

### Files

- `preeti_sample.pdf` — Single page with Preeti-encoded text + Helvetica text
- `preeti_sample_rescued.txt` — Expected output after rescue
- `multipage_sample.pdf` — Three pages of Preeti-encoded text
- `multipage_sample_rescued.txt` — Expected output after rescue

### Regenerating

From the `packages/converter/` directory:

```bash
uv run python -c "
from tests.test_pdf_integration import _build_test_pdf, _build_multipage_pdf
from nepali_converter.pdf import rescue_pdf

with open('tests/fixtures/preeti_sample.pdf', 'wb') as f:
    f.write(_build_test_pdf([('Preeti', 'g]kfn'), ('Helvetica', 'Hello World')]))

with open('tests/fixtures/multipage_sample.pdf', 'wb') as f:
    f.write(_build_multipage_pdf([
        [('Preeti', 'g]kfn'), ('Helvetica', 'Hello World')],
        [('Preeti', 'gd:t]'), ('Preeti', 'lxdfn')],
        [('Preeti', '!@#\$%^&*()')],
    ]))

rescue_pdf('tests/fixtures/preeti_sample.pdf', output_path='tests/fixtures/preeti_sample_rescued.txt')
rescue_pdf('tests/fixtures/multipage_sample.pdf', output_path='tests/fixtures/multipage_sample_rescued.txt')
"
```
