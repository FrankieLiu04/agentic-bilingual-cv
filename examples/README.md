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
| Identity | Avery Lin / 林艾文; backend software engineer; Port Aurora / 曙港 |
| Education | Aster Vale Institute of Technology / 星谷理工学院; 2021-2025; B.Eng. Computer Science; GPA 3.9/4.0; top 3% of 300; two-year Presidential Scholarship |
| Nebula Cloud (big tech) | May-Aug 2024; Redis cache cut p99 latency from 120 ms to 45 ms at 120k QPS; Kafka pipeline at 20k events/s; 40 integration tests |
| Cobalt Kite (startup) | Jul-Aug 2023; 8-person team; weekly reporting reduced from 4 hours to 45 minutes; accessibility rework |
| AtlasNote | 2024; RAG research assistant; 12,000 synthetic abstracts; top-5 hit rate 71%-84%; 48 automated tests |
| MiniKV | 2023; Go + Raft + gRPC; 18k ops/s; 3-second leader failover |
| MeshRoute | 2023; 50-node topologies; 120 generated scenarios |
| Awards | 2023 East Asia Algorithm Contest regional silver; 2024 CloudHack best cloud innovation award (120 teams) |
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
