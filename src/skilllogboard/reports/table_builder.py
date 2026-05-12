"""Report-ready table builders and exporters."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
import csv
import io
import json

from skilllogboard.compare.config_diff import build_config_diff, flatten_config
from skilllogboard.compare.leaderboard import build_leaderboard
from skilllogboard.compare.run_index import build_run_index
from skilllogboard.compare.seed_group import group_runs_by_seed


@dataclass
class ReportTable:
    table_id: str
    table_type: str
    columns: list[str]
    rows: list[dict[str, Any]]
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def table_to_markdown(table: ReportTable) -> str:
    lines = [
        "| " + " | ".join(table.columns) + " |",
        "| " + " | ".join("---" for _ in table.columns) + " |",
    ]
    for row in table.rows:
        lines.append(
            "| " + " | ".join(_escape_markdown(_cell(row.get(col))) for col in table.columns) + " |"
        )
    return "\n".join(lines)


def table_to_csv_string(table: ReportTable) -> str:
    f = io.StringIO()
    writer = csv.DictWriter(f, fieldnames=table.columns, extrasaction="ignore")
    writer.writeheader()
    for row in table.rows:
        writer.writerow({column: _cell(row.get(column)) for column in table.columns})
    return f.getvalue()


def write_table_csv(table: ReportTable, path: str | Path) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(table_to_csv_string(table), encoding="utf-8")
    return out


def table_to_latex(table: ReportTable) -> str:
    lines = [
        "\\begin{tabular}{" + "l" * len(table.columns) + "}",
        " & ".join(_escape_latex(col) for col in table.columns) + r" \\",
        r"\hline",
    ]
    for row in table.rows:
        lines.append(" & ".join(_escape_latex(_cell(row.get(col))) for col in table.columns) + r" \\")
    lines.append("\\end{tabular}")
    return "\n".join(lines)


def table_to_html(table: ReportTable) -> str:
    head = "".join(f"<th>{_escape_html(column)}</th>" for column in table.columns)
    rows = []
    for row in table.rows:
        rows.append("".join(f"<td>{_escape_html(_cell(row.get(column)))}</td>" for column in table.columns))
    body = "\n".join(f"<tr>{cells}</tr>" for cells in rows)
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def build_leaderboard_table(
    root_dir_or_records: str | Path | list[dict[str, Any]],
    metric: str,
    mode: str = "max",
) -> ReportTable:
    records = _coerce_records(root_dir_or_records)
    rows = build_leaderboard(records, metric=metric, mode=mode)
    columns = [
        "rank",
        "run_id",
        "run_name",
        "metric_value",
        "best_step",
        "warning_count",
        "error_count",
    ]
    return ReportTable(
        table_id="leaderboard",
        table_type="leaderboard",
        columns=columns,
        rows=[{column: row.get(column, "") for column in columns} for row in rows],
        metadata={"metric": metric, "mode": mode},
    )


def build_seed_summary_table(
    root_dir_or_records: str | Path | list[dict[str, Any]],
    metric: str,
    mode: str = "max",
    group_by: str | list[str] | None = None,
) -> ReportTable:
    records = _coerce_records(root_dir_or_records)
    group_keys = [group_by] if isinstance(group_by, str) else group_by
    rows = group_runs_by_seed(records, metric=metric, mode=mode, group_by=group_keys)
    columns = ["group_key", "count", "mean", "std", "median", "best", "best_run_id"]
    return ReportTable(
        table_id="seed-summary",
        table_type="seed-summary",
        columns=columns,
        rows=rows,
        metadata={"metric": metric, "mode": mode, "group_by": group_keys or []},
    )


def build_config_diff_table(
    root_dir_or_records: str | Path | list[dict[str, Any]],
    include_constant: bool = False,
) -> ReportTable:
    records = _coerce_records(root_dir_or_records)
    rows = build_config_diff(records, include_constant=include_constant)
    dynamic = sorted({key for row in rows for key in row if key.startswith("run:")})
    columns = ["key", "distinct_values", "variation_count", *dynamic]
    return ReportTable(
        table_id="config-diff",
        table_type="config-diff",
        columns=columns,
        rows=rows,
        metadata={"include_constant": include_constant},
    )


def build_ablation_summary_table(
    root_dir_or_records: str | Path | list[dict[str, Any]],
    metric: str,
    mode: str = "max",
    axes: list[str] | None = None,
) -> ReportTable:
    from skilllogboard.compare.leaderboard import metric_value

    records = _coerce_records(root_dir_or_records)
    axis_keys = axes or sorted({key for record in records for key in flatten_config(record.get("config") or {})})
    rows: list[dict[str, Any]] = []
    for key in axis_keys:
        buckets: dict[str, list[float]] = {}
        for record in records:
            flat = flatten_config(record.get("config") or {})
            value_id = str(flat.get(key, ""))
            if value_id == "":
                continue
            _name, metric_val, _step = metric_value(record, metric)
            if metric_val is None:
                buckets.setdefault(value_id, [])
            else:
                buckets.setdefault(value_id, []).append(float(metric_val))
        for value_id in sorted(buckets):
            values = buckets[value_id]
            best = None
            mean = None
            if values:
                best = min(values) if mode == "min" else max(values)
                mean = sum(values) / len(values)
            rows.append(
                {
                    "axis": key,
                    "value": value_id,
                    "count": len(values),
                    "best": best,
                    "mean": mean,
                }
            )
    return ReportTable(
        table_id="ablation-summary",
        table_type="ablation-summary",
        columns=["axis", "value", "count", "best", "mean"],
        rows=rows,
        metadata={"metric": metric, "mode": mode, "axes": axis_keys},
    )


def build_rule_audit_table(root_dir_or_records: str | Path | list[dict[str, Any]]) -> ReportTable:
    records = _coerce_records(root_dir_or_records)
    rows: list[dict[str, Any]] = []
    for record in records:
        run_dir = Path(str(record.get("run_dir", "")))
        trace = run_dir / "skill_trace.jsonl"
        if not trace.exists():
            continue
        for line in trace.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            rows.append(
                {
                    "rule_id": item.get("rule_id", ""),
                    "outcome": item.get("outcome", ""),
                    "severity": item.get("severity", ""),
                    "message": item.get("message", ""),
                    "run_id": record.get("run_id", ""),
                }
            )
    columns = ["rule_id", "outcome", "severity", "message", "run_id"]
    return ReportTable(
        table_id="rule-audit",
        table_type="rule-audit",
        columns=columns,
        rows=rows,
        metadata={},
    )


def build_report_table(
    table_type: str,
    root_dir_or_records: str | Path | list[dict[str, Any]],
    metric: str = "",
    mode: str = "max",
    group_by: str | list[str] | None = None,
) -> ReportTable:
    if table_type == "leaderboard":
        return build_leaderboard_table(root_dir_or_records, metric=metric, mode=mode)
    if table_type == "seed-summary":
        return build_seed_summary_table(root_dir_or_records, metric=metric, mode=mode, group_by=group_by)
    if table_type == "config-diff":
        return build_config_diff_table(root_dir_or_records)
    if table_type == "ablation-summary":
        return build_ablation_summary_table(root_dir_or_records, metric=metric, mode=mode)
    if table_type == "rule-audit":
        return build_rule_audit_table(root_dir_or_records)
    raise ValueError(f"Unsupported report table type: {table_type}")


def _coerce_records(root_dir_or_records: str | Path | list[dict[str, Any]]) -> list[dict[str, Any]]:
    if isinstance(root_dir_or_records, list):
        return root_dir_or_records
    return build_run_index(root_dir_or_records)


def _cell(value: Any) -> str:
    return "" if value is None else str(value)


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


def _escape_html(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
