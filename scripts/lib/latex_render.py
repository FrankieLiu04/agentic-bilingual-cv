"""Render validated resume data into editable LaTeX."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined

MONTHS_EN = (
    "",
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
)

TEX_ESCAPES = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def tex_escape(value: Any) -> str:
    return "".join(TEX_ESCAPES.get(char, char) for char in str(value))


def _format_date_value(value: str, locale: str) -> str:
    if value == "present":
        return "Present" if locale == "en" else "至今"
    year, *month = value.split("-")
    if not month:
        return year
    month_number = int(month[0])
    if locale == "en":
        return f"{MONTHS_EN[month_number]} {year}"
    return f"{year} 年 {month_number} 月"


def format_date_range(date_range: dict[str, str], locale: str) -> str:
    start = date_range["start"]
    end = date_range["end"]
    if start == end:
        return _format_date_value(start, locale)
    return f"{_format_date_value(start, locale)} -- {_format_date_value(end, locale)}"


def locale_join(values: list[str], locale: str) -> str:
    separator = ", " if locale == "en" else "、"
    return separator.join(values)


def render_latex(
    data: dict[str, Any],
    locale: str,
    template_dir: Path,
) -> str:
    environment = Environment(
        loader=FileSystemLoader(template_dir),
        undefined=StrictUndefined,
        autoescape=False,
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
        variable_start_string="<<",
        variable_end_string=">>",
        block_start_string="<%",
        block_end_string="%>",
        comment_start_string="<#",
        comment_end_string="#>",
    )
    template = environment.get_template("resume.tex.j2")
    metric_map = {item["id"]: item for item in data["metrics"]}

    def localized(value: dict[str, str]) -> str:
        return tex_escape(value[locale])

    def date_text(value: dict[str, str]) -> str:
        return tex_escape(format_date_range(value, locale))

    def technologies(values: list[str]) -> str:
        return tex_escape(locale_join(values, locale))

    def metric_summary(refs: list[str]) -> str:
        parts: list[str] = []
        label_separator = ": " if locale == "en" else "："
        item_separator = "; " if locale == "en" else "；"
        for ref in refs:
            metric = metric_map[ref]
            display = metric["display"][locale]
            label = metric.get("label", {}).get(locale)
            parts.append(f"{label}{label_separator}{display}" if label else display)
        return tex_escape(item_separator.join(parts))

    labels = {
        "en": {
            "education": "Education",
            "experience": "Experience",
            "projects": "Projects",
            "activities": "Leadership",
            "skills": "Skills",
            "title_suffix": "Resume",
        },
        "zh": {
            "education": "教育经历",
            "experience": "工作经历",
            "projects": "项目经历",
            "activities": "领导力",
            "skills": "技能",
            "title_suffix": "简历",
        },
    }[locale]

    basics = data["basics"]
    name = basics["name"][locale]
    return template.render(
        data=data,
        locale=locale,
        class_option="english" if locale == "en" else "chinese",
        labels=labels,
        metadata_author=tex_escape(name),
        metadata_title=tex_escape(f"{name} - {labels['title_suffix']}"),
        display_name=tex_escape(name.upper() if locale == "en" else name),
        localized=localized,
        date_text=date_text,
        technologies=technologies,
        metric_summary=metric_summary,
        tex_escape=tex_escape,
    )
