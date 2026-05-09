"""Config diff and ablation-axis helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import csv
import json

from skilllogboard.compare.leaderboard import rows_to_markdown


def flatten_config(config: dict[str, Any], prefix: str = "") -> dict[str, Any]:
    if not config:
        return {}
    flat: dict[str, Any] = {}
    for key in sorted(config):
        dotted = f"{prefix}.{key}" if prefix else str(key)
        value = config[key]
        if isinstance(value, dict):
            flat.update(flatten_config(value, dotted))
        else:
            flat[dotted] = _normalize_value(value)
    return flat


def build_config_diff(
    records: list[dict[str, Any]],
    include_constant: bool = False,
) -> list[dict[str, Any]]:
    flattened = [(record, flatten_config(record.get("config") or {})) for record in records]
    keys = sorted({key for _record, config in flattened for key in config})
    rows: list[dict[str, Any]] = []
    for key in keys:
        values = {str(record.get("run_id", "")): config.get(key, "") for record, config in flattened}
        distinct = sorted({_value_id(value) for value in values.values()})
        if not include_constant and len(distinct) <= 1:
            continue
        row: dict[str, Any] = {
            "key": key,
            "distinct_values": ", ".join(distinct),
            "variation_count": len(distinct),
        }
        for run_id, value in values.items():
            row[f"run:{run_id}"] = value
        rows.append(row)
    return rows


def extract_ablation_axes(
    records: list[dict[str, Any]],
    candidate_keys: list[str] | None = None,
) -> list[dict[str, Any]]:
    flattened = [(record, flatten_config(record.get("config") or {})) for record in records]
    keys = candidate_keys or sorted({key for _record, config in flattened for key in config})
    axes: list[dict[str, Any]] = []
    for key in keys:
        values = [config.get(key, "") for _record, config in flattened]
        distinct = sorted({_value_id(value) for value in values if value != ""})
        if candidate_keys is None and len(distinct) <= 1:
            continue
        counts = {value: values.count(value) for value in sorted(set(values), key=_value_id) if value != ""}
        axes.append(
            {
                "key": key,
                "distinct_values": distinct,
                "run_count": sum(counts.values()),
                "value_counts": {_value_id(key): count for key, count in counts.items()},
            }
        )
    return axes


def config_diff_columns(rows: list[dict[str, Any]]) -> list[str]:
    dynamic = sorted({key for row in rows for key in row if key.startswith("run:")})
    return ["key", "distinct_values", "variation_count", *dynamic]


def config_diff_to_markdown(rows: list[dict[str, Any]]) -> str:
    return rows_to_markdown(rows, config_diff_columns(rows))


def write_config_diff_csv(rows: list[dict[str, Any]], path: str | Path) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    columns = config_diff_columns(rows)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})
    return out


def ablation_axes_to_markdown(axes: list[dict[str, Any]]) -> str:
    if not axes:
        return "No varying config axes were detected."
    rows = [
        {
            "key": axis["key"],
            "distinct_values": ", ".join(axis.get("distinct_values", [])),
            "run_count": axis.get("run_count", 0),
        }
        for axis in axes
    ]
    return rows_to_markdown(rows, ["key", "distinct_values", "run_count"])


def _normalize_value(value: Any) -> Any:
    if isinstance(value, (list, tuple)):
        return json.dumps(list(value), sort_keys=True)
    if isinstance(value, dict):
        return json.dumps(value, sort_keys=True)
    return value


def _value_id(value: Any) -> str:
    if isinstance(value, (list, dict, tuple)):
        return json.dumps(value, sort_keys=True)
    return str(value)
