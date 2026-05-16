"""Metric summary cache primitives for large project views."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
import csv
import hashlib


@dataclass
class MetricSummary:
    name: str
    count: int = 0
    first_step: int | None = None
    last_step: int | None = None
    min: float | None = None
    max: float | None = None
    last_value: float | None = None
    best: float | None = None
    group: str = "metrics"
    source_mtime: float = 0.0
    source_hash: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def summarize_metrics_csv(path: str | Path, mode_by_metric: dict[str, str] | None = None) -> list[dict[str, Any]]:
    """Return per-metric aggregates without retaining full series rows."""

    metrics_path = Path(path)
    if not metrics_path.exists():
        return []
    source_hash = _file_hash(metrics_path)
    source_mtime = metrics_path.stat().st_mtime
    grouped: dict[str, MetricSummary] = {}
    modes = mode_by_metric or {}
    with metrics_path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            name = str(row.get("name") or "")
            if not name:
                continue
            step = _as_int(row.get("step"))
            value = _as_float(row.get("value"))
            group = str(row.get("group") or "metrics")
            summary = grouped.setdefault(
                name,
                MetricSummary(
                    name=name,
                    group=group,
                    source_mtime=source_mtime,
                    source_hash=source_hash,
                ),
            )
            if group and summary.group == "metrics":
                summary.group = group
            summary.count += 1
            if isinstance(step, int):
                summary.first_step = step if summary.first_step is None else min(summary.first_step, step)
                summary.last_step = step if summary.last_step is None else max(summary.last_step, step)
            if isinstance(value, (int, float)):
                summary.last_value = value
                summary.min = value if summary.min is None else min(summary.min, value)
                summary.max = value if summary.max is None else max(summary.max, value)
                mode = modes.get(name, "max")
                if summary.best is None:
                    summary.best = value
                elif mode == "min":
                    summary.best = min(summary.best, value)
                else:
                    summary.best = max(summary.best, value)
    return [item.to_dict() for item in sorted(grouped.values(), key=lambda item: (item.group, item.name))]


def _file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _as_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _as_int(value: Any) -> int | None:
    try:
        if value in {None, ""}:
            return None
        return int(value)
    except (TypeError, ValueError):
        return None
