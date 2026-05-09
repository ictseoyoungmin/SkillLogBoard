"""Manifest schema and atomic save helpers."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any
import os
import tempfile

import yaml


@dataclass
class Manifest:
    project: str
    run_name: str
    run_id: str
    run_dir: str
    created_at: str = field(default_factory=lambda: datetime.now().astimezone().isoformat())
    updated_at: str | None = None
    status: str = "running"
    framework: str | None = None
    task_type: str | None = None
    model_name: str | None = None
    dataset_name: str | None = None
    seed: int | None = None
    main_metric: dict[str, Any] | None = None
    best_metric: dict[str, Any] | None = None
    files: dict[str, str] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
    error_summary: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def touch(self) -> None:
        self.updated_at = datetime.now().astimezone().isoformat()

    def save(self, path: str | Path) -> None:
        """Atomic YAML save."""
        self.touch()
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = self.to_dict()

        fd, tmp_name = tempfile.mkstemp(prefix=".manifest_", suffix=".yaml", dir=str(path.parent))
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)
            os.replace(tmp_name, path)
        finally:
            if os.path.exists(tmp_name):
                os.remove(tmp_name)


def load_manifest(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}
