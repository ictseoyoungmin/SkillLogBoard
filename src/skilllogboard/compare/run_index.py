"""Run discovery and indexing for multi-run compare reports."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
import csv
import json

import yaml


IGNORED_DIRS = {
    ".git",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
}


@dataclass
class RunRecord:
    """JSON-friendly summary of one run folder.

    The record intentionally stores only values needed by compare views. Full
    source files remain in the run directory and can be loaded by callers when
    a richer single-run dashboard is needed.
    """

    project: str
    run_id: str
    run_name: str
    run_dir: str
    status: str = "unknown"
    created_at: str | None = None
    updated_at: str | None = None
    main_metric: dict[str, Any] | None = None
    best_metric: dict[str, Any] | None = None
    config: dict[str, Any] = field(default_factory=dict)
    metrics: dict[str, dict[str, Any]] = field(default_factory=dict)
    artifact_count: int = 0
    warning_count: int = 0
    error_count: int = 0
    manifest: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def discover_runs(root_dir: str | Path) -> list[Path]:
    """Return deterministic run directories below ``root_dir``.

    Missing roots are treated as empty so CLI commands can print a friendly
    "no runs found" message without a traceback.
    """

    root = Path(root_dir)
    if not root.exists() or not root.is_dir():
        return []

    found: list[Path] = []
    stack = [root]
    while stack:
        current = stack.pop()
        if (current / "manifest.yaml").exists():
            found.append(current)
            continue
        children = [
            child
            for child in current.iterdir()
            if child.is_dir() and child.name not in IGNORED_DIRS and not child.name.startswith(".")
        ]
        stack.extend(sorted(children, reverse=True))
    return sorted(found, key=lambda path: path.as_posix())


def load_run_record(run_dir: str | Path) -> RunRecord:
    run_path = Path(run_dir)
    manifest = _load_yaml(run_path / "manifest.yaml")
    warnings: list[str] = []
    if not manifest:
        warnings.append("manifest.yaml missing or empty")

    config = _load_yaml(run_path / "config.yaml")
    latest_metrics = _read_latest_metrics(run_path / "metrics.csv")
    warning_count, error_count = _summarize_skill_trace(run_path / "skill_trace.jsonl")
    artifact_count = _count_artifacts(run_path / "artifact_index.json")

    run_id = str(manifest.get("run_id") or run_path.name)
    return RunRecord(
        project=str(manifest.get("project") or run_path.parent.name or "unknown"),
        run_id=run_id,
        run_name=str(manifest.get("run_name") or run_id),
        run_dir=str(run_path),
        status=str(manifest.get("status") or "unknown"),
        created_at=manifest.get("created_at"),
        updated_at=manifest.get("updated_at"),
        main_metric=manifest.get("main_metric"),
        best_metric=manifest.get("best_metric"),
        config=config,
        metrics=latest_metrics,
        artifact_count=artifact_count,
        warning_count=warning_count,
        error_count=error_count,
        manifest=manifest,
        warnings=warnings,
    )


def build_run_index(root_dir: str | Path) -> list[dict[str, Any]]:
    return [load_run_record(path).to_dict() for path in discover_runs(root_dir)]


def save_run_index(records: list[RunRecord | dict[str, Any]], path: str | Path) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    data = [record.to_dict() if isinstance(record, RunRecord) else record for record in records]
    out.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    return out


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data if isinstance(data, dict) else {}


def _read_latest_metrics(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    latest: dict[str, dict[str, Any]] = {}
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("name")
            if not name:
                continue
            latest[name] = {
                "name": name,
                "value": _to_float(row.get("value")),
                "step": _to_int(row.get("step")),
                "metadata_json": row.get("metadata_json", ""),
            }
    return latest


def _summarize_skill_trace(path: Path) -> tuple[int, int]:
    if not path.exists():
        return 0, 0
    warning_count = 0
    error_count = 0
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            outcome = str(record.get("outcome", "")).lower()
            if outcome == "warning":
                warning_count += 1
            if outcome == "error":
                error_count += 1
    return warning_count, error_count


def _count_artifacts(path: Path) -> int:
    if not path.exists():
        return 0
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return 0
    artifacts = data.get("artifacts", [])
    return len(artifacts) if isinstance(artifacts, list) else 0


def _to_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _to_int(value: Any) -> int | None:
    if value in (None, ""):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
