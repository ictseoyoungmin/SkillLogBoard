"""Metrics CSV writer.

MVP schema:
timestamp, step, name, value, group, metadata_json
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any
import csv
import json


class MetricsCsvWriter:
    fieldnames = ["timestamp", "step", "name", "value", "group", "metadata_json"]

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            with self.path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()

    def write_metric(
        self,
        name: str,
        value: float,
        step: int | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        group = name.split("/", 1)[0] if "/" in name else ""
        row = {
            "timestamp": datetime.now().astimezone().isoformat(),
            "step": "" if step is None else step,
            "name": name,
            "value": value,
            "group": group,
            "metadata_json": json.dumps(metadata or {}, ensure_ascii=False),
        }
        with self.path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writerow(row)
            f.flush()
