"""Report provenance helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class ReportProvenance:
    files: list[str] = field(default_factory=list)
    metrics: list[str] = field(default_factory=list)
    columns: list[str] = field(default_factory=list)
    step_range: dict[str, int] | None = None
    run_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "files": sorted(set(self.files)),
            "metrics": sorted(set(self.metrics)),
            "columns": list(self.columns),
            "step_range": self.step_range,
            "run_ids": list(self.run_ids),
            "metadata": dict(self.metadata),
        }


def file_provenance(paths: list[str | Path]) -> dict[str, Any]:
    files = []
    for path in paths:
        candidate = Path(path)
        if candidate.exists():
            files.append(candidate.as_posix())
    return ReportProvenance(files=files).to_dict()
