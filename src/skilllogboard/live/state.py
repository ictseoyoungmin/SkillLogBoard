"""Live Board state aggregation."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from skilllogboard.live.monitoring import read_monitoring_records
from skilllogboard.live.readers import (
    read_artifacts,
    read_events,
    read_manifest,
    read_metrics,
    read_rule_trace,
    tail_log_file,
)


@dataclass
class LiveRunState:
    mode: str
    run_dir: str
    status: str = "unknown"
    manifest: dict[str, Any] = field(default_factory=dict)
    metrics: dict[str, Any] = field(default_factory=dict)
    metric_series: list[dict[str, Any]] = field(default_factory=list)
    events: list[dict[str, Any]] = field(default_factory=list)
    rules: list[dict[str, Any]] = field(default_factory=list)
    artifacts: list[dict[str, Any]] = field(default_factory=list)
    monitoring: list[dict[str, Any]] = field(default_factory=list)
    logs: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metric_catalog: list[dict[str, Any]] = field(default_factory=list)
    selected_metrics: list[str] = field(default_factory=list)
    pinned_metrics: list[str] = field(default_factory=list)
    context_markers: list[dict[str, Any]] = field(default_factory=list)
    report_artifacts: list[dict[str, Any]] = field(default_factory=list)
    artifact_groups: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    agent_workspace: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_empty_live_run_state(run_dir: str | Path) -> LiveRunState:
    return LiveRunState(mode="run", run_dir=str(Path(run_dir)))


def build_live_run_state(
    run_dir: str | Path,
    limits: dict[str, int] | None = None,
    log_file: str | Path | None = None,
) -> LiveRunState:
    limits = limits or {}
    run = Path(run_dir)
    warnings: list[str] = []
    manifest, manifest_warnings = read_manifest(run)
    warnings.extend(manifest_warnings)
    metric_series, latest_metrics, metric_warnings = read_metrics(run)
    warnings.extend(metric_warnings)
    events, event_warnings = read_events(run, limit=limits.get("events", 200))
    warnings.extend(event_warnings)
    rules, rule_warnings = read_rule_trace(run, limit=limits.get("rules", 200))
    warnings.extend(rule_warnings)
    artifacts, artifact_warnings = read_artifacts(run, limit=limits.get("artifacts", 50))
    warnings.extend(artifact_warnings)
    logs, log_warnings = tail_log_file(log_file, limit=limits.get("logs", 100))
    warnings.extend(log_warnings)
    monitoring = read_monitoring_records(run, limit=limits.get("monitoring", 200))
    metric_catalog = build_metric_catalog(metric_series, manifest)
    selected_metrics = [metric_catalog[0]["name"]] if metric_catalog else []
    manifest_pins = {
        entry.get("name") for entry in manifest.get("pins", []) if isinstance(entry, dict)
    }
    pinned_metrics = [
        item["name"] for item in metric_catalog if item.get("pinned") or item["name"] in manifest_pins
    ]
    if not pinned_metrics and selected_metrics:
        pinned_metrics = selected_metrics[:1]
    context_markers = build_context_markers(events, rules, artifacts)

    report_artifacts = read_report_artifacts(run)
    return LiveRunState(
        mode="run",
        run_dir=str(run),
        status=str(manifest.get("status", "unknown")),
        manifest=manifest,
        metrics=latest_metrics,
        metric_series=metric_series,
        events=events,
        rules=rules,
        artifacts=artifacts,
        monitoring=monitoring,
        logs=logs,
        warnings=warnings,
        metric_catalog=metric_catalog,
        selected_metrics=selected_metrics,
        pinned_metrics=pinned_metrics,
        context_markers=context_markers,
        report_artifacts=report_artifacts,
        artifact_groups=group_report_artifacts(report_artifacts),
        agent_workspace=read_agent_workspace(run),
    )


def build_metric_catalog(
    metric_series: list[dict[str, Any]], manifest: dict[str, Any]
) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in metric_series:
        name = str(row.get("name") or "")
        if name:
            grouped.setdefault(name, []).append(row)
    main_metric = manifest.get("main_metric") or {}
    main_name = main_metric.get("name") if isinstance(main_metric, dict) else None
    catalog = []
    for name, rows in sorted(grouped.items()):
        values = [row.get("value") for row in rows if isinstance(row.get("value"), (int, float))]
        steps = [row.get("step") for row in rows if isinstance(row.get("step"), int)]
        latest = rows[-1] if rows else {}
        inferred_group = name.split("/", 1)[0] if "/" in name else "metrics"
        group = str(latest.get("group") or inferred_group)
        catalog.append(
            {
                "name": name,
                "group": group,
                "count": len(rows),
                "latest": latest.get("value"),
                "min": min(values) if values else None,
                "max": max(values) if values else None,
                "first_step": min(steps) if steps else None,
                "last_step": max(steps) if steps else None,
                "pinned": name == main_name,
            }
        )
    catalog.sort(key=lambda item: (not item["pinned"], item["group"], item["name"]))
    return catalog


def build_context_markers(
    events: list[dict[str, Any]], rules: list[dict[str, Any]], artifacts: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    markers: list[dict[str, Any]] = []
    for event in events:
        markers.append(
            {
                "type": event.get("type", "event"),
                "source": "event",
                "severity": event.get("severity", "info"),
                "step": event.get("step"),
                "label": event.get("message") or event.get("key") or event.get("type", "event"),
            }
        )
    for rule in rules:
        outcome = str(rule.get("outcome") or rule.get("severity") or "rule")
        markers.append(
            {
                "type": "rule",
                "source": "rule",
                "severity": outcome,
                "step": rule.get("step"),
                "label": rule.get("rule_id") or rule.get("type") or "rule",
            }
        )
    for artifact in artifacts:
        markers.append(
            {
                "type": "artifact",
                "source": "artifact",
                "severity": "info",
                "step": artifact.get("step"),
                "label": artifact.get("name") or artifact.get("path") or "artifact",
            }
        )
    return markers[-200:]


def read_report_artifacts(run_dir: Path) -> list[dict[str, Any]]:
    candidates = [
        ("dashboard", run_dir / "dashboard.html"),
        ("summary", run_dir / "summary.md"),
        ("report", run_dir / "report.md"),
        ("report-html", run_dir / "report.html"),
        ("report-manifest", run_dir / "report_manifest.yaml"),
    ]
    artifacts = [
        _report_artifact_record(kind, path, run_dir)
        for kind, path in candidates
        if path.exists() and path.is_file()
    ]
    for folder in ["report", "reports", "tables", "figures"]:
        root = run_dir / folder
        if root.exists() and root.is_dir():
            for path in sorted(root.rglob("*")):
                if path.is_file():
                    artifacts.append(
                        _report_artifact_record(_infer_report_artifact_type(path), path, run_dir)
                    )
    deduped: dict[str, dict[str, Any]] = {}
    for item in artifacts:
        deduped[item["path"]] = item
    return sorted(deduped.values(), key=lambda item: (item["type"], item["path"]))[:200]


def group_report_artifacts(artifacts: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for artifact in artifacts:
        groups.setdefault(str(artifact.get("type") or "artifact"), []).append(artifact)
    return groups


def read_agent_workspace(run_dir: Path) -> dict[str, Any]:
    agent_dir = run_dir / "agent"
    actions, _ = read_jsonl_if_exists(agent_dir / "actions.jsonl")
    latest = actions[-1] if actions else {}
    return {
        "actions_count": len(actions),
        "latest_action": latest,
        "latest_status": latest.get("status") or latest.get("outcome") or "",
        "latest_target": latest.get("target") or latest.get("task") or "",
        "files_changed": latest.get("files_changed") or latest.get("files") or [],
        "handoff": (agent_dir / "handoff.md").exists(),
        "decisions": (agent_dir / "decisions.md").exists(),
    }


def _report_artifact_record(kind: str, path: Path, run_dir: Path) -> dict[str, Any]:
    stat = path.stat()
    return {
        "type": kind,
        "name": path.name,
        "path": path.relative_to(run_dir).as_posix(),
        "size": stat.st_size,
        "modified": int(stat.st_mtime),
        "preview": "metadata",
    }


def _infer_report_artifact_type(path: Path) -> str:
    parent_names = {part.lower() for part in path.parts}
    suffix = path.suffix.lower()
    if "tables" in parent_names or suffix in {".csv", ".tsv"}:
        return "table"
    if "figures" in parent_names or suffix in {".png", ".jpg", ".jpeg", ".svg", ".webp"}:
        return "figure"
    if suffix in {".html", ".md", ".yaml", ".yml", ".json"}:
        return "report"
    return "artifact"


def read_jsonl_if_exists(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    if not path.exists():
        return [], []
    from skilllogboard.live.readers import read_jsonl

    return read_jsonl(path, limit=200)
