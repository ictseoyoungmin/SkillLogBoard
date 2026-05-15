"""Serializable chart specifications for portable report figures."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
import json


@dataclass
class ChartSpec:
    chart_id: str
    chart_type: str
    metric: str = ""
    source_files: list[str] = field(default_factory=list)
    encoding: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def chart_spec_from_artifact(artifact: dict[str, Any]) -> ChartSpec:
    provenance = artifact.get("provenance") or {}
    metrics = provenance.get("metrics") or []
    metric = str(metrics[0]) if metrics else ""
    return ChartSpec(
        chart_id=str(artifact.get("id") or artifact.get("kind") or "chart"),
        chart_type=str(artifact.get("kind") or "figure"),
        metric=metric,
        source_files=[str(item) for item in provenance.get("files") or artifact.get("source_files") or []],
        encoding={"x": "step", "y": metric or "value", "series": "run_id"},
        metadata={"figure_path": artifact.get("path"), **dict(artifact.get("metadata") or {})},
    )


def write_chart_spec(path: str | Path, spec: ChartSpec) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(spec.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out
