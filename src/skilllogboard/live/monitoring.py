"""monitoring.jsonl schema and helpers."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any
import json


@dataclass
class MonitoringRecord:
    source: str
    type: str
    metrics: dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now().astimezone().isoformat())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def append_monitoring_record(
    run_dir: str | Path,
    record: MonitoringRecord | dict[str, Any],
) -> Path:
    data = record.to_dict() if isinstance(record, MonitoringRecord) else dict(record)
    data.setdefault("timestamp", datetime.now().astimezone().isoformat())
    path = Path(run_dir) / "monitoring.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(data, sort_keys=True) + "\n")
    return path


def read_monitoring_records(run_dir: str | Path, limit: int | None = 200) -> list[dict[str, Any]]:
    path = Path(run_dir) / "monitoring.jsonl"
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    if limit is not None:
        lines = lines[-limit:]
    records: list[dict[str, Any]] = []
    for line in lines:
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(item, dict):
            records.append(item)
    return records
