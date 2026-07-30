# Resume intermediate schema

`resume.schema.json` defines the auditable intermediate document between agent
fact gathering and LaTeX authoring.

## Core rules

- Store English and Chinese wording together in every `localizedText` object.
- Store dates once as `YYYY`, `YYYY-MM`, or `present`; rendering decides how
  each language displays them. Omit an optional date or location when the
  source does not provide it; never infer one merely to fill the layout.
- Store every quantitative fact once in `metrics`. Statements refer to metrics
  through `metric_refs`.
- Attach a verification status and source references to each claim-bearing
  item.
- Keep uncertain questions in `pending_questions`.
- Keep unreadable or unclassified source material in `unresolved_items`; never
  silently discard it.
- A document marked `render_ready` must have no pending or unresolved items.

## Verification statuses

- `confirmed`: explicitly supported by user-provided material or confirmation.
- `needs_confirmation`: extracted or inferred wording that the user must check.
- `fictional`: intentionally invented public test data, never user data.

`source_refs` must point to IDs declared in the top-level `sources` list.
The M4 semantic validator checks cross-reference integrity, global ID
uniqueness, date ordering, unused metrics, workflow readiness, and separation
between fictional and real data.

## Workflow statuses

- `draft`: extraction or conversation is still in progress.
- `needs_review`: bilingual wording exists but user review is pending.
- `render_ready`: all questions and unresolved material have been cleared.

Passing JSON Schema validation proves structural correctness. It does not prove
that claims are true; agents must still preserve sources and obtain user
confirmation.

## Validation

From the repository root:

```bash
make check-data
```

This runs `scripts/validate-data`, which uses JSON Schema validation followed by
repository-specific semantic checks.
