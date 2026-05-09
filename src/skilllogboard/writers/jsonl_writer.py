"""Append-only JSONL writer."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import json


class JsonlWriter:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, obj: Any) -> None:
        if hasattr(obj, "to_dict"):
            data = obj.to_dict()
        elif isinstance(obj, dict):
            data = obj
        else:
            data = {"value": obj}

        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
            f.flush()
