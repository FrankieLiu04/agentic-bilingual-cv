# Template design system

`cv.cls` contains the shared public layout system. `resume.tex.j2` is the
single content template used to generate both language variants from
structured YAML; there are no hand-maintained per-language `.tex` skeletons.
The fictional example renders the full pipeline and exercises the class in
both languages.

The style was independently reconstructed from layout characteristics of a
private resume: compact A4 geometry, blue section accents, muted secondary
text, two-column entries, tight bullet lists, and language-aware typography.
No private resume text, contact details, links, PDF metadata, or binary assets
are included.

## Public class API

- `\cvsetmetadata{author}{title}` sets PDF metadata explicitly.
- `\cvheader{name}{headline}{contact line}` renders the page header.
- `\cvsection{title}` starts a language-aware section.
- `\cventry{primary}{date}{secondary}{location}` renders a two-row entry.
- `cvitems` provides a compact bullet-list environment.
- `\cvskill{label}{content}` renders a skill row.
- `\cvaward{title}{date}` renders a compact one-line honors entry.
- `\cvsep` separates contact items.

Use the `english` or `chinese` language option, plus an optional `compact` or
`airy` spacing preset (`normal` is the default). Both variants share the same
semantic macros and color system; section typography and spacing adapt to the
language and preset.

The Jinja template uses `<< value >>` and `<% block %>` delimiters so its syntax
does not conflict with LaTeX braces. Generated `.tex` files are ordinary,
editable LaTeX documents and include a local copy of `cv.cls`.

## Font fallbacks

The English template uses Latin Modern fonts distributed with TeX. The Chinese
template tries these system fonts in order:

1. Songti SC / Heiti SC
2. Noto Serif CJK SC / Noto Sans CJK SC
3. Source Han Serif SC / Source Han Sans SC

Compilation stops with a clear error if no supported Chinese serif font is
available, rather than silently producing missing glyphs.
