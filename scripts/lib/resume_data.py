"""Loading and validation helpers for bilingual resume data."""

from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


class ResumeDataError(ValueError):
    """Raised when resume data is structurally or semantically invalid."""


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ResumeDataError(f"cannot read YAML {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ResumeDataError(f"{path}: document root must be an object")
    return value


def load_schema(path: Path) -> dict[str, Any]:
    try:
        import json

        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ResumeDataError(f"cannot read JSON Schema {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ResumeDataError(f"{path}: schema root must be an object")
    return value


def schema_errors(data: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    validator = Draft202012Validator(schema)
    errors: list[str] = []
    for error in sorted(
        validator.iter_errors(data),
        key=lambda item: [str(part) for part in item.path],
    ):
        pointer = "/" + "/".join(str(part) for part in error.absolute_path)
        errors.append(f"{pointer or '/'}: {error.message}")
    return errors


def _walk(value: Any, path: str = "") -> Iterator[tuple[Any, str]]:
    yield value, path or "/"
    if isinstance(value, dict):
        for key, child in value.items():
            yield from _walk(child, f"{path}/{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk(child, f"{path}/{index}")


def _date_key(value: str) -> tuple[int, int]:
    if value == "present":
        current_year = datetime.now(timezone.utc).year
        return current_year + 1, 1
    parts = value.split("-")
    return int(parts[0]), int(parts[1]) if len(parts) == 2 else 1


def semantic_errors(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    sources = data.get("sources", [])
    metrics = data.get("metrics", [])
    source_ids = [item.get("id") for item in sources if isinstance(item, dict)]
    metric_ids = [item.get("id") for item in metrics if isinstance(item, dict)]
    source_set = set(source_ids)
    metric_set = set(metric_ids)

    if len(source_ids) != len(source_set):
        errors.append("/sources: source IDs must be unique")
    if len(metric_ids) != len(metric_set):
        errors.append("/metrics: metric IDs must be unique")

    all_ids: dict[str, str] = {}
    referenced_metrics: set[str] = set()
    workflow_status = data.get("workflow", {}).get("status")
    fictional = data.get("document", {}).get("fictional")

    for value, path in _walk(data):
        if not isinstance(value, dict):
            continue

        identifier = value.get("id")
        if isinstance(identifier, str):
            if identifier in all_ids:
                errors.append(
                    f"{path}/id: duplicate ID '{identifier}' "
                    f"(first used at {all_ids[identifier]})"
                )
            else:
                all_ids[identifier] = f"{path}/id"

        verification = value.get("verification")
        if isinstance(verification, dict):
            refs = verification.get("source_refs", [])
            unknown = sorted(set(refs) - source_set)
            if unknown:
                errors.append(
                    f"{path}/verification/source_refs: unknown sources "
                    f"{', '.join(unknown)}"
                )
            status = verification.get("status")
            if workflow_status == "render_ready" and status == "needs_confirmation":
                errors.append(
                    f"{path}/verification/status: render-ready data "
                    "cannot need confirmation"
                )
            if fictional is True and status != "fictional":
                errors.append(
                    f"{path}/verification/status: fictional documents "
                    "must use fictional verification"
                )
            if fictional is False and status == "fictional":
                errors.append(
                    f"{path}/verification/status: real documents cannot "
                    "contain fictional claims"
                )

        refs = value.get("metric_refs")
        if isinstance(refs, list):
            unknown = sorted(set(refs) - metric_set)
            if unknown:
                errors.append(
                    f"{path}/metric_refs: unknown metrics {', '.join(unknown)}"
                )
            referenced_metrics.update(refs)

        date_range = value.get("date")
        if isinstance(date_range, dict):
            start = date_range.get("start")
            end = date_range.get("end")
            if isinstance(start, str) and isinstance(end, str):
                if start == "present":
                    errors.append(f"{path}/date/start: start cannot be present")
                elif _date_key(start) > _date_key(end):
                    errors.append(f"{path}/date: start must not be after end")

    unused_metrics = sorted(metric_set - referenced_metrics)
    if unused_metrics:
        errors.append(f"/metrics: unreferenced metrics {', '.join(unused_metrics)}")

    if workflow_status == "render_ready":
        if data.get("pending_questions"):
            errors.append(
                "/pending_questions: render-ready data must have no pending questions"
            )
        if data.get("unresolved_items"):
            errors.append(
                "/unresolved_items: render-ready data must have no unresolved items"
            )

    if fictional is True:
        private_sources = [
            item.get("id")
            for item in sources
            if isinstance(item, dict) and item.get("private") is True
        ]
        if private_sources:
            errors.append(
                "/sources: fictional public data cannot use private sources "
                + ", ".join(str(item) for item in private_sources)
            )

    return errors


def validate_resume(data_path: Path, schema_path: Path) -> dict[str, Any]:
    data = load_yaml(data_path)
    schema = load_schema(schema_path)
    errors = schema_errors(data, schema)
    if not errors:
        errors.extend(semantic_errors(data))
    if errors:
        formatted = "\n".join(f"- {error}" for error in errors)
        raise ResumeDataError(f"{data_path} failed validation:\n{formatted}")
    return data
