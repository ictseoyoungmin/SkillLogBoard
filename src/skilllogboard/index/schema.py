"""Schema for the rebuildable project index."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
import json

DEFAULT_INDEX_PATH = ".skilllogboard/index.json"
INDEX_SCHEMA_VERSION = 1


@dataclass
class ProjectIndexRun:
    run_id: str
    path: str
    status: str = "unknown"
    started_at: str = ""
    updated_at: float = 0.0
    duration: float | None = None
    key_metrics: dict[str, Any] = field(default_factory=dict)
    metric_summaries: list[dict[str, Any]] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    group: str = ""
    baseline: bool = False
    artifact_count: int = 0
    warning_count: int = 0
    fingerprint: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ProjectIndex:
    root_dir: str
    generated_at: str
    runs: list[ProjectIndexRun]
    schema_version: int = INDEX_SCHEMA_VERSION
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "root_dir": self.root_dir,
            "generated_at": self.generated_at,
            "run_count": len(self.runs),
            "runs": [run.to_dict() for run in self.runs],
            "warnings": self.warnings,
        }


def read_project_index(path: str | Path) -> ProjectIndex:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    runs = [ProjectIndexRun(**item) for item in data.get("runs", []) if isinstance(item, dict)]
    return ProjectIndex(
        root_dir=str(data.get("root_dir") or ""),
        generated_at=str(data.get("generated_at") or ""),
        runs=runs,
        schema_version=int(data.get("schema_version") or INDEX_SCHEMA_VERSION),
        warnings=[str(item) for item in data.get("warnings", [])],
    )


def write_project_index(index: ProjectIndex, path: str | Path) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(index.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out
