"""Retention policy schema."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class CheckpointRetentionPolicy:
    keep_best_checkpoint: bool = True
    keep_latest_checkpoint: bool = True
    max_checkpoints: int | None = None
    protect_baseline_checkpoint: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class RetentionPolicy:
    keep_best: int = 1
    keep_latest: int = 3
    older_than_days: int | None = None
    exclude_tags: list[str] = field(default_factory=list)
    protect_baseline: bool = True
    dry_run: bool = True
    archive_before_delete: bool = True
    artifact_rules: dict[str, Any] = field(default_factory=dict)
    checkpoints: CheckpointRetentionPolicy = field(default_factory=CheckpointRetentionPolicy)

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "RetentionPolicy":
        if not data:
            return cls()
        checkpoints = data.get("checkpoints")
        return cls(
            keep_best=int(data.get("keep_best", 1)),
            keep_latest=int(data.get("keep_latest", 3)),
            older_than_days=data.get("older_than_days"),
            exclude_tags=[str(item) for item in data.get("exclude_tags", [])],
            protect_baseline=bool(data.get("protect_baseline", True)),
            dry_run=bool(data.get("dry_run", True)),
            archive_before_delete=bool(data.get("archive_before_delete", True)),
            artifact_rules=dict(data.get("artifact_rules") or {}),
            checkpoints=CheckpointRetentionPolicy(**checkpoints) if isinstance(checkpoints, dict) else CheckpointRetentionPolicy(),
        )

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["checkpoints"] = self.checkpoints.to_dict()
        return data
