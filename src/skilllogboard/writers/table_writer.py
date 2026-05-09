"""Dependency-light table writer."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import csv
import html
import re


def save_table(name: str, table: Any, output_dir: str | Path) -> Path:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = _unique_path(output_dir, f"{_safe_name(name)}.csv")

    if hasattr(table, "to_csv"):
        table.to_csv(csv_path, index=False)
        if hasattr(table, "to_html"):
            html_path = csv_path.with_suffix(".html")
            html_path.write_text(table.to_html(index=False), encoding="utf-8")
        return csv_path

    if not isinstance(table, list) or any(not isinstance(row, dict) for row in table):
        raise TypeError("table must be a list of dictionaries or an object with to_csv()")

    fieldnames: list[str] = []
    for row in table:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(str(key))

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in table:
            writer.writerow(row)

    html_path = csv_path.with_suffix(".html")
    html_path.write_text(_to_html_table(fieldnames, table), encoding="utf-8")
    return csv_path


def _safe_name(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9가-힣._-]+", "_", value)
    return re.sub(r"_+", "_", value).strip("._-") or "table"


def _unique_path(directory: Path, filename: str) -> Path:
    candidate = directory / filename
    if not candidate.exists():
        return candidate
    stem = candidate.stem
    suffix = candidate.suffix
    for idx in range(1, 1000):
        suffixed = directory / f"{stem}_{idx:03d}{suffix}"
        if not suffixed.exists():
            return suffixed
    raise RuntimeError(f"Could not create unique table path for {filename!r}")


def _to_html_table(fieldnames: list[str], rows: list[dict[str, Any]]) -> str:
    header = "".join(f"<th>{html.escape(str(name))}</th>" for name in fieldnames)
    body = []
    for row in rows:
        cells = "".join(f"<td>{html.escape(str(row.get(name, '')))}</td>" for name in fieldnames)
        body.append(f"<tr>{cells}</tr>")
    if not rows:
        body.append("<tr></tr>")
    return (
        "<!doctype html>\n"
        "<html><head><meta charset=\"utf-8\"><title>Table</title></head><body>\n"
        "<table>\n<thead><tr>"
        + header
        + "</tr></thead>\n<tbody>\n"
        + "\n".join(body)
        + "\n</tbody>\n</table>\n</body></html>\n"
    )
