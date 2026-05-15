"""Schemas and YAML helpers for report artifact manifests."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


@dataclass
class ReportArtifact:
    id: str
    type: str
    path: str
    kind: str
    title: str = ""
    source_files: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    provenance: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ReportManifest:
    report_id: str
    schema_version: str = "2.0"
    source: dict[str, Any] = field(default_factory=dict)
    outputs: list[ReportArtifact | dict[str, Any]] = field(default_factory=list)
    parameters: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    provenance: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().astimezone().isoformat())

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["outputs"] = [
            output.to_dict() if isinstance(output, ReportArtifact) else dict(output)
            for output in self.outputs
        ]
        return data


def write_report_manifest(path: str | Path, manifest: ReportManifest | dict[str, Any]) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    data = manifest.to_dict() if isinstance(manifest, ReportManifest) else dict(manifest)
    out.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return out


def read_report_manifest(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        return {}
    data.setdefault("schema_version", "1.0")
    return data


def validate_report_manifest_schema(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not manifest.get("report_id"):
        errors.append("report_id is required")
    outputs = manifest.get("outputs")
    if not isinstance(outputs, list):
        errors.append("outputs must be a list")
        outputs = []
    for index, output in enumerate(outputs):
        if not isinstance(output, dict):
            errors.append(f"outputs[{index}] must be an object")
            continue
        for key in ["id", "type", "path", "kind"]:
            if not output.get(key):
                errors.append(f"outputs[{index}].{key} is required")
        provenance = output.get("provenance", {})
        if provenance and not isinstance(provenance, dict):
            errors.append(f"outputs[{index}].provenance must be an object")
    if "provenance" in manifest and not isinstance(manifest["provenance"], dict):
        errors.append("provenance must be an object")
    return errors


def relative_artifact_path(path: str | Path, base_dir: str | Path) -> str:
    path = Path(path)
    base = Path(base_dir)
    try:
        return path.relative_to(base).as_posix()
    except ValueError:
        return path.as_posix()
