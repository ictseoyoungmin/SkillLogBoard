"""Dry-run prune planner."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from time import time
from typing import Any

from skilllogboard.index.builder import build_project_index
from skilllogboard.retention.policy import RetentionPolicy


@dataclass
class PruneAction:
    run_id: str
    path: str
    action: str
    reason: str
    protected: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def plan_prune(root_dir: str | Path, policy: RetentionPolicy | None = None) -> dict[str, Any]:
    active_policy = policy or RetentionPolicy()
    index = build_project_index(root_dir)
    protected_ids = _protected_run_ids(index.runs, active_policy)
    cutoff = time() - (active_policy.older_than_days or 0) * 86400 if active_policy.older_than_days else None
    actions: list[PruneAction] = []
    for run in index.runs:
        tags = {str(tag) for tag in run.tags}
        if run.run_id in protected_ids:
            actions.append(PruneAction(run.run_id, run.path, "keep", "protected by best/latest/baseline policy", True))
        elif tags.intersection(active_policy.exclude_tags):
            actions.append(PruneAction(run.run_id, run.path, "keep", "protected by exclude_tags", True))
        elif cutoff is not None and run.updated_at >= cutoff:
            actions.append(PruneAction(run.run_id, run.path, "keep", "newer than older_than_days", True))
        else:
            action = "archive" if active_policy.archive_before_delete else "delete_candidate"
            reason = "dry-run candidate" if active_policy.dry_run else "eligible for retention action"
            actions.append(PruneAction(run.run_id, run.path, action, reason, False))
    return {
        "dry_run": active_policy.dry_run,
        "policy": active_policy.to_dict(),
        "run_count": len(index.runs),
        "actions": [action.to_dict() for action in actions],
    }


def _protected_run_ids(runs: list[Any], policy: RetentionPolicy) -> set[str]:
    protected: set[str] = set()
    latest = sorted(runs, key=lambda run: (-run.updated_at, run.run_id))[: max(0, policy.keep_latest)]
    protected.update(run.run_id for run in latest)
    if policy.protect_baseline:
        protected.update(run.run_id for run in runs if run.baseline)
    scored = []
    for run in runs:
        numeric = [value for value in run.key_metrics.values() if isinstance(value, (int, float))]
        if numeric:
            scored.append((max(numeric), run.updated_at, run.run_id))
    protected.update(run_id for _, _, run_id in sorted(scored, reverse=True)[: max(0, policy.keep_best)])
    return protected
