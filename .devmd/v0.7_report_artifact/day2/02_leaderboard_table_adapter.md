---
milestone: "v0.7"
phase: "Report Artifact Layer"
day: "2"
slice: "02_leaderboard_table_adapter"
title: "leaderboard table adapter"
priority: "P0"
status: "pending"
target_version: "v0.7-report-artifacts"
---

# 02_leaderboard_table_adapter — leaderboard table adapter

## Objective

Implement a report table adapter for leaderboard data using existing compare logic.

## Context

Week 5 already has leaderboard functionality. v0.7 should reuse it rather than duplicate ranking code.

## Dependencies

- 01_table_builder_contract

## Target Files

- src/skilllogboard/reports/table_builder.py
- src/skilllogboard/compare/leaderboard.py
- tests/test_report_tables.py

## Implementation Steps

1. Implement `build_leaderboard_table(root_dir_or_records, metric, mode)` or equivalent.
2. Reuse existing `build_run_index` and `build_leaderboard` where possible.
3. Return a ReportTable with stable columns.
4. Include rank, run_id, run_name, metric_value, best_step, warning_count, error_count if available.
5. Add tests with temporary run folders or fake records.

## Acceptance Criteria

- Leaderboard report table builds from existing run records.
- Rows are sorted according to mode.
- Missing metric values are handled consistently.
- Existing compare leaderboard tests still pass.

## Verification Commands

```bash
pytest -q tests/test_report_tables.py tests/test_leaderboard.py
```

## Non-goals

- Do not implement unrelated future features.

## Handoff Notes

- Keep this slice focused and small.
- Preserve existing v0.6 public APIs and run folder compatibility.
- Existing `summary.md`, `dashboard.html`, `compare.md`, `compare.html`, and `export-table` behavior must not regress.
- Core install must remain lightweight. Do not add matplotlib, pandas, torch, lightning, sklearn, or domain packages to core dependencies.
- If a blocker appears, document it in the Agent Completion Block instead of expanding scope.

---

## Agent Completion Block

> The agent must update this block after finishing the slice.

- [x] Implementation completed
- [x] Acceptance criteria verified
- [x] Tests or smoke checks executed
- [x] No unrelated files changed
- [x] Notes added below if anything was skipped or deferred

**Status:** COMPLETED
**Completed at:** 2026-05-12
**Completed by:** Codex
**Verification command(s):** .venv/bin/pytest -q; .venv/bin/python examples/basic_usage.py; .venv/bin/python examples/ir_drop_example.py; .venv/bin/python examples/trajectory_example.py; .venv/bin/python -m build --no-isolation
**Notes:** Implemented and verified as part of the v0.7 report artifact layer pass. Optional figure generation keeps a readable skipped-dependency fallback when matplotlib is unavailable.

<!-- AGENT_STATUS: COMPLETED -->

