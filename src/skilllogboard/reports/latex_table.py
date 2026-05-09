"""Small LaTeX-like table export helper."""

from __future__ import annotations

from typing import Any

from skilllogboard.compare.leaderboard import rows_to_latex


def export_latex_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    return rows_to_latex(rows, columns)
