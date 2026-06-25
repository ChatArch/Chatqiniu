"""Output helpers for Chatqiniu CLI."""

from __future__ import annotations

import json
from typing import Any, Iterable, Mapping

import click
from chatstyle import render_dry_run, render_key_values, render_table

from .client import DryRunResult


def render_data(data: Any, *, output_format: str = "table", columns: list[str] | None = None, heading: str | None = None) -> None:
    """Render data in table, JSON, or Markdown format."""

    if isinstance(data, DryRunResult):
        render_dry_run(data.steps, heading=f"Dry run: {data.action}")
        return
    if output_format == "json":
        click.echo(json.dumps(data, indent=2, ensure_ascii=False, default=str))
        return
    if output_format == "markdown":
        click.echo(to_markdown(data, columns=columns))
        return
    if isinstance(data, Mapping):
        if "items" in data and isinstance(data["items"], list):
            render_rows(data["items"], columns=columns, heading=heading)
        elif "certs" in data and isinstance(data["certs"], list):
            render_rows(data["certs"], columns=columns, heading=heading)
        elif "domains" in data and isinstance(data["domains"], list):
            render_rows(data["domains"], columns=columns, heading=heading)
        else:
            render_key_values({str(k): _scalar(v) for k, v in data.items()}, heading=heading)
        return
    if isinstance(data, list):
        render_rows(data, columns=columns, heading=heading)
        return
    click.echo(str(data))


def render_rows(rows: Iterable[Any], *, columns: list[str] | None = None, heading: str | None = None) -> None:
    normalized = [_normalize_row(row) for row in rows]
    if not normalized:
        click.echo("No results.")
        return
    selected_columns = columns or list(normalized[0].keys())
    render_table(normalized, selected_columns, heading=heading)


def to_markdown(data: Any, *, columns: list[str] | None = None) -> str:
    rows = _extract_rows(data)
    if rows:
        normalized = [_normalize_row(row) for row in rows]
        selected_columns = columns or list(normalized[0].keys())
        lines = ["| " + " | ".join(selected_columns) + " |", "| " + " | ".join("---" for _ in selected_columns) + " |"]
        for row in normalized:
            lines.append("| " + " | ".join(str(row.get(col, "")) for col in selected_columns) + " |")
        return "\n".join(lines)
    if isinstance(data, Mapping):
        lines = ["| Key | Value |", "| --- | --- |"]
        for key, value in data.items():
            lines.append(f"| {key} | {_scalar(value)} |")
        return "\n".join(lines)
    return str(data)


def _extract_rows(data: Any) -> list[Any]:
    if isinstance(data, list):
        return data
    if isinstance(data, Mapping):
        for key in ("items", "certs", "domains"):
            value = data.get(key)
            if isinstance(value, list):
                return value
    return []


def _normalize_row(row: Any) -> dict[str, Any]:
    if isinstance(row, Mapping):
        return {str(k): _scalar(v) for k, v in row.items()}
    return {"value": _scalar(row)}


def _scalar(value: Any) -> Any:
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return json.dumps(value, ensure_ascii=False, default=str)
