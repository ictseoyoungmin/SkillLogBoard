"""Event schema.

Events are append-only records used by JSONL writers. Keep the schema simple and
human-readable during MVP development.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any


@dataclass
class Event:
    type: str
    key: str
    value: Any = None
    step: int | None = None
    path: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().astimezone().isoformat())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
