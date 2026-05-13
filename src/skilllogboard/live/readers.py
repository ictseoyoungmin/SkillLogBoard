"""Safe readers for local run folders."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import csv
import json
import os

import yaml


def read_manifest(run_dir: str | Path) -> tuple[dict[str, Any], list[str]]:
    path = Path(run_dir) / "manifest.yaml"
    if not path.exists():
        return {}, [f"missing {path.name}"]
    try:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except Exception as exc:
        return {}, [f"could not read {path.name}: {exc}"]
    return data if isinstance(data, dict) else {}, []


def read_metrics(run_dir: str | Path) -> tuple[list[dict[str, Any]], dict[str, Any], list[str]]:
    path = Path(run_dir) / "metrics.csv"
    if not path.exists():
        return [], {}, [f"missing {path.name}"]
    rows: list[dict[str, Any]] = []
    latest: dict[str, Any] = {}
    try:
        with path.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                item = {
                    "timestamp": row.get("timestamp", ""),
                    "step": _as_int(row.get("step")),
                    "name": row.get("name", ""),
                    "value": _as_float(row.get("value")),
                    "group": row.get("group", ""),
                    "metadata": _json_value(row.get("metadata_json", "{}")),
                }
                if item["name"]:
                    rows.append(item)
                    latest[str(item["name"])] = item
    except Exception as exc:
        return rows, latest, [f"could not read {path.name}: {exc}"]
    return rows, latest, []


def read_jsonl(path: str | Path, limit: int | None = None) -> tuple[list[dict[str, Any]], list[str]]:
    path = Path(path)
    if not path.exists():
        return [], [f"missing {path.name}"]
    lines = _tail_lines(path, limit=limit)
    records: list[dict[str, Any]] = []
    warnings: list[str] = []
    for idx, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            warnings.append(f"invalid JSONL record in {path.name}:{idx}")
            continue
        if isinstance(record, dict):
            records.append(record)
    return records, warnings


def read_events(run_dir: str | Path, limit: int = 200) -> tuple[list[dict[str, Any]], list[str]]:
    return read_jsonl(Path(run_dir) / "events.jsonl", limit=limit)


def read_rule_trace(run_dir: str | Path, limit: int = 200) -> tuple[list[dict[str, Any]], list[str]]:
    return read_jsonl(Path(run_dir) / "skill_trace.jsonl", limit=limit)


def read_artifacts(run_dir: str | Path, limit: int = 50) -> tuple[list[dict[str, Any]], list[str]]:
    run = Path(run_dir)
    path = run / "artifact_index.json"
    warnings: list[str] = []
    records: list[dict[str, Any]] = []
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            artifacts = data.get("artifacts", []) if isinstance(data, dict) else []
            records = [item for item in artifacts if isinstance(item, dict)][-limit:]
        except Exception as exc:
            warnings.append(f"could not read {path.name}: {exc}")
    else:
        artifacts_dir = run / "artifacts"
        if artifacts_dir.exists():
            for item in sorted(artifacts_dir.iterdir(), key=lambda p: p.stat().st_mtime)[-limit:]:
                if item.is_file():
                    records.append(
                        {
                            "name": item.name,
                            "type": "artifact",
                            "path": item.relative_to(run).as_posix(),
                            "size": item.stat().st_size,
                        }
                    )
        else:
            warnings.append("missing artifact_index.json")
    return records, warnings


def tail_log_file(path: str | Path | None, limit: int = 100, max_bytes: int = 65536) -> tuple[list[str], list[str]]:
    if not path:
        return [], []
    path = Path(path)
    if not path.exists():
        return [], [f"missing log file: {path}"]
    try:
        size = path.stat().st_size
        with path.open("rb") as f:
            if size > max_bytes:
                f.seek(max(0, size - max_bytes))
            text = f.read().decode("utf-8", errors="replace")
    except Exception as exc:
        return [], [f"could not read log file {path}: {exc}"]
    return text.splitlines()[-limit:], []


def _tail_lines(path: Path, limit: int | None) -> list[str]:
    if limit is None:
        return path.read_text(encoding="utf-8").splitlines()
    try:
        with path.open("rb") as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            f.seek(max(0, size - 65536))
            text = f.read().decode("utf-8", errors="replace")
    except OSError:
        return []
    return text.splitlines()[-limit:]


def _json_value(value: str | None) -> Any:
    try:
        return json.loads(value or "{}")
    except json.JSONDecodeError:
        return {}


def _as_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _as_int(value: Any) -> int | None:
    try:
        if value in {None, ""}:
            return None
        return int(value)
    except (TypeError, ValueError):
        return None
