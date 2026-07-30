# Agentic Bilingual CV repository contract

## Purpose

Turn a user-provided DOCX or conversation into an auditable bilingual resume:

```text
DOCX or conversation
  -> fact extraction and questions
  -> bilingual YAML
  -> editable English and Chinese LaTeX
  -> XeLaTeX PDFs
  -> automated and visual validation
```

DOCX is reference material for an agent, not a deterministic conversion API.
The generated PDFs must always come directly from LaTeX.

## Privacy boundary

- Treat `input/`, `data/private/`, `output/`, and `build/` as private or
  generated.
- Never move real names, contacts, links, source text, YAML, LaTeX, PDFs, logs,
  or metadata into tracked examples.
- Use only deliberately fictional data under `examples/`.
- Inspect `git status`, staged files, and PDF metadata before any commit.
- Do not read or modify unrelated private files.

## Factual integrity

- Never invent or silently alter experience, dates, organizations, metrics, or
  outcomes.
- Preserve uncertain facts in `pending_questions`.
- Preserve unreadable or unclassified source content in `unresolved_items`.
- Use `needs_confirmation` until evidence or the user resolves a claim.
- Set `workflow.status: render_ready` only when blocking questions and
  unresolved items are empty and every real claim is confirmed.
- Keep quantitative values in `metrics`; reference them with `metric_refs`.
- Keep normalized dates in YAML. Let the renderer localize their display.

## Resume workflow

1. Inspect the repository and read:
   - `data/schema/README.md`
   - `scripts/README.md`
   - `template/README.md`
2. Gather input:
   - For DOCX, read paragraphs, tables, headers, footers, and visible layout.
     Use `scripts/extract-docx` only as a text fallback; review the rendered
     document when layout carries meaning.
   - For conversation, summarize supplied facts and ask about omissions or
     contradictions.
3. Create or update a private YAML file under `data/private/`.
4. Present extracted facts, proposed bilingual wording, pending questions, and
   unresolved material to the user before declaring it ready.
5. Run:

   ```bash
   scripts/validate-data data/private/resume.yaml
   scripts/render data/private/resume.yaml --output-dir output
   ```

6. Inspect `output/validation-report.txt`, extract PDF text when useful, render
   every PDF page to images, and visually check both languages.
7. Iterate on YAML wording first. Edit generated LaTeX only for deliberate
   final layout refinements.

## Page fitting

When content exceeds the target page count, adjust in this order:

1. remove repetition and tighten wording without changing facts;
2. prioritize the most relevant content with the user;
3. reduce low-value detail or move it to an optional longer version;
4. adjust spacing conservatively.

Do not preserve one page by repeatedly shrinking type, margins, or line spacing
until readability suffers.

## Commands

```bash
make check
make render-example
scripts/validate-data PATH.yaml
scripts/render PATH.yaml --output-dir output
scripts/extract-text output/resume-en.pdf
scripts/privacy-scan
```

Use `--force` with `scripts/render` only when the user intends to replace
manually edited generated LaTeX or `cv.cls`.

## Acceptance criteria

A completed resume task requires:

- supported facts and translations are consistent;
- pending and unresolved items are visible or cleared;
- YAML passes structural and semantic validation;
- both `.tex` files remain editable;
- both PDFs compile with XeLaTeX;
- target page count, portrait A4, embedded fonts, metadata, text extraction,
  and LaTeX logs pass;
- visual inspection finds no clipping, overlap, broken glyphs, or unreadable
  typography;
- no private artifact is staged.

Repository changes additionally require `make check` and
`scripts/privacy-scan --staged` before commit.
