"""Compare helpers for multi-run SkillLogBoard reports."""

from skilllogboard.compare.run_index import (
    RunRecord,
    build_run_index,
    discover_runs,
    load_run_record,
)

__all__ = ["RunRecord", "build_run_index", "discover_runs", "load_run_record"]
