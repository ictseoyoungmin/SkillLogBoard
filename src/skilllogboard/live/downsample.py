"""Deterministic downsampling for live metric series."""

from __future__ import annotations

from typing import Any
import math


def downsample_points(rows: list[dict[str, Any]], max_points: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Bound a series while preserving first and last points."""

    original_count = len(rows)
    safe_max = max(1, int(max_points or 1))
    if original_count <= safe_max:
        return list(rows), {
            "method": "none",
            "downsampled": False,
            "original_count": original_count,
            "returned_count": original_count,
            "max_points": safe_max,
        }
    if safe_max == 1:
        selected = [rows[-1]]
    elif safe_max == 2:
        selected = [rows[0], rows[-1]]
    else:
        last_index = original_count - 1
        indexes = {0, last_index}
        slots = safe_max - 2
        for slot in range(1, slots + 1):
            indexes.add(math.floor(slot * last_index / (slots + 1)))
        selected = [rows[index] for index in sorted(indexes)[:safe_max]]
        if selected[-1] is not rows[-1]:
            selected[-1] = rows[-1]
    return selected, {
        "method": "first-last-even",
        "downsampled": True,
        "original_count": original_count,
        "returned_count": len(selected),
        "max_points": safe_max,
    }
