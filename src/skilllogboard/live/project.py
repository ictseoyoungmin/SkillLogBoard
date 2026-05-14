"""Project-level live board state."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import os

from skilllogboard.live.readers import read_metrics
from skilllogboard.live.state import build_live_run_state

DEFAULT_MAX_DISCOVERY_DEPTH = 4
DEFAULT_COMPARE_MAX_RUNS = 6
DEFAULT_COMPARE_MAX_POINTS = 240
DEFAULT_EXCLUDE_DIRS = {
    ".git",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "_reports",
    "artifacts",
    "build",
    "dist",
    "htmlcov",
    "node_modules",
    "report",
    "reports",
}


def find_run_dirs(
    root_dir: str | Path,
    max_depth: int = DEFAULT_MAX_DISCOVERY_DEPTH,
    exclude_dirs: set[str] | None = None,
) -> list[Path]:
    root = Path(root_dir)
    if (root / "manifest.yaml").exists():
        return [root]
    excludes = DEFAULT_EXCLUDE_DIRS if exclude_dirs is None else exclude_dirs
    manifests: list[Path] = []
    for current_root, dirnames, filenames in os.walk(root):
        current = Path(current_root)
        rel = current.relative_to(root)
        depth = 0 if rel == Path(".") else len(rel.parts)
        dirnames[:] = [
            name
            for name in dirnames
            if name not in excludes and not name.startswith(".") and depth < max_depth
        ]
        if "manifest.yaml" in filenames:
            manifests.append(current / "manifest.yaml")
    return sorted(manifests)


def build_live_project_state(root_dir: str | Path, latest: bool = False) -> dict[str, Any]:
    root = Path(root_dir)
    manifests = find_run_dirs(root)
    run_dirs = [path.parent if path.name == "manifest.yaml" else path for path in manifests]
    if latest and run_dirs:
        run_dirs = [max(run_dirs, key=lambda p: p.stat().st_mtime)]

    runs = []
    counts: dict[str, int] = {}
    warnings: list[str] = []
    for run_dir in run_dirs:
        state = build_live_run_state(run_dir)
        status = state.status
        counts[status] = counts.get(status, 0) + 1
        warnings.extend(f"{run_dir.name}: {warning}" for warning in state.warnings)
        runs.append(
            {
                "run_dir": str(run_dir),
                "run_id": state.manifest.get("run_id", run_dir.name),
                "run_name": state.manifest.get("run_name", run_dir.name),
                "project": state.manifest.get("project", ""),
                "status": status,
                "metrics": state.metrics,
                "metric_catalog": state.metric_catalog,
                "main_metric": state.manifest.get("main_metric"),
                "best_metric": state.manifest.get("best_metric"),
                "warnings": state.warnings,
                "capabilities": state.capabilities,
            }
        )
    metric_catalog = _project_metric_catalog(runs)
    compare = build_compare_state(root, latest=latest)
    capabilities = _project_capabilities(
        runs=runs,
        metric_catalog=metric_catalog,
        compare=compare,
        warnings=warnings,
        status_counts=counts,
    )
    return {
        "mode": "project",
        "root_dir": str(root),
        "runs": runs,
        "status_counts": counts,
        "alerts": warnings[-20:],
        "leaderboard": _leaderboard_lite(runs),
        "metric_catalog": metric_catalog,
        "selected_metrics": [metric_catalog[0]["name"]] if metric_catalog else [],
        "compare": compare,
        "compare_candidates": compare["runs"],
        "shared_metrics": compare["shared_metrics"],
        "warnings": warnings,
        "capabilities": capabilities,
    }


def build_compare_state(
    root_dir: str | Path,
    metric: str | None = None,
    selected_run_ids: list[str] | None = None,
    max_runs: int = DEFAULT_COMPARE_MAX_RUNS,
    max_points: int = DEFAULT_COMPARE_MAX_POINTS,
    normalize: bool = False,
    align: str = "step",
    latest: bool = False,
) -> dict[str, Any]:
    """Build a bounded project compare payload without pandas, databases, or caches."""

    root = Path(root_dir)
    manifests = find_run_dirs(root)
    run_dirs = [path.parent if path.name == "manifest.yaml" else path for path in manifests]
    if latest and run_dirs:
        run_dirs = [max(run_dirs, key=lambda p: p.stat().st_mtime)]

    run_records = [_read_compare_run(run_dir) for run_dir in run_dirs]
    shared_metrics = _shared_metric_names(run_records)
    selected_metric = metric or (shared_metrics[0] if shared_metrics else None)
    candidates = _compare_candidates(run_records, selected_metric)
    selected_ids = [item for item in (selected_run_ids or []) if item]
    ordered_ids = selected_ids or [run["run_id"] for run in candidates[:max_runs]]
    selected_runs = [run for run in candidates if run["run_id"] in ordered_ids][: max(1, max_runs)]
    safe_align = align if align in {"step", "relative"} else "step"
    warnings: list[str] = []
    if not selected_metric:
        warnings.append("no shared numeric metrics found for compare")

    series = []
    for run in selected_runs:
        rows = run["metric_rows"].get(selected_metric or "", [])
        if selected_metric and not rows:
            warnings.append(f"{run['run_id']}: missing metric {selected_metric}")
        points = _compare_points(
            rows,
            max_points=max_points,
            normalize=normalize,
            align=safe_align,
        )
        series.append(
            {
                "run_id": run["run_id"],
                "run_name": run["run_name"],
                "status": run["status"],
                "role": run["role"],
                "roles": run["roles"],
                "metric": selected_metric,
                "visible": True,
                "points": points,
                "point_count": len(points),
            }
        )

    return {
        "metric": selected_metric,
        "align": safe_align,
        "normalize": bool(normalize),
        "bounds": {"max_runs": max_runs, "max_points": max_points},
        "runs": [_public_compare_run(run) for run in candidates],
        "selected_run_ids": [run["run_id"] for run in selected_runs],
        "shared_metrics": shared_metrics,
        "series": series,
        "warnings": warnings,
    }


def _leaderboard_lite(runs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for run in runs:
        best = run.get("best_metric") or {}
        if isinstance(best, dict) and best.get("name"):
            value = best.get("value", best.get("best_value"))
            step = best.get("step", best.get("best_step"))
            rows.append(
                {
                    "run_id": run.get("run_id"),
                    "metric": best.get("name"),
                    "value": value,
                    "step": step,
                    "status": run.get("status"),
                }
            )
    rows.sort(key=lambda item: item["value"] if isinstance(item["value"], (int, float)) else 0, reverse=True)
    return rows


def _project_metric_catalog(runs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    for run in runs:
        for metric in run.get("metric_catalog") or []:
            name = str(metric.get("name") or "")
            if not name:
                continue
            item = grouped.setdefault(
                name,
                {
                    "name": name,
                    "group": metric.get("group") or "metrics",
                    "count": 0,
                    "run_count": 0,
                    "latest": None,
                    "min": None,
                    "max": None,
                    "pinned": False,
                },
            )
            values = [metric.get("min"), metric.get("max"), metric.get("latest")]
            numeric = [value for value in values if isinstance(value, (int, float))]
            item["count"] += int(metric.get("count") or 0)
            item["run_count"] += 1
            item["latest"] = metric.get("latest")
            item["pinned"] = bool(item["pinned"] or metric.get("pinned"))
            if numeric:
                item["min"] = min(numeric) if item["min"] is None else min(item["min"], *numeric)
                item["max"] = max(numeric) if item["max"] is None else max(item["max"], *numeric)
    return sorted(grouped.values(), key=lambda item: (not item["pinned"], item["group"], item["name"]))


def _project_capabilities(
    runs: list[dict[str, Any]],
    metric_catalog: list[dict[str, Any]],
    compare: dict[str, Any],
    warnings: list[str],
    status_counts: dict[str, int],
) -> dict[str, Any]:
    run_caps = [run.get("capabilities") or {} for run in runs]
    artifact_count = sum(int(cap.get("artifact_count") or 0) for cap in run_caps)
    report_artifact_count = sum(int(cap.get("report_artifact_count") or 0) for cap in run_caps)
    rule_count = sum(int(cap.get("rule_count") or 0) for cap in run_caps)
    event_count = sum(int(cap.get("event_count") or 0) for cap in run_caps)
    agent_count = sum(1 for cap in run_caps if cap.get("agent_evidence"))
    shared_metric_count = len(compare.get("shared_metrics") or [])
    return {
        "mode": "project",
        "run_count": len(runs),
        "metric_count": len(metric_catalog),
        "shared_metric_count": shared_metric_count,
        "event_count": event_count,
        "rule_count": rule_count,
        "artifact_count": artifact_count,
        "report_artifact_count": report_artifact_count,
        "warning_count": len(warnings),
        "agent_evidence": agent_count > 0,
        "agent_run_count": agent_count,
        "compare_ready": len(runs) >= 2 and shared_metric_count > 0,
        "completed_count": int(status_counts.get("completed") or 0),
        "running_count": int(status_counts.get("running") or 0),
        "failed_count": int(status_counts.get("failed") or 0),
    }


def _read_compare_run(run_dir: Path) -> dict[str, Any]:
    state = build_live_run_state(run_dir)
    rows, latest_metrics, warnings = read_metrics(run_dir)
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        if isinstance(row.get("value"), (int, float)) and row.get("name"):
            grouped.setdefault(str(row["name"]), []).append(row)
    run_id = str(state.manifest.get("run_id") or run_dir.name)
    best_metric = state.manifest.get("best_metric")
    mtime = run_dir.stat().st_mtime if run_dir.exists() else 0
    return {
        "run_dir": str(run_dir),
        "run_id": run_id,
        "run_name": str(state.manifest.get("run_name") or run_id),
        "status": str(state.manifest.get("status") or "unknown"),
        "project": str(state.manifest.get("project") or ""),
        "metric_rows": grouped,
        "metric_names": set(grouped),
        "latest_metrics": latest_metrics,
        "best_metric": best_metric if isinstance(best_metric, dict) else {},
        "mtime": mtime,
        "warnings": warnings,
        "role": "candidate",
        "roles": [],
    }


def _shared_metric_names(runs: list[dict[str, Any]]) -> list[str]:
    metric_sets = [run["metric_names"] for run in runs if run["metric_names"]]
    if not metric_sets:
        return []
    shared = set.intersection(*metric_sets) if len(metric_sets) > 1 else set(metric_sets[0])
    if not shared:
        shared = set.union(*metric_sets)
    return sorted(shared)


def _compare_candidates(runs: list[dict[str, Any]], metric: str | None) -> list[dict[str, Any]]:
    candidates = sorted(runs, key=lambda run: (-run["mtime"], run["run_id"]))
    if not candidates:
        return []
    latest = candidates[0]
    best = _best_run_for_metric(candidates, metric)
    baseline = _baseline_run(candidates)
    for run in candidates:
        roles = []
        if run is best:
            roles.append("best")
        if run is latest:
            roles.append("latest")
        if run is baseline:
            roles.append("baseline")
        run["roles"] = roles or ["candidate"]
        run["role"] = roles[0] if roles else "candidate"
    return sorted(
        candidates,
        key=lambda run: (0 if run["role"] != "candidate" else 1, -run["mtime"], run["run_id"]),
    )


def _best_run_for_metric(runs: list[dict[str, Any]], metric: str | None) -> dict[str, Any] | None:
    scored = []
    for run in runs:
        rows = run["metric_rows"].get(metric or "", [])
        values = [row.get("value") for row in rows if isinstance(row.get("value"), (int, float))]
        best_metric = run.get("best_metric") or {}
        if (
            isinstance(best_metric, dict)
            and best_metric.get("name") == metric
            and isinstance(best_metric.get("value"), (int, float))
        ):
            values.append(best_metric["value"])
        if values:
            scored.append((max(values), run["mtime"], run))
    return max(scored, key=lambda item: (item[0], item[1]))[2] if scored else (runs[0] if runs else None)


def _baseline_run(runs: list[dict[str, Any]]) -> dict[str, Any] | None:
    for run in runs:
        text = f"{run['run_id']} {run['run_name']}".lower()
        if "baseline" in text:
            return run
    return sorted(runs, key=lambda run: (run["mtime"], run["run_id"]))[0] if runs else None


def _compare_points(
    rows: list[dict[str, Any]],
    max_points: int,
    normalize: bool,
    align: str,
) -> list[dict[str, Any]]:
    bounded = _bounded_rows(rows, max_points=max_points)
    values = [row["value"] for row in bounded if isinstance(row.get("value"), (int, float))]
    v_min = min(values) if values else 0
    v_max = max(values) if values else 1
    first_step = bounded[0].get("step") if bounded else 0
    points = []
    for index, row in enumerate(bounded):
        step = row.get("step")
        raw_value = row.get("value")
        value = raw_value
        if normalize and isinstance(raw_value, (int, float)):
            value = 0.0 if v_max == v_min else (raw_value - v_min) / (v_max - v_min)
        x = index if step is None else step
        if align == "relative":
            x = index if step is None else step - (first_step or 0)
        points.append({"step": step, "x": x, "value": value, "raw_value": raw_value})
    return points


def _bounded_rows(rows: list[dict[str, Any]], max_points: int) -> list[dict[str, Any]]:
    if max_points <= 0 or len(rows) <= max_points:
        return rows
    stride = max(1, len(rows) // max_points)
    bounded = rows[::stride][:max_points]
    if bounded and bounded[-1] is not rows[-1]:
        bounded[-1] = rows[-1]
    return bounded


def _public_compare_run(run: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_dir": run["run_dir"],
        "run_id": run["run_id"],
        "run_name": run["run_name"],
        "status": run["status"],
        "project": run["project"],
        "role": run["role"],
        "roles": run["roles"],
        "metrics": sorted(run["metric_names"]),
        "mtime": run["mtime"],
    }
