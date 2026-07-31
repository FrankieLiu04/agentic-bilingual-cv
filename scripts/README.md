# Command-line workflow

All executable scripts use `uv` inline dependency metadata. Dependencies are
resolved into the `uv` cache; the repository does not create or track a virtual
environment.

## Validate structured data

```bash
scripts/validate-data data/private/resume.yaml
```

This checks JSON Schema structure plus semantic invariants:

- globally unique IDs;
- valid source and metric references;
- ordered date ranges;
- no unreferenced metrics;
- no unconfirmed, pending, or unresolved content at `render_ready`;
- no fictional claims in real documents, or private sources in fictional
  public documents.

## Read DOCX reference text

```bash
scripts/extract-docx input/resume.docx -o data/private/source-text.txt
```

This extracts paragraphs, tables, headers, and footers for agent reference.
It does not convert DOCX into resume data and does not replace visual review.

## Generate LaTeX and PDF

```bash
scripts/render data/private/resume.yaml --output-dir output
```

The command:

1. validates the YAML;
2. generates editable `resume-en.tex` and `resume-zh.tex`;
3. copies the shared `cv.cls`;
4. compiles each `.tex` directly with XeLaTeX;
5. validates both PDFs;
6. writes `validation-report.txt`.

If an existing `.tex` or `cv.cls` differs from generated content, rendering
stops to protect manual edits. Use a different output directory or explicitly
pass `--force` if replacement is intended. Use `--tex-only` to generate LaTeX
without compiling.

## Validate PDF

```bash
scripts/validate-pdf \
  --expected-pages 1 \
  --log-dir build/render/DOCUMENT_ID \
  output/resume-en.pdf output/resume-zh.pdf
```

The validator rejects unexpected page counts or page sizes, unembedded fonts,
empty metadata, broken text extraction, missing LaTeX logs, and LaTeX overflow,
font, glyph, or package warnings.

## Extract text

```bash
scripts/extract-text output/resume-en.pdf
scripts/extract-text output/resume-en.pdf output/resume-zh.pdf \
  --output-dir output/text
```

Text extraction preserves approximate layout and is intended for agent review,
not as an alternative PDF generator.

## Test and privacy checks

```bash
scripts/test
scripts/privacy-scan
scripts/privacy-scan --staged
scripts/privacy-scan --staged --deny-file data/private/release-denylist.txt
```

The privacy scanner rejects protected directories, resume binaries, absolute
home paths, non-example email addresses, probable phone numbers, and personal
profile URLs. Add release-specific private strings with repeated `--deny`
arguments, an ignored `--deny-file`, or the local `PRIVACY_DENYLIST`
environment variable.
