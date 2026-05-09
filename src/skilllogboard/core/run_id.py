"""Run id utilities."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re


def slugify(value: str, max_length: int = 64) -> str:
    """Convert a run name to a filesystem-safe slug."""
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9가-힣._-]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("._-")
    return (value or "run")[:max_length]


def make_run_id(run_name: str, created_at: datetime | None = None) -> str:
    """Create a timestamp + slug run id."""
    created_at = created_at or datetime.now().astimezone()
    ts = created_at.strftime("%Y-%m-%d_%H-%M-%S")
    return f"{ts}_{slugify(run_name)}"


def ensure_unique_run_dir(project_dir: Path, run_id: str) -> Path:
    """Create a collision-safe run directory path.

    The directory is not created here. This helper only returns a safe path.
    """
    candidate = project_dir / run_id
    if not candidate.exists():
        return candidate

    for idx in range(1, 1000):
        suffixed = project_dir / f"{run_id}_{idx:03d}"
        if not suffixed.exists():
            return suffixed

    raise RuntimeError(f"Could not create unique run id for {run_id!r}")
