"""Dependency-light image helpers."""

from __future__ import annotations

from pathlib import Path


def validate_image_path(image: str | Path) -> Path:
    path = Path(image)
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"Image source does not exist or is not a file: {path}")
    return path
