"""Project-level live board state."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from skilllogboard.live.state import build_live_run_state


def find_run_dirs(root_dir: str | Path) -> list[Path]:
    root = Path(root_dir)
    if (root / "manifest.yaml").exists():
        return [root]
    return sorted(path for path in root.rglob("manifest.yaml") if path.is_file())


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
                "main_metric": state.manifest.get("main_metric"),
                "best_metric": state.manifest.get("best_metric"),
                "warnings": state.warnings,
            }
        )
    return {
        "mode": "project",
        "root_dir": str(root),
        "runs": runs,
        "status_counts": counts,
        "alerts": warnings[-20:],
        "leaderboard": _leaderboard_lite(runs),
        "warnings": warnings,
    }


def _leaderboard_lite(runs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for run in runs:
        best = run.get("best_metric") or {}
        if isinstance(best, dict) and best.get("name"):
            rows.append(
                {
                    "run_id": run.get("run_id"),
                    "metric": best.get("name"),
                    "value": best.get("value"),
                    "step": best.get("step"),
                    "status": run.get("status"),
                }
            )
    return rows
