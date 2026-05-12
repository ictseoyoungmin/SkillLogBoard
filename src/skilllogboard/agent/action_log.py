"""Run-level agent action JSONL helpers."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any
import json


@dataclass
class AgentAction:
    actor: str
    action: str
    status: str
    timestamp: str = field(default_factory=lambda: datetime.now().astimezone().isoformat())
    target: str = ""
    command: str = ""
    outputs: list[str] = field(default_factory=list)
    duration_sec: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def normalize_agent_action(action_record: AgentAction | dict[str, Any]) -> dict[str, Any]:
    data = action_record.to_dict() if isinstance(action_record, AgentAction) else dict(action_record)
    missing = [key for key in ["actor", "action", "status"] if not str(data.get(key, "")).strip()]
    if missing:
        raise ValueError(f"Missing required agent action fields: {', '.join(missing)}")
    data.setdefault("timestamp", datetime.now().astimezone().isoformat())
    data.setdefault("target", "")
    data.setdefault("command", "")
    outputs = data.get("outputs", [])
    if isinstance(outputs, str):
        outputs = [outputs]
    data["outputs"] = list(outputs or [])
    data.setdefault("duration_sec", None)
    data.setdefault("metadata", {})
    return data


def append_agent_action(run_dir: str | Path, action_record: AgentAction | dict[str, Any]) -> Path:
    data = normalize_agent_action(action_record)
    path = _action_log_path(run_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(data, sort_keys=True) + "\n")
    return path


def read_agent_actions(run_dir: str | Path) -> list[dict[str, Any]]:
    path = _action_log_path(run_dir)
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid agent action JSONL at {path}:{lineno}") from exc
        records.append(record)
    return records


def _action_log_path(run_dir: str | Path) -> Path:
    return Path(run_dir) / "agent" / "actions.jsonl"
