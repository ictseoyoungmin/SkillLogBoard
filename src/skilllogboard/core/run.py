"""Run state placeholder."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Run:
    project: str
    run_name: str
    run_id: str
    run_dir: Path
