"""Run state helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

STATUS_RUNNING = "running"
STATUS_COMPLETED = "completed"
STATUS_FAILED = "failed"
STATUS_INTERRUPTED = "interrupted"

TERMINAL_STATUSES = {STATUS_COMPLETED, STATUS_FAILED, STATUS_INTERRUPTED}


@dataclass
class Run:
    project: str
    run_name: str
    run_id: str
    run_dir: Path
