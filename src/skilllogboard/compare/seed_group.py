"""Seed grouping and aggregate summaries."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import csv
import json
import statistics

from skilllogboard.compare.config_diff import flatten_config
from skilllogboard.compare.leaderboard import metric_value, rows_to_markdown

SEED_COLUMNS = [
    "group_key",
    "count",
    "mean",
    "std",
    "median",
    "best",
    "best_run_id",
]


def extract_seed(record: dict[str, Any]) -> Any:
    config = record.get("config") or {}
    if "seed" in config:
        return config.get("seed")
    manifest = record.get("manifest") or {}
    if "seed" in manifest:
        return manifest.get("seed")
    return record.get("seed")


def make_group_key(
    record: dict[str, Any],
    exclude_keys: list[str] | None = None,
    group_by: list[str] | None = None,
) -> str:
    flat = flatten_config(record.get("config") or {})
    if group_by is not None:
        selected = {key: flat.get(key, "") for key in group_by}
    else:
        excluded = set(exclude_keys or ["seed"])
        selected = {key: value for key, value in flat.items() if key not in excluded}
    return json.dumps(selected, sort_keys=True)


def group_runs_by_seed(
    records: list[dict[str, Any]],
    metric: str,
    mode: str = "max",
    group_by: list[str] | None = None,
) -> list[dict[str, Any]]:
    groups: dict[str, list[tuple[dict[str, Any], float]]] = {}
    for record in records:
        _metric_name, value, _step = metric_value(record, metric)
        key = make_group_key(record, group_by=group_by)
        if value is None:
            groups.setdefault(key, [])
            continue
        groups.setdefault(key, []).append((record, value))

    rows: list[dict[str, Any]] = []
    for group_key in sorted(groups):
        values = [value for _record, value in groups[group_key]]
        row = _summary_row(group_key, groups[group_key], values, mode)
        rows.append(row)
    return rows


def seed_summary_to_markdown(rows: list[dict[str, Any]]) -> str:
    return rows_to_markdown(rows, SEED_COLUMNS)


def write_seed_summary_csv(rows: list[dict[str, Any]], path: str | Path) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=SEED_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in SEED_COLUMNS})
    return out


def _summary_row(
    group_key: str,
    records_and_values: list[tuple[dict[str, Any], float]],
    values: list[float],
    mode: str,
) -> dict[str, Any]:
    if not values:
        return {
            "group_key": group_key,
            "count": 0,
            "mean": None,
            "std": None,
            "median": None,
            "best": None,
            "best_run_id": "",
        }
    best_record, best = _best(records_and_values, mode)
    return {
        "group_key": group_key,
        "count": len(values),
        "mean": statistics.fmean(values),
        "std": statistics.pstdev(values) if len(values) > 1 else 0.0,
        "median": statistics.median(values),
        "best": best,
        "best_run_id": best_record.get("run_id", ""),
    }


def _best(
    records_and_values: list[tuple[dict[str, Any], float]],
    mode: str,
) -> tuple[dict[str, Any], float]:
    if mode.lower() == "min":
        return min(records_and_values, key=lambda item: (item[1], str(item[0].get("run_id", ""))))
    return max(records_and_values, key=lambda item: (item[1], str(item[0].get("run_id", ""))))
