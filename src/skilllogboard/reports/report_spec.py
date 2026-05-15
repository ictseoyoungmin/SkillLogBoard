"""Parser for the simple Markdown ReportSpec block format."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import re

import yaml


class ReportSpecParseError(ValueError):
    """Raised when a report spec block is malformed."""


@dataclass
class ReportSpecItem:
    id: str
    kind: str
    type: str
    output: str = ""
    title: str = ""
    metric: str = ""
    mode: str = "max"
    group_by: list[str] = field(default_factory=list)
    metrics: list[str] = field(default_factory=list)
    render_mode: str = ""
    baseline_run_id: str = ""
    reference_run_id: str = ""
    delta_mode: str = ""
    params: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind,
            "type": self.type,
            "output": self.output,
            "title": self.title,
            "metric": self.metric,
            "mode": self.mode,
            "group_by": self.group_by,
            "metrics": self.metrics,
            "render_mode": self.render_mode,
            "baseline_run_id": self.baseline_run_id,
            "reference_run_id": self.reference_run_id,
            "delta_mode": self.delta_mode,
            "params": self.params,
        }


def parse_report_spec(path: str | Path) -> list[ReportSpecItem]:
    return parse_report_spec_text(Path(path).read_text(encoding="utf-8"))


def parse_report_spec_text(text: str) -> list[ReportSpecItem]:
    items: list[ReportSpecItem] = []
    current_id: str | None = None
    current_fields: dict[str, Any] = {}

    def flush() -> None:
        nonlocal current_id, current_fields
        if current_id is None:
            return
        items.append(_build_item(current_id, current_fields))
        current_id = None
        current_fields = {}

    for raw_line in text.splitlines():
        line = raw_line.strip()
        heading = re.match(r"^##\s+((?:REPORT|TABLE|FIG)-[A-Za-z0-9_-]+)\s*$", line)
        if heading:
            flush()
            current_id = heading.group(1)
            current_fields = {}
            continue
        if current_id is None:
            continue
        if line.startswith("## "):
            flush()
            continue
        if not line or line.startswith("#"):
            continue
        if not line.startswith("- "):
            continue
        key, value = _parse_bullet(line)
        current_fields[key] = value

    flush()
    return items


def _parse_bullet(line: str) -> tuple[str, Any]:
    body = line[2:].strip()
    if ":" not in body:
        raise ReportSpecParseError(f"Malformed report spec metadata line: {line}")
    key, raw_value = body.split(":", 1)
    key = key.strip()
    raw_value = raw_value.strip()
    if not key:
        raise ReportSpecParseError(f"Missing metadata key in line: {line}")
    if raw_value == "":
        return key, ""
    try:
        return key, yaml.safe_load(raw_value)
    except yaml.YAMLError as exc:
        raise ReportSpecParseError(f"Could not parse metadata value for {key!r}: {raw_value}") from exc


def _build_item(item_id: str, fields: dict[str, Any]) -> ReportSpecItem:
    fields = dict(fields)
    kind = str(fields.pop("kind", _infer_kind(item_id))).lower()
    item_type = str(fields.pop("type", _default_type(kind)))
    output = str(fields.pop("output", ""))
    title = str(fields.pop("title", item_id.replace("-", " ").title()))
    metric = str(fields.pop("metric", ""))
    mode = str(fields.pop("mode", "max"))
    group_by = _as_list(fields.pop("group_by", []))
    metrics = _as_list(fields.pop("metrics", []))
    render_mode = str(fields.pop("render_mode", ""))
    baseline_run_id = str(fields.pop("baseline_run_id", fields.pop("baseline", "")))
    reference_run_id = str(fields.pop("reference_run_id", fields.pop("reference", "")))
    delta_mode = str(fields.pop("delta_mode", ""))
    return ReportSpecItem(
        id=item_id,
        kind=kind,
        type=item_type,
        output=output,
        title=title,
        metric=metric,
        mode=mode,
        group_by=group_by,
        metrics=metrics,
        render_mode=render_mode,
        baseline_run_id=baseline_run_id,
        reference_run_id=reference_run_id,
        delta_mode=delta_mode,
        params=fields,
    )


def _infer_kind(item_id: str) -> str:
    prefix = item_id.split("-", 1)[0].lower()
    return "figure" if prefix == "fig" else prefix


def _default_type(kind: str) -> str:
    if kind == "report":
        return "research-report"
    if kind == "table":
        return "leaderboard"
    if kind == "figure":
        return "metric-curve-overlay"
    return kind


def _as_list(value: Any) -> list[str]:
    if value in (None, ""):
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]
