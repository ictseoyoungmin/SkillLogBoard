"""Artifact storage modes."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import os
import shutil


def store_artifact(source: str | Path, dest_dir: str | Path, mode: str = "copy") -> dict[str, Any]:
    """Store an artifact using copy, symlink, or hardlink with safe copy fallback."""

    src = Path(source)
    out_dir = Path(dest_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / src.name
    requested = mode if mode in {"copy", "symlink", "hardlink"} else "copy"
    effective = requested
    warning = ""
    try:
        if requested == "symlink":
            if target.exists() or target.is_symlink():
                target.unlink()
            target.symlink_to(src.resolve())
        elif requested == "hardlink":
            if target.exists():
                target.unlink()
            os.link(src, target)
        else:
            shutil.copy2(src, target)
    except OSError as exc:
        effective = "copy"
        warning = f"{requested} failed; copied artifact instead: {exc}"
        shutil.copy2(src, target)
    return {
        "path": str(target),
        "name": src.name,
        "storage_mode": requested,
        "effective_storage_mode": effective,
        "warning": warning,
    }
