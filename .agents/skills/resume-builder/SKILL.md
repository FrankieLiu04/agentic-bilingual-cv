---
name: resume-builder
description: Build, revise, render, and validate English-Chinese resumes in this repository from a DOCX or conversational input. Use when an agent must extract resume facts, ask clarification questions, create auditable private YAML, generate editable bilingual LaTeX, compile XeLaTeX PDFs, fit content responsibly, or perform final resume quality and privacy checks.
---

# Resume builder

Follow `AGENTS.md` as the authoritative workflow and privacy contract.

1. Read `data/schema/README.md`, `scripts/README.md`, and
   `template/README.md`.
2. Read the DOCX visually and structurally, or organize conversational input.
   Do not treat DOCX extraction as deterministic conversion.
3. Put real structured data only under `data/private/`. Record sources,
   verification status, metrics, pending questions, and unresolved content.
4. Never invent or silently change facts. Do not mark data `render_ready`
   until blocking questions and unresolved items are cleared.
5. Validate and render with repository scripts:

   ```bash
   scripts/validate-data data/private/resume.yaml
   scripts/render data/private/resume.yaml --output-dir output
   ```

6. Review both validation results and rendered PDF pages. Improve wording and
   prioritization before reducing typography to meet a page target.
7. Keep real source files and generated artifacts ignored. Run
   `scripts/privacy-scan --staged` before any commit.

Use the shared scripts and templates; do not create a parallel rendering or
validation path.
