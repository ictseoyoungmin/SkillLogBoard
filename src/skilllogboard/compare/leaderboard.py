"""Leaderboard helpers for multi-run comparison."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import csv

LEADERBOARD_COLUMNS = [
    "rank",
    "run_id",
    "run_name",
    "status",
    "metric_name",
    "metric_value",
    "best_step",
    "created_at",
    "warning_count",
    "error_count",
]


def latest_metric(record: dict[str, Any], metric: str) -> float | None:
    row = (record.get("metrics") or {}).get(metric)
    if not row:
        return None
    return _to_float(row.get("value"))


def best_metric(record: dict[str, Any], metric: str | None = None) -> tuple[str | None, float | None, Any]:
    best = record.get("best_metric") or {}
    name = best.get("name")
    if metric is not None and name != metric:
        return name, None, best.get("best_step")
    return name, _to_float(best.get("best_value")), best.get("best_step")


def metric_value(
    record: dict[str, Any],
    metric: str | None = None,
    value_source: str = "best_or_latest",
) -> tuple[str | None, float | None, Any]:
    selected_metric = metric or ((record.get("main_metric") or {}).get("name"))
    best_name, best_value, best_step = best_metric(record, selected_metric)
    if value_source in {"best", "best_or_latest"} and best_value is not None:
        return best_name or selected_metric, best_value, best_step
    if selected_metric is None:
        return best_name, best_value, best_step
    latest_value = latest_metric(record, selected_metric)
    return selected_metric, latest_value, (record.get("metrics") or {}).get(selected_metric, {}).get("step")


def build_leaderboard(
    records: list[dict[str, Any]],
    metric: str | None = None,
    mode: str | None = None,
    value_source: str = "best_or_latest",
) -> list[dict[str, Any]]:
    metric_mode = _normalize_mode(mode or _infer_mode(records, metric))
    prepared = []
    for index, record in enumerate(records):
        metric_name, value, best_step = metric_value(record, metric, value_source=value_source)
        prepared.append((record, metric_name, value, best_step, index))

    reverse = metric_mode == "max"
    prepared.sort(
        key=lambda item: (
            item[2] is None,
            0 if item[2] is None else (-item[2] if reverse else item[2]),
            str(item[0].get("run_id", "")),
            item[4],
        )
    )

    rows: list[dict[str, Any]] = []
    rank = 1
    for record, metric_name, value, best_step, _index in prepared:
        rows.append(
            {
                "rank": "" if value is None else rank,
                "run_id": record.get("run_id", ""),
                "run_name": record.get("run_name", ""),
                "status": record.get("status", ""),
                "metric_name": metric_name or metric or "",
                "metric_value": value,
                "best_step": best_step,
                "created_at": record.get("created_at", ""),
                "warning_count": record.get("warning_count", 0),
                "error_count": record.get("error_count", 0),
            }
        )
        if value is not None:
            rank += 1
    return rows


def write_leaderboard_csv(rows: list[dict[str, Any]], path: str | Path) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=LEADERBOARD_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: _cell(row.get(key)) for key in LEADERBOARD_COLUMNS})
    return out


def leaderboard_to_markdown(rows: list[dict[str, Any]]) -> str:
    return rows_to_markdown(rows, LEADERBOARD_COLUMNS)


def rows_to_markdown(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(_escape_markdown(_cell(row.get(col))) for col in columns) + " |")
    return "\n".join(lines)


def rows_to_latex(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    selected = columns or LEADERBOARD_COLUMNS
    lines = ["\\begin{tabular}{" + "l" * len(selected) + "}", " & ".join(selected) + r" \\", r"\hline"]
    for row in rows:
        lines.append(" & ".join(_escape_latex(_cell(row.get(col))) for col in selected) + r" \\")
    lines.append("\\end{tabular}")
    return "\n".join(lines)


def _infer_mode(records: list[dict[str, Any]], metric: str | None) -> str:
    for record in records:
        main = record.get("main_metric") or {}
        if metric is None or main.get("name") == metric:
            mode = main.get("mode")
            if mode:
                return str(mode)
        best = record.get("best_metric") or {}
        if metric is None or best.get("name") == metric:
            mode = best.get("mode")
            if mode:
                return str(mode)
    return "max"


def _normalize_mode(mode: str) -> str:
    lowered = mode.lower()
    if lowered not in {"max", "min"}:
        raise ValueError("mode must be 'max' or 'min'")
    return lowered


def _to_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _cell(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def _escape_markdown(value: str) -> str:
    return value.replace("|", "\\|")


def _escape_latex(value: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    return value
