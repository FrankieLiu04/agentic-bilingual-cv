# Fictional bilingual example

`fictional-resume.yaml` is the only canonical source for an entirely fictional
candidate:

- `fictional-resume.yaml`

Every person, organization, location, experience, and metric is invented for
public template testing. Technology names are real so the example remains
useful. The email address uses the reserved `example.com` domain.

## Structured source of truth

The YAML document validates against
`data/schema/resume.schema.json`. It stores bilingual text, normalized dates,
metrics, source references, and verification status. The table below is a
compact review aid; the YAML document is authoritative.

| Area | Canonical fictional facts |
| --- | --- |
| Identity | Avery Lin / 林艾文; software engineer; Port Aurora / 曙港 |
| Education | Aster Vale Institute of Technology / 星谷理工学院; 2021-2025; B.Eng. Computer Engineering; GPA 3.8/4.0 |
| LumenArc | May-Aug 2024; 2 million simulated records/day; 35% less triage time; integration-test coverage 62%-86% |
| Cobalt Kite | Jun-Aug 2023; 8-person team; weekly reporting reduced from 4 hours to 45 minutes |
| AtlasNote | 2024; 12,000 synthetic abstracts; top-5 hit rate 71%-84%; 48 automated tests |
| MeshRoute | 2023; 50-node simulated topologies; 120 generated scenarios |
| Leadership | 2022-2024; 6 workshops; 90 students; average feedback 4.7/5 |

## Build

From the repository root:

```bash
make check-data
make examples
```

`make examples` validates the YAML, generates editable English and Chinese
`.tex` files, compiles them directly with XeLaTeX, and validates the
resulting PDFs.

## Compact verification blocks

Every claim in the YAML carries an explicit `verification` block for
auditability. To avoid repeating the same object 38 times, the example
defines one YAML anchor (`&fictional_verification` on the first metric's
verification block) and reuses it with `*fictional_verification` aliases;
`yaml.safe_load` resolves the aliases before schema validation. Real
documents may use the same pattern or repeat the block explicitly.

Generated artifacts are written to:

```text
build/examples/resume-en.tex
build/examples/resume-en.pdf
build/examples/resume-zh.tex
build/examples/resume-zh.pdf
build/examples/validation-report.txt
```

All files under `build/` are ignored by Git. To create the same editable
artifacts under the user-facing ignored output directory, run:

```bash
make render-example
```
