# End-to-end testing

## Public conversation path

`examples/fictional-resume.yaml` represents facts supplied in conversation.
It is deliberately fictional and safe to publish.

```bash
make check
make render-example
```

This validates the schema and semantic invariants, generates both editable
LaTeX files, compiles both PDFs with XeLaTeX, checks PDF structure and LaTeX
logs, reports per-page fill percentages, verifies the agent-skill copies are
in sync, runs unit tests, and scans public candidates for privacy leaks.

## Private DOCX path

Keep the source document and all derived artifacts in ignored locations:

```bash
scripts/extract-docx input/resume.docx --output data/private/source-text.txt
scripts/validate-data data/private/resume.yaml
scripts/render data/private/resume.yaml --output-dir output/private-docx-test
```

The release gate for a private DOCX test is:

- every retained fact has a source and verification state;
- unresolved material is surfaced instead of discarded;
- English and Chinese `.tex` files are generated from the same YAML;
- both PDFs compile directly from LaTeX and pass automated checks;
- every rendered page is visually inspected;
- no private source or generated artifact appears in the staged file list.

The repository maintainers completed this path before the first public
release. The private input and outputs were intentionally not committed.
