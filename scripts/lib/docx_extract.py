"""Extract reference text from DOCX without treating it as a conversion API."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from docx.document import Document as DocumentType
from docx.table import Table
from docx.text.paragraph import Paragraph


def _blocks(parent: Any) -> Iterator[Paragraph | Table]:
    if isinstance(parent, DocumentType):
        container = parent.element.body
    else:
        container = parent._element
    for child in container.iterchildren():
        if child.tag.endswith("}p"):
            yield Paragraph(child, parent)
        elif child.tag.endswith("}tbl"):
            yield Table(child, parent)


def _table_text(table: Table) -> list[str]:
    rows: list[str] = []
    for row in table.rows:
        cells: list[str] = []
        for cell in row.cells:
            text = " ".join(cell.text.split())
            if text and text not in cells:
                cells.append(text)
        if any(cells):
            rows.append(" | ".join(cells))
    return rows


def _container_text(parent: Any) -> list[str]:
    lines: list[str] = []
    for block in _blocks(parent):
        if isinstance(block, Paragraph):
            text = " ".join(block.text.split())
            if text:
                lines.append(text)
        else:
            lines.extend(_table_text(block))
    return lines


def extract_docx_text(document: DocumentType) -> str:
    sections: list[tuple[str, list[str]]] = []

    header_lines: list[str] = []
    footer_lines: list[str] = []
    for section in document.sections:
        header_lines.extend(_container_text(section.header))
        footer_lines.extend(_container_text(section.footer))
    if header_lines:
        sections.append(("header", list(dict.fromkeys(header_lines))))

    body_lines = _container_text(document)
    sections.append(("body", body_lines))

    if footer_lines:
        sections.append(("footer", list(dict.fromkeys(footer_lines))))

    output: list[str] = []
    for label, lines in sections:
        output.append(f"[{label}]")
        output.extend(lines)
        output.append("")
    return "\n".join(output).rstrip() + "\n"
