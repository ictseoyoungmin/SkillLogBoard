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
    )
