# Generated output

Rendered user resumes, LaTeX sources, PDFs, and validation reports will be
written here. This directory is ignored by Git except for this README.

Generate the fictional example here with:

```bash
make render-example
```

For private data, run:

```bash
scripts/render data/private/resume.yaml --output-dir output
```

The generated `.tex` files remain editable. PDFs are compiled directly from
those files with XeLaTeX.

The tracked public example remains the structured YAML under `examples/`;
generated LaTeX and PDFs stay ignored.
