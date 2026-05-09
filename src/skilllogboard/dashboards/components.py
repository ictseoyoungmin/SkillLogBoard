"""Dashboard data loading and HTML component helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import csv
import html
import json

import yaml


CORE_FILES = [
    "manifest.yaml",
    "config.yaml",
    "metrics.csv",
    "events.jsonl",
    "skill_trace.jsonl",
    "artifact_index.json",
    "summary.md",
    "dashboard.html",
]


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_events(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    events = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            events.append(json.loads(line))
    return events


def load_metrics(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            parsed = dict(row)
            parsed["value"] = _to_float(row.get("value"))
            parsed["step"] = _to_int_or_text(row.get("step"))
            parsed["metadata"] = _load_metadata(row.get("metadata_json"))
            rows.append(parsed)
    return rows


def group_metrics(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        name = str(row.get("name", ""))
        if name:
            grouped.setdefault(name, []).append(row)
    return grouped


def load_run_context(run_dir: str | Path) -> dict[str, Any]:
    run_dir = Path(run_dir)
    warnings: list[str] = []
    manifest_path = run_dir / "manifest.yaml"
    config_path = run_dir / "config.yaml"
    metrics_path = run_dir / "metrics.csv"
    events_path = run_dir / "events.jsonl"
    artifact_index_path = run_dir / "artifact_index.json"
    skill_trace_path = run_dir / "skill_trace.jsonl"

    for path in [manifest_path, config_path, metrics_path, events_path, artifact_index_path, skill_trace_path]:
        if not path.exists():
            warnings.append(f"Missing optional file: {path.name}")

    manifest = load_yaml(manifest_path)
    config = load_yaml(config_path)
    metrics = load_metrics(metrics_path)
    events = load_events(events_path)
    artifact_index = load_json(artifact_index_path)
    skill_trace = load_events(skill_trace_path)
    artifacts = list(artifact_index.get("artifacts", []))
    file_links = [
        {"label": name, "href": name}
        for name in CORE_FILES
        if (run_dir / name).exists()
    ]

    return {
        "run_dir": str(run_dir),
        "title": f"SkillLogBoard Dashboard - {manifest.get('run_name') or run_dir.name}",
        "manifest": manifest,
        "config": config,
        "metrics": metrics,
        "metric_series": group_metrics(metrics),
        "events_summary": summarize_events(events),
        "skill_trace": skill_trace,
        "rule_audit_summary": summarize_rule_audit(skill_trace),
        "artifacts": artifacts,
        "file_links": file_links,
        "warnings": warnings,
    }


def summarize_events(events: list[dict[str, Any]]) -> dict[str, Any]:
    counts: dict[str, int] = {}
    for event in events:
        event_type = str(event.get("type", "unknown"))
        counts[event_type] = counts.get(event_type, 0) + 1
    return {"count": len(events), "by_type": counts}


def summarize_rule_audit(records: list[dict[str, Any]]) -> dict[str, Any]:
    counts: dict[str, int] = {}
    actionable = []
    for record in records:
        outcome = str(record.get("outcome", "unknown"))
        counts[outcome] = counts.get(outcome, 0) + 1
        if outcome in {"warning", "error", "planned"}:
            actionable.append(record)
    return {"count": len(records), "by_outcome": counts, "actionable": actionable}


def render_best_metric_card(manifest: dict[str, Any]) -> str:
    main_metric = manifest.get("main_metric") or {}
    best_metric = manifest.get("best_metric") or {}
    if not main_metric and not best_metric:
        return '<p class="empty">No main metric configured yet.</p>'
    name = best_metric.get("name") or main_metric.get("name", "")
    mode = best_metric.get("mode") or main_metric.get("mode", "")
    value = best_metric.get("best_value")
    step = best_metric.get("best_step")
    if value is None:
        return (
            "<div class=\"metric-card\">"
            f"<strong>{_esc(name)}</strong><span>Mode: {_esc(mode)}</span>"
            "<span>No best value has been logged yet.</span></div>"
        )
    return (
        "<div class=\"metric-card\">"
        f"<strong>{_esc(name)}</strong>"
        f"<span>Mode: {_esc(mode)}</span>"
        f"<span>Best value: {_esc(value)}</span>"
        f"<span>Best step: {_esc(step)}</span>"
        "</div>"
    )


def render_metric_panel(metric_series: dict[str, list[dict[str, Any]]]) -> str:
    if not metric_series:
        return '<p class="empty">No metrics have been logged yet.</p>'
    rows = ["<table><thead><tr><th>Metric</th><th>Step</th><th>Value</th></tr></thead><tbody>"]
    for name, series in metric_series.items():
        for point in series:
            rows.append(
                "<tr>"
                f"<td>{_esc(name)}</td>"
                f"<td>{_esc(point.get('step', ''))}</td>"
                f"<td>{_esc(point.get('value', ''))}</td>"
                "</tr>"
            )
    rows.append("</tbody></table>")
    rows.append(_render_svg(metric_series))
    return "\n".join(rows)


def render_config_table(config: dict[str, Any]) -> str:
    if not config:
        return '<p class="empty">No config values are available.</p>'
    rows = ["<table><thead><tr><th>Key</th><th>Value</th></tr></thead><tbody>"]
    for key, value in sorted(flatten_config(config).items()):
        css = " class=\"key-field\"" if key in {"model_name", "dataset_name", "seed", "optimizer", "lr", "batch_size"} else ""
        rows.append(f"<tr{css}><td>{_esc(key)}</td><td><code>{_esc(value)}</code></td></tr>")
    rows.append("</tbody></table>")
    return "\n".join(rows)


def render_artifact_table(artifacts: list[dict[str, Any]]) -> str:
    if not artifacts:
        return '<p class="empty">No artifacts, images, or tables have been logged yet.</p>'
    rows = [
        "<table><thead><tr><th>Name</th><th>Type</th><th>Path</th><th>Mode</th><th>Size</th></tr></thead><tbody>"
    ]
    for item in artifacts:
        path = item.get("path")
        source = item.get("source") or ""
        path_html = f'<a href="{_esc(path)}">{_esc(path)}</a>' if path else _esc(source)
        mode = "copy" if item.get("copy") else "reference"
        rows.append(
            "<tr>"
            f"<td>{_esc(item.get('name', ''))}</td>"
            f"<td>{_esc(item.get('type', ''))}</td>"
            f"<td>{path_html}</td>"
            f"<td>{mode}</td>"
            f"<td>{_esc(item.get('size', ''))}</td>"
            "</tr>"
        )
    rows.append("</tbody></table>")
    return "\n".join(rows)


def render_rule_audit(records: list[dict[str, Any]]) -> str:
    if not records:
        return '<p class="empty">No skill_trace.jsonl rule results are available.</p>'
    rows = [
        "<table><thead><tr><th>Rule</th><th>Type</th><th>Status</th><th>Outcome</th><th>Severity</th><th>Message</th></tr></thead><tbody>"
    ]
    for record in records:
        rows.append(
            "<tr>"
            f"<td>{_esc(record.get('rule_id', ''))}</td>"
            f"<td>{_esc(record.get('rule_type', ''))}</td>"
            f"<td>{_esc(record.get('status', ''))}</td>"
            f"<td>{_esc(record.get('outcome', ''))}</td>"
            f"<td>{_esc(record.get('severity', ''))}</td>"
            f"<td>{_esc(record.get('message', ''))}</td>"
            "</tr>"
        )
    rows.append("</tbody></table>")
    return "\n".join(rows)


def flatten_config(config: dict[str, Any], prefix: str = "") -> dict[str, str]:
    flattened: dict[str, str] = {}
    for key, value in config.items():
        full_key = f"{prefix}.{key}" if prefix else str(key)
        if isinstance(value, dict):
            flattened.update(flatten_config(value, full_key))
        else:
            flattened[full_key] = json.dumps(value, ensure_ascii=False) if isinstance(value, list) else str(value)
    return flattened


def _render_svg(metric_series: dict[str, list[dict[str, Any]]]) -> str:
    labels = ", ".join(_esc(name) for name in metric_series)
    return f'<div class="chart-fallback" role="img" aria-label="Metric curve fallback">Metric curve data: {labels}</div>'


def _to_float(value: Any) -> float | Any:
    try:
        return float(value)
    except (TypeError, ValueError):
        return value


def _to_int_or_text(value: Any) -> int | str | None:
    if value in ("", None):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return str(value)


def _load_metadata(value: str | None) -> dict[str, Any]:
    if not value:
        return {}
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return {}


def _esc(value: Any) -> str:
    return html.escape("" if value is None else str(value))
