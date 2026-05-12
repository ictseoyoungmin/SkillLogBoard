---
milestone: "v0.7"
phase: "Report Artifact Layer"
day: "2"
slice: "03_seed_summary_table_adapter"
title: "seed summary table adapter"
priority: "P0"
status: "pending"
target_version: "v0.7-report-artifacts"
---

# 03_seed_summary_table_adapter — seed summary table adapter

## Objective

Implement a report table adapter for seed summary results.

## Context

Week 5 seed grouping already computes mean/std/median/best. v0.7 should expose it as report-ready table artifacts.

## Dependencies

- 02_leaderboard_table_adapter

## Target Files

- src/skilllogboard/reports/table_builder.py
- src/skilllogboard/compare/seed_group.py
- tests/test_report_tables.py

## Implementation Steps

1. Implement `build_seed_summary_table(root_dir_or_records, metric, mode, group_by)`.
2. Reuse existing seed grouping logic where possible.
3. Return rows with group, count, mean, std, median, best, best_run_id.
4. Support `group_by` as string or list.
5. Add tests for multiple seeds and group_by axes.

## Acceptance Criteria

- Seed summary table builds deterministically.
- Mean/std/median/best fields are present.
- Missing metric values do not crash table generation.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_report_tables.py tests/test_seed_group.py
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

