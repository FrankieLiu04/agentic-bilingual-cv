# Agentic Bilingual CV

[中文](#中文) · [English](#english)

> **Public release:** the repository includes a shared bilingual LaTeX design,
> auditable YAML schema, Codex and Claude Code skills, a fictional end-to-end
> example, automated PDF checks, privacy scanning, tests, and GitHub Actions.

## 中文

### 项目介绍

Agentic Bilingual CV 是一个面向 coding agent 的中英文简历模板仓库。你可以
使用 Claude Code、Codex 或其他 coding agent，把已有 DOCX 简历作为参考
材料，或直接在对话中描述自己的经历。Agent 会协助整理事实、追问缺失信息、
润色表述，并使用同一套设计体系生成中英文 LaTeX 与 PDF。

本项目不把 DOCX 当作稳定的机器转换格式。DOCX 和对话内容都是供 Agent 阅读
的输入；结构化中间稿才是模板渲染的内容来源。

```text
DOCX / 对话描述
        ↓
Agent 阅读、整理、追问
        ↓
结构化中间稿
        ↓
模板渲染
        ↓
中英文 LaTeX + PDF
        ↓
质量检查
```

### 快速开始

> 仓库已提供从 Agent 整理事实、YAML 校验、可编辑 LaTeX、XeLaTeX PDF 到
> 自动与视觉质量检查的完整工作流。DOCX 阅读与最终内容取舍仍由 Agent 负责。

1. 克隆仓库，并在仓库根目录启动你使用的 coding agent。
2. 选择一种输入方式：
   - 把现有简历放入 `input/`；
   - 或直接在对话中提供教育、工作、项目与技能信息。
3. 要求 Agent 使用 `resume-builder` 工作流创建结构化中间稿。
4. 审核 Agent 整理出的事实和待确认项。
5. 生成中英文 LaTeX 与 PDF，并运行质量检查。

可以先运行完全虚构的端到端示例：

```bash
make check
make render-example
```

生成结果位于被 Git 忽略的 `output/example/`。

### 使用 DOCX 输入

将 DOCX 文件放入 `input/`。该目录默认被 Git 忽略，文件不会因常规
`git add .` 被提交。然后可以向 Agent 提示：

```text
请阅读 input/ 中的 DOCX 简历，提取可确认的事实并列出所有不确定项。
不要猜测或补写经历。经我确认后，生成自然的中英文版本，并渲染和检查 PDF。
```

Agent 应保留无法识别的内容并明确标记，而不是静默丢弃。

Agent 可使用 `scripts/extract-docx input/your-resume.docx` 读取段落、表格、
页眉与页脚作为辅助，但它不是确定性转换器，仍需结合 DOCX 的可视布局审核。

### 使用对话输入

不需要准备 DOCX。你可以直接描述现有信息，例如：

```text
请帮我制作一份中英文简历。我会分段提供教育、实习、项目和技能。
先把信息整理成结构化草稿，向我确认缺失或矛盾之处，不要编造数字和成果。
确认后再生成 LaTeX 和 PDF。
```

### 示例提示词

中文：

```text
请使用本仓库的 resume-builder 工作流，根据我提供的信息制作一页中英文简历。
先提取事实和待确认项，再润色；不要改变日期、学校、公司或量化结果。
如果内容超过一页，优先压缩措辞和调整内容层级，不要无限缩小字体。
最后生成两种语言的 LaTeX 和 PDF，并运行全部质量检查。
```

English:

```text
Use this repository's resume-builder workflow to create one-page English and
Chinese resumes from the information I provide. Extract facts and questions
first, and do not invent or alter dates, organizations, metrics, or outcomes.
If the content exceeds one page, improve wording and prioritization before
reducing typography. Generate both LaTeX and PDF outputs and run all checks.
```

### 输出文件

默认输出位于 `output/`：

```text
output/
├── resume-en.tex
├── resume-en.pdf
├── resume-zh.tex
├── resume-zh.pdf
└── validation-report.txt
```

具体用户的结构化数据、LaTeX、PDF 和验证报告均为本地私密产物，默认不受
Git 追踪。仓库内只提供使用完全虚构数据构建的公开示例。

### 环境要求

当前模板构建需要：

- `uv`；
- 支持 XeLaTeX 的 TeX 发行版；
- 中文字体：Songti SC、Noto CJK SC 或 Source Han SC 字体系列之一；
- Poppler 命令行工具：`pdfinfo`、`pdffonts`、`pdftotext`，视觉检查还会使用
  `pdftoppm`。

在仓库根目录运行：

```bash
make check-data
make examples
make check
make render-example
```

`make check-data` 验证结构化 YAML。完整虚构示例位于 `build/examples/`：
`.tex` 由共享模板生成，PDF 由 XeLaTeX 直接编译对应 `.tex` 文件并自动校验。
`make render-example` 将可编辑 LaTeX、PDF 和验证报告写入 `output/example/`。

处理自己的私密 YAML：

```bash
scripts/validate-data data/private/resume.yaml
scripts/render data/private/resume.yaml --output-dir output
```

如果已有 `.tex` 或 `cv.cls` 包含手工修改，渲染器会拒绝静默覆盖；只有明确传入
`--force` 才会替换。

### 隐私与事实准确性

- `input/`、`data/private/`、`output/` 和 `build/` 默认不进入 Git。
- 请在提交前检查 `git status`，不要依赖忽略规则替代人工复核。
- Agent 不得编造经历、数字或成果，也不得擅自改变日期、学校或公司。
- 无法识别、互相矛盾或缺少依据的信息必须向用户确认。
- 发布前应扫描姓名、邮箱、电话、链接以及 PDF metadata。
- 提交前运行 `scripts/privacy-scan --staged`；还可通过被忽略的
  `--deny-file` 添加本次发布专用的姓名或标识符。
- 不要把真实简历放入 issue、日志、公开对话或示例数据。

### 模板定制

排版资源位于 `template/`。颜色、间距、字体、标题和区块样式由共享 class
集中维护；`resume.tex.j2` 从同一份结构化数据生成中英文两种变体。
定制模板时，请同时渲染两种语言并重新运行 `make check`。

### 常见问题

**这是 DOCX 到 LaTeX 的确定性转换器吗？**

不是。DOCX 是供 Agent 理解的参考材料，Agent 会先整理为结构化中间稿，再由
稳定模板渲染。

**Agent 可以帮我补全成果数字吗？**

不可以。Agent 可以指出哪里适合量化并向你提问，但不能虚构数字。

**简历必须限制为一页吗？**

一页是常见目标，不是以牺牲可读性为代价的硬约束。内容过多时，应先压缩措辞、
调整层级或与用户讨论删减，不能无限缩小字体。

**我的真实简历会被提交吗？**

敏感目录已默认忽略，但你仍应在每次提交前检查暂存内容。已经被 Git 追踪的
文件不会因为后来加入 `.gitignore` 而自动移除。

**中英文版本是逐字翻译吗？**

不是。两种版本共享相同事实，但会根据语言习惯自然表达，并保持视觉体系一致。

**可以手工修改生成的 LaTeX 吗？**

可以。生成文件是普通 LaTeX。渲染器默认保护不同于自动生成结果的现有文件，
避免下一次运行时静默覆盖手工调整。

## English

### About

Agentic Bilingual CV is a resume template designed for use with coding agents
such as Claude Code, Codex, and others. Provide an existing DOCX as
reference material or describe your background in conversation. The agent
organizes facts, asks follow-up questions, edits the writing, and produces
English and Chinese LaTeX and PDFs within one visual system.

DOCX is not treated as a stable machine-conversion API. Documents and
conversation are inputs for the agent to interpret; a structured intermediate
draft is the source used by the templates.

```text
DOCX / conversation
        ↓
Agent reads, organizes, and asks questions
        ↓
Structured intermediate draft
        ↓
Template rendering
        ↓
English and Chinese LaTeX + PDF
        ↓
Quality checks
```

### Quick start

> The repository provides the complete agent workflow from fact organization
> and YAML validation to editable LaTeX, XeLaTeX PDFs, and automated and visual
> checks. The agent remains responsible for DOCX interpretation and final
> content decisions.

1. Clone the repository and start your coding agent at the repository root.
2. Choose an input method:
   - place an existing resume in `input/`; or
   - describe your education, experience, projects, and skills in chat.
3. Ask the agent to use the `resume-builder` workflow to create a structured
   intermediate draft.
4. Review extracted facts and unresolved questions.
5. Generate both language variants and run the PDF quality checks.

Start with the entirely fictional end-to-end example:

```bash
make check
make render-example
```

Artifacts are written under the Git-ignored `output/example/` directory.

### Using a DOCX

Place the DOCX file in `input/`. The directory is ignored by Git by default, so
normal use of `git add .` will not stage it. Then prompt the agent:

```text
Read the DOCX files in input/. Extract only supported facts and list every
uncertainty. Do not infer or invent experience. After I confirm the draft,
produce natural English and Chinese versions, render the PDFs, and validate
them.
```

The agent should preserve and flag unrecognized material instead of silently
discarding it.

The agent may use `scripts/extract-docx input/your-resume.docx` to read
paragraphs, tables, headers, and footers as an aid. It is not a deterministic
converter, and the visible DOCX layout must still be reviewed.

### Using conversation input

No document is required. Start by supplying what you know:

```text
Help me create English and Chinese resumes. I will provide my education,
internships, projects, and skills in several messages. First organize them into
a structured draft and ask about missing or conflicting information. Do not
invent metrics or achievements. Render LaTeX and PDFs only after confirmation.
```

### Example prompts

English:

```text
Use this repository's resume-builder workflow to create one-page English and
Chinese resumes from the information I provide. Extract facts and questions
first, and do not invent or alter dates, organizations, metrics, or outcomes.
If the content exceeds one page, improve wording and prioritization before
reducing typography. Generate both LaTeX and PDF outputs and run all checks.
```

中文：

```text
请使用本仓库的 resume-builder 工作流，根据我提供的信息制作一页中英文简历。
先提取事实和待确认项，再润色；不要改变日期、学校、公司或量化结果。
如果内容超过一页，优先压缩措辞和调整内容层级，不要无限缩小字体。
最后生成两种语言的 LaTeX 和 PDF，并运行全部质量检查。
```

### Outputs

The default output layout is:

```text
output/
├── resume-en.tex
├── resume-en.pdf
├── resume-zh.tex
├── resume-zh.pdf
└── validation-report.txt
```

User-specific structured data, LaTeX, PDFs, and reports are private local
artifacts and are ignored by default. Only examples built from entirely
fictional data belong in the public repository.

### Requirements

The current template build requires:

- `uv`;
- a TeX distribution with XeLaTeX;
- one supported Chinese font family: Songti SC, Noto CJK SC, or Source Han SC;
- Poppler command-line tools: `pdfinfo`, `pdffonts`, and `pdftotext`;
  visual review additionally uses `pdftoppm`.

Run this at the repository root:

```bash
make check-data
make examples
make check
make render-example
```

`make check-data` validates the structured YAML. Complete fictional examples
are written to `build/examples/`: `.tex` files are generated from the shared
template, and every PDF is compiled directly from its matching `.tex` file by
XeLaTeX and validated automatically. `make render-example` writes editable
LaTeX, PDFs, and the validation report to `output/example/`.

For private YAML:

```bash
scripts/validate-data data/private/resume.yaml
scripts/render data/private/resume.yaml --output-dir output
```

If an existing `.tex` or `cv.cls` contains manual changes, the renderer refuses
to overwrite it silently. Replacement requires an explicit `--force`.

### Privacy and factual accuracy

- `input/`, `data/private/`, `output/`, and `build/` are ignored by default.
- Check `git status` before every commit; ignore rules do not replace review.
- The agent must not invent experience, metrics, or outcomes, or change dates,
  schools, or employers.
- Unreadable, contradictory, or unsupported information must be surfaced for
  confirmation.
- Before publishing, scan for names, email addresses, phone numbers, links, and
  PDF metadata.
- Run `scripts/privacy-scan --staged` before committing; use an ignored
  `--deny-file` for release-specific names or identifiers.
- Never place a real resume in public examples, issues, logs, or conversations.

### Customizing the template

Layout assets live in `template/`. Colors, spacing, typography, headings, and
section styles are centralized in a shared class, and `resume.tex.j2` generates
both language variants from the same structured data. Render and run
`make check` after every visual change.

### FAQ

**Is this a deterministic DOCX-to-LaTeX converter?**

No. DOCX is reference material for the agent. The agent first produces a
structured intermediate draft, which stable templates then render.

**Can the agent fill in missing achievement metrics?**

No. It may identify opportunities for quantification and ask questions, but it
must not fabricate numbers.

**Must every resume fit on one page?**

One page is a common target, not a reason to sacrifice readability. Improve
wording and prioritization or discuss cuts with the user before shrinking type.

**Can my real resume be committed accidentally?**

Sensitive directories are ignored by default, but always inspect staged files.
Files already tracked by Git are not protected by later `.gitignore` changes.

**Are the two languages literal translations?**

No. They share the same facts but use natural phrasing for each language while
remaining visually consistent.

**Can I edit generated LaTeX manually?**

Yes. Generated files are ordinary LaTeX. The renderer protects existing files
that differ from generated output so a later run cannot silently erase manual
refinements.

## License

This project is released under the [MIT License](LICENSE).
