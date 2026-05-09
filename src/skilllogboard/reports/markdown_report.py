"""Markdown summary builder for a single run."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import csv
import json

import yaml


def build_summary(run_dir: str | Path) -> Path:
    run_dir = Path(run_dir)
    out = run_dir / "summary.md"
    manifest = _load_yaml(run_dir / "manifest.yaml")
    config = _load_yaml(run_dir / "config.yaml")
    latest_metrics = _read_latest_metrics(run_dir / "metrics.csv")
    artifact_records = _read_artifact_index(run_dir / "artifact_index.json")

    lines = ["# Run Summary", ""]
    lines.extend(_run_section(run_dir, manifest))
    lines.extend(_config_section(config))
    lines.extend(_metrics_section(manifest, latest_metrics))
    lines.extend(_artifact_section(artifact_records))
    lines.extend(
        [
            "## Files",
            "",
            "- `manifest.yaml`",
            "- `config.yaml`",
            "- `metrics.csv`",
            "- `events.jsonl`",
            "- `artifact_index.json`",
            "",
        ]
    )
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _run_section(run_dir: Path, manifest: dict[str, Any]) -> list[str]:
    rows = {
        "Project": manifest.get("project", "unknown"),
        "Run": manifest.get("run_name", run_dir.name),
        "Run ID": manifest.get("run_id", run_dir.name),
        "Status": manifest.get("status", "unknown"),
        "Created": manifest.get("created_at", ""),
        "Updated": manifest.get("updated_at", ""),
        "Model": manifest.get("model_name", ""),
        "Dataset": manifest.get("dataset_name", ""),
        "Seed": manifest.get("seed", ""),
    }
    lines = ["## Run", ""]
    for key, value in rows.items():
        if value not in (None, ""):
            lines.append(f"- {key}: `{value}`")
    lines.append("")
    return lines


def _config_section(config: dict[str, Any]) -> list[str]:
    lines = ["## Config", ""]
    if not config:
        lines.extend(["No `config.yaml` file was found or it was empty.", ""])
        return lines
    for key in ["model_name", "dataset_name", "seed", "optimizer", "lr", "batch_size"]:
        if key in config:
            lines.append(f"- {key}: `{config[key]}`")
    lines.extend(["", "Full config: `config.yaml`", ""])
    return lines


def _metrics_section(manifest: dict[str, Any], latest_metrics: dict[str, dict[str, str]]) -> list[str]:
    lines = ["## Metrics", ""]
    best_metric = manifest.get("best_metric")
    if best_metric:
        lines.append(
            "- Best metric: "
            f"`{best_metric.get('name')}` = `{best_metric.get('best_value')}` "
            f"at step `{best_metric.get('best_step')}` ({best_metric.get('mode')})"
        )
        lines.append("")
    if not latest_metrics:
        lines.extend(["No metrics have been logged yet.", ""])
        return lines
    lines.extend(["| Metric | Latest value | Step |", "|---|---:|---:|"])
    for name, row in latest_metrics.items():
        lines.append(f"| `{name}` | `{row.get('value', '')}` | `{row.get('step', '')}` |")
    lines.extend(["", "Metric files: `metrics.csv`, `events.jsonl`", ""])
    return lines


def _artifact_section(records: list[dict[str, Any]]) -> list[str]:
    lines = ["## Artifacts", ""]
    if not records:
        lines.extend(["No artifacts, images, or tables have been logged yet.", ""])
        return lines
    lines.extend(["| Name | Type | Path | Mode |", "|---|---|---|---|"])
    for record in records:
        path = record.get("path") or record.get("source") or ""
        mode = "copy" if record.get("copy") else "reference"
        lines.append(
            f"| `{record.get('name', '')}` | `{record.get('type', '')}` | `{path}` | `{mode}` |"
        )
    lines.append("")
    return lines


def _read_latest_metrics(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    latest: dict[str, dict[str, str]] = {}
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("name")
            if name:
                latest[name] = row
    return latest


def _read_artifact_index(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return list(data.get("artifacts", []))
