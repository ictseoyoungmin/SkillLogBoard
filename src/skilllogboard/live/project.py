"""Project-level live board state."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from concurrent.futures import ThreadPoolExecutor
import json
import os

from skilllogboard.live.downsample import downsample_points
from skilllogboard.live.readers import read_manifest, read_metric_summary, read_metrics
from skilllogboard.query import filter_runs

DEFAULT_MAX_DISCOVERY_DEPTH = 4
DEFAULT_COMPARE_MAX_RUNS = 6
DEFAULT_COMPARE_MAX_POINTS = 240
COMPARE_MAX_RUNS_LIMIT = 25
COMPARE_MAX_POINTS_LIMIT = 2000
DEFAULT_PROJECT_RUN_LIMIT = 500
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

SUMMARY_FIRST_VIEWS = {"overview", "runs", "artifacts", "reports", "agent", "settings"}
SERIES_VIEWS = {"compare", "lab", "metric-lab"}
_RUN_SUMMARY_CACHE: dict[str, tuple[tuple[float, ...], dict[str, Any]]] = {}


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


def build_live_project_state(
    root_dir: str | Path,
    latest: bool = False,
    view: str | None = None,
) -> dict[str, Any]:
    root = Path(root_dir)
    manifests = find_run_dirs(root)
    run_dirs = [path.parent if path.name == "manifest.yaml" else path for path in manifests]
    if latest and run_dirs:
        run_dirs = [max(run_dirs, key=lambda p: p.stat().st_mtime)]

    runs = []
    counts: dict[str, int] = {}
    warnings: list[str] = []
    max_workers = min(16, max(1, len(run_dirs)))
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        run_states = list(executor.map(_read_project_run_summary, run_dirs))
    for run_dir, state in zip(run_dirs, run_states):
        status = state["status"]
        counts[status] = counts.get(status, 0) + 1
        warnings.extend(f"{run_dir.name}: {warning}" for warning in state["warnings"])
        runs.append(state)
    metric_catalog = _project_metric_catalog(runs)
    selected_view = _normalized_view(view)
    shared_metrics = _shared_summary_metric_names(runs)
    compare = (
        build_compare_state(root, latest=latest)
        if selected_view in SERIES_VIEWS or selected_view == "state"
        else _compare_summary(runs, shared_metrics)
    )
    capabilities = _project_capabilities(
        runs=runs,
        metric_catalog=metric_catalog,
        compare=compare,
        warnings=warnings,
        status_counts=counts,
    )
    return {
        "mode": "project",
        "current_view": "overview" if selected_view == "state" else selected_view,
        "payload_scope": "series" if selected_view in SERIES_VIEWS or selected_view == "state" else "summary",
        "root_dir": str(root),
        "runs": runs[:DEFAULT_PROJECT_RUN_LIMIT],
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
    filters: str | None = None,
) -> dict[str, Any]:
    """Build a bounded project compare payload without pandas, databases, or caches."""

    root = Path(root_dir)
    safe_max_runs = min(max(1, int(max_runs or DEFAULT_COMPARE_MAX_RUNS)), COMPARE_MAX_RUNS_LIMIT)
    safe_max_points = min(max(1, int(max_points or DEFAULT_COMPARE_MAX_POINTS)), COMPARE_MAX_POINTS_LIMIT)
    manifests = find_run_dirs(root)
    run_dirs = [path.parent if path.name == "manifest.yaml" else path for path in manifests]
    if latest and run_dirs:
        run_dirs = [max(run_dirs, key=lambda p: p.stat().st_mtime)]

    run_records = [_read_compare_run(run_dir) for run_dir in run_dirs]
    run_records, parsed_filters = filter_runs(run_records, filters)
    shared_metrics = _shared_metric_names(run_records)
    selected_metric = metric or (shared_metrics[0] if shared_metrics else None)
    candidates = _compare_candidates(run_records, selected_metric)
    selected_ids = [item for item in (selected_run_ids or []) if item]
    ordered_ids = selected_ids or [run["run_id"] for run in candidates[:safe_max_runs]]
    selected_runs = [run for run in candidates if run["run_id"] in ordered_ids][:safe_max_runs]
    safe_align = align if align in {"step", "relative"} else "step"
    warnings: list[str] = []
    warnings.extend(error.message for error in parsed_filters.errors)
    if not selected_metric:
        warnings.append("no shared numeric metrics found for compare")

    series = []
    baseline_value = _baseline_value(selected_runs, selected_metric)
    for run in selected_runs:
        rows = run["metric_rows"].get(selected_metric or "", [])
        if selected_metric and not rows:
            warnings.append(f"{run['run_id']}: missing metric {selected_metric}")
        points, downsampling = _compare_points(
            rows,
            max_points=safe_max_points,
            normalize=normalize,
            align=safe_align,
        )
        last_raw = points[-1].get("raw_value") if points else None
        delta = (
            float(last_raw) - baseline_value
            if isinstance(last_raw, (int, float)) and isinstance(baseline_value, (int, float))
            else None
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
                "downsampling": downsampling,
                "delta_from_baseline": delta,
            }
        )

    return {
        "metric": selected_metric,
        "align": safe_align,
        "normalize": bool(normalize),
        "bounds": {"max_runs": safe_max_runs, "max_points": safe_max_points},
        "runs": [_public_compare_run(run) for run in candidates],
        "selected_run_ids": [run["run_id"] for run in selected_runs],
        "shared_metrics": shared_metrics,
        "series": series,
        "filter": parsed_filters.to_dict(),
        "baseline_value": baseline_value,
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


def _read_project_run_summary(run_dir: Path) -> dict[str, Any]:
    fingerprint = _run_summary_fingerprint(run_dir)
    cache_key = str(run_dir.resolve())
    cached = _RUN_SUMMARY_CACHE.get(cache_key)
    if cached and cached[0] == fingerprint:
        return dict(cached[1])

    manifest, manifest_warnings = read_manifest(run_dir)
    metric_catalog, latest_metrics, metric_warnings = read_metric_summary(run_dir)
    main_metric = manifest.get("main_metric") if isinstance(manifest.get("main_metric"), dict) else {}
    main_name = main_metric.get("name") if isinstance(main_metric, dict) else None
    for metric in metric_catalog:
        metric["pinned"] = metric.get("name") == main_name
    artifact_count, artifact_warnings = _quick_artifact_count(run_dir)
    report_artifact_count = _quick_report_artifact_count(run_dir)
    agent_evidence = _quick_agent_evidence(run_dir)
    warnings = manifest_warnings + metric_warnings + artifact_warnings
    status = str(manifest.get("status", "unknown"))
    run_id = str(manifest.get("run_id") or run_dir.name)
    caps = {
        "mode": "run",
        "run_count": 1,
        "metric_count": len(metric_catalog),
        "shared_metric_count": 0,
        "event_count": 0,
        "rule_count": 0,
        "artifact_count": artifact_count + report_artifact_count,
        "report_artifact_count": report_artifact_count,
        "warning_count": len(warnings),
        "agent_evidence": agent_evidence,
        "compare_ready": False,
    }
    summary = {
        "run_dir": str(run_dir),
        "run_id": run_id,
        "run_name": str(manifest.get("run_name") or run_id),
        "project": str(manifest.get("project") or ""),
        "status": status,
        "metrics": latest_metrics,
        "metric_catalog": metric_catalog,
        "main_metric": main_metric,
        "best_metric": manifest.get("best_metric"),
        "tags": manifest.get("tags") or [],
        "group": manifest.get("group") or "",
        "baseline": manifest.get("baseline") or False,
        "branch": (manifest.get("git") or {}).get("branch") if isinstance(manifest.get("git"), dict) else "",
        "updated": int(run_dir.stat().st_mtime) if run_dir.exists() else 0,
        "artifact_count": caps["artifact_count"],
        "report_artifact_count": caps["report_artifact_count"],
        "agent_evidence": caps["agent_evidence"],
        "warnings": warnings,
        "warning_count": len(warnings),
        "capabilities": caps,
    }
    _RUN_SUMMARY_CACHE[cache_key] = (fingerprint, summary)
    return dict(summary)


def _run_summary_fingerprint(run_dir: Path) -> tuple[float, ...]:
    paths = [
        run_dir / "manifest.yaml",
        run_dir / "metrics.csv",
        run_dir / "artifact_index.json",
        run_dir / "agent" / "actions.jsonl",
    ]
    return tuple(path.stat().st_mtime if path.exists() else 0.0 for path in paths)


def _quick_artifact_count(run_dir: Path) -> tuple[int, list[str]]:
    index_path = run_dir / "artifact_index.json"
    if index_path.exists():
        try:
            data = json.loads(index_path.read_text(encoding="utf-8"))
        except Exception as exc:
            return 0, [f"could not read {index_path.name}: {exc}"]
        artifacts = data.get("artifacts", []) if isinstance(data, dict) else []
        return len([item for item in artifacts if isinstance(item, dict)]), []
    artifacts_dir = run_dir / "artifacts"
    if artifacts_dir.exists() and artifacts_dir.is_dir():
        return sum(1 for item in artifacts_dir.iterdir() if item.is_file()), []
    return 0, ["missing artifact_index.json"]


def _quick_report_artifact_count(run_dir: Path) -> int:
    count = 0
    for name in ["dashboard.html", "summary.md", "report.md", "report.html", "report_manifest.yaml"]:
        path = run_dir / name
        if path.exists() and path.is_file():
            count += 1
    report_manifest = run_dir / "report" / "report_manifest.yaml"
    if report_manifest.exists() and report_manifest.is_file():
        count += 1
    return count


def _quick_agent_evidence(run_dir: Path) -> bool:
    agent_dir = run_dir / "agent"
    return any(
        path.exists() and (path.stat().st_size > 0 if path.is_file() else True)
        for path in [
            agent_dir / "actions.jsonl",
            agent_dir / "handoff.md",
            agent_dir / "handoff.json",
            agent_dir / "decisions.md",
        ]
    )


def _normalized_view(view: str | None) -> str:
    if not view:
        return "state"
    value = str(view).strip().lower()
    return value if value else "state"


def _shared_summary_metric_names(runs: list[dict[str, Any]]) -> list[str]:
    metric_sets = []
    for run in runs:
        names = {metric["name"] for metric in run.get("metric_catalog") or [] if metric.get("name")}
        if names:
            metric_sets.append(names)
    if not metric_sets:
        return []
    shared = set.intersection(*metric_sets) if len(metric_sets) > 1 else set(metric_sets[0])
    if not shared:
        shared = set.union(*metric_sets)
    return sorted(shared)


def _compare_summary(runs: list[dict[str, Any]], shared_metrics: list[str]) -> dict[str, Any]:
    metric = shared_metrics[0] if shared_metrics else None
    candidates = _summary_compare_candidates(runs, metric)
    selected = candidates[:DEFAULT_COMPARE_MAX_RUNS]
    warnings = [] if metric else ["no shared numeric metrics found for compare"]
    return {
        "metric": metric,
        "align": "step",
        "normalize": False,
        "bounds": {"max_runs": DEFAULT_COMPARE_MAX_RUNS, "max_points": DEFAULT_COMPARE_MAX_POINTS},
        "runs": candidates,
        "selected_run_ids": [run["run_id"] for run in selected],
        "shared_metrics": shared_metrics,
        "series": [],
        "warnings": warnings,
    }


def _summary_compare_candidates(runs: list[dict[str, Any]], metric: str | None) -> list[dict[str, Any]]:
    candidates = sorted(runs, key=lambda run: (-(run.get("updated") or 0), run.get("run_id") or ""))
    if not candidates:
        return []
    latest = candidates[0]
    baseline = _summary_baseline_run(candidates)
    best = _summary_best_run(candidates, metric)
    public = []
    for run in candidates:
        roles = []
        if run is best:
            roles.append("best")
        if run is latest:
            roles.append("latest")
        if run is baseline:
            roles.append("baseline")
        role = roles[0] if roles else "candidate"
        public.append(
            {
                "run_dir": run["run_dir"],
                "run_id": run["run_id"],
                "run_name": run["run_name"],
                "status": run["status"],
                "project": run["project"],
                "role": role,
                "roles": roles or ["candidate"],
                "metrics": [item["name"] for item in run.get("metric_catalog") or []],
                "mtime": run.get("updated") or 0,
            }
        )
    return sorted(public, key=lambda run: (0 if run["role"] != "candidate" else 1, -run["mtime"], run["run_id"]))


def _summary_best_run(runs: list[dict[str, Any]], metric: str | None) -> dict[str, Any] | None:
    scored = []
    for run in runs:
        best_metric = run.get("best_metric") or {}
        value = None
        if isinstance(best_metric, dict) and best_metric.get("name") == metric:
            value = best_metric.get("value", best_metric.get("best_value"))
        if value is None:
            latest = (run.get("metrics") or {}).get(metric or "", {})
            if isinstance(latest, dict):
                value = latest.get("value")
        if isinstance(value, (int, float)):
            scored.append((value, run.get("updated") or 0, run))
    return max(scored, key=lambda item: (item[0], item[1]))[2] if scored else (runs[0] if runs else None)


def _summary_baseline_run(runs: list[dict[str, Any]]) -> dict[str, Any] | None:
    for run in runs:
        text = f"{run.get('run_id', '')} {run.get('run_name', '')}".lower()
        if run.get("baseline") or "baseline" in text:
            return run
    return sorted(runs, key=lambda run: (run.get("updated") or 0, run.get("run_id") or ""))[0] if runs else None


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
    manifest, manifest_warnings = read_manifest(run_dir)
    rows, latest_metrics, warnings = read_metrics(run_dir)
    warnings = manifest_warnings + warnings
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        if isinstance(row.get("value"), (int, float)) and row.get("name"):
            grouped.setdefault(str(row["name"]), []).append(row)
    run_id = str(manifest.get("run_id") or run_dir.name)
    best_metric = manifest.get("best_metric")
    mtime = run_dir.stat().st_mtime if run_dir.exists() else 0
    tags = [str(item) for item in manifest.get("tags") or []]
    return {
        "run_dir": str(run_dir),
        "run_id": run_id,
        "run_name": str(manifest.get("run_name") or run_id),
        "status": str(manifest.get("status") or "unknown"),
        "project": str(manifest.get("project") or ""),
        "tags": tags,
        "group": str(manifest.get("group") or ""),
        "baseline": bool(manifest.get("baseline")),
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
        if run.get("baseline") or "baseline" in text:
            return run
    return sorted(runs, key=lambda run: (run["mtime"], run["run_id"]))[0] if runs else None


def _compare_points(
    rows: list[dict[str, Any]],
    max_points: int,
    normalize: bool,
    align: str,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    bounded, metadata = downsample_points(rows, max_points=max_points)
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
    return points, metadata


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
        "tags": run.get("tags") or [],
        "group": run.get("group") or "",
        "baseline": bool(run.get("baseline")),
        "role": run["role"],
        "roles": run["roles"],
        "metrics": sorted(run["metric_names"]),
        "mtime": run["mtime"],
    }


def _baseline_value(runs: list[dict[str, Any]], metric: str | None) -> float | None:
    baseline = _baseline_run(runs)
    if baseline is None or not metric:
        return None
    rows = baseline["metric_rows"].get(metric, [])
    for row in reversed(rows):
        value = row.get("value")
        if isinstance(value, (int, float)):
            return float(value)
    return None
