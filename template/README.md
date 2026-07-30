# Template design system

`cv.cls` contains the shared public layout system. `resume-en.tex` and
`resume-zh.tex` are minimal language-specific skeletons used to exercise the
class. `resume.tex.j2` is the shared M4 content template used to generate both
language variants from structured YAML.

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
- `\cvsep` separates contact items.

Use the `english` or `chinese` document-class option. Both variants share the
same spacing, semantic macros, and color system; section typography adapts to
the language.

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
