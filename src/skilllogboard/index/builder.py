"""Project index builder."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from skilllogboard.index.metrics import summarize_metrics_csv
from skilllogboard.index.schema import DEFAULT_INDEX_PATH, ProjectIndex, ProjectIndexRun, write_project_index
from skilllogboard.live.project import find_run_dirs
from skilllogboard.live.readers import read_artifact_count, read_manifest


def build_project_index(root_dir: str | Path, latest: bool = False) -> ProjectIndex:
    """Build a derived summary-first index from manifests and metric summaries."""

    root = Path(root_dir)
    discovered = find_run_dirs(root)
    run_dirs = [path.parent if path.name == "manifest.yaml" else path for path in discovered]
    if latest and run_dirs:
        run_dirs = [max(run_dirs, key=lambda path: path.stat().st_mtime)]

    runs: list[ProjectIndexRun] = []
    warnings: list[str] = []
    for run_dir in run_dirs:
        manifest, manifest_warnings = read_manifest(run_dir)
        artifact_count, artifact_warnings = read_artifact_count(run_dir)
        metric_modes = _metric_modes(manifest)
        metric_summaries = summarize_metrics_csv(run_dir / "metrics.csv", metric_modes)
        warning_count = len(manifest_warnings) + len(artifact_warnings)
        warnings.extend(f"{run_dir.name}: {warning}" for warning in manifest_warnings + artifact_warnings)
        run_id = str(manifest.get("run_id") or run_dir.name)
        runs.append(
            ProjectIndexRun(
                run_id=run_id,
                path=str(run_dir),
                status=str(manifest.get("status") or "unknown"),
                started_at=str(manifest.get("started_at") or manifest.get("created_at") or ""),
                updated_at=_updated_at(run_dir, manifest),
                duration=_duration(manifest),
                key_metrics=_key_metrics(manifest, metric_summaries),
                metric_summaries=metric_summaries,
                tags=[str(item) for item in manifest.get("tags") or []],
                group=str(manifest.get("group") or ""),
                baseline=bool(manifest.get("baseline")),
                artifact_count=artifact_count,
                warning_count=warning_count,
                fingerprint=_fingerprint(run_dir),
            )
        )
    runs.sort(key=lambda run: (-run.updated_at, run.run_id))
    return ProjectIndex(
        root_dir=str(root),
        generated_at=datetime.now(timezone.utc).isoformat(),
        runs=runs,
        warnings=warnings,
    )


def rebuild_project_index(
    root_dir: str | Path,
    output_path: str | Path | None = None,
    dry_run: bool = False,
    latest: bool = False,
) -> tuple[ProjectIndex, Path]:
    index = build_project_index(root_dir, latest=latest)
    out = Path(output_path) if output_path else Path(root_dir) / DEFAULT_INDEX_PATH
    if not dry_run:
        write_project_index(index, out)
    return index, out


def _metric_modes(manifest: dict[str, Any]) -> dict[str, str]:
    modes: dict[str, str] = {}
    for key in ("main_metric", "best_metric"):
        item = manifest.get(key)
        if isinstance(item, dict) and item.get("name"):
            modes[str(item["name"])] = str(item.get("mode") or "max")
    return modes


def _key_metrics(manifest: dict[str, Any], metric_summaries: list[dict[str, Any]]) -> dict[str, Any]:
    best = manifest.get("best_metric")
    if isinstance(best, dict) and best.get("name"):
        return {str(best["name"]): best.get("value", best.get("best_value"))}
    return {
        str(item["name"]): item.get("last_value")
        for item in metric_summaries[:5]
        if item.get("name") and item.get("last_value") is not None
    }


def _updated_at(run_dir: Path, manifest: dict[str, Any]) -> float:
    value = manifest.get("updated_at") or manifest.get("finished_at")
    if isinstance(value, (int, float)):
        return float(value)
    return run_dir.stat().st_mtime if run_dir.exists() else 0.0


def _duration(manifest: dict[str, Any]) -> float | None:
    value = manifest.get("duration") or manifest.get("duration_seconds")
    return float(value) if isinstance(value, (int, float)) else None


def _fingerprint(run_dir: Path) -> dict[str, Any]:
    files = ["manifest.yaml", "metrics.csv", "artifact_index.json", "agent/actions.jsonl"]
    result: dict[str, Any] = {}
    for name in files:
        path = run_dir / name
        if path.exists():
            stat = path.stat()
            result[name] = {"mtime": stat.st_mtime, "size": stat.st_size}
    return result
