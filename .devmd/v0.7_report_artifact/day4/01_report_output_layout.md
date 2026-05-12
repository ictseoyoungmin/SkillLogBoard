---
milestone: "v0.7"
phase: "Report Artifact Layer"
day: "4"
slice: "01_report_output_layout"
title: "report output layout"
priority: "P0"
status: "pending"
target_version: "v0.7-report-artifacts"
---

# 01_report_output_layout — report output layout

## Objective

Implement a safe output layout for single-run and multi-run report packages.

## Context

v0.7 must avoid polluting existing run folders while still creating predictable report outputs.

## Dependencies

- day3 figure builder slices completed.

## Target Files

- src/skilllogboard/reports/report_builder.py
- tests/test_report_builder.py

## Implementation Steps

1. Create `report_builder.py`.
2. Define output path policy for single-run reports.
3. Define output path policy for multi-run reports, such as `runs/{project}/_reports/{report_id}/`.
4. Implement helper to create report directory tree: `tables/`, `figures/`.
5. Ensure paths are deterministic in tests by allowing explicit output_dir.
6. Add tests for output layout creation.

## Acceptance Criteria

- Report output directories are created.
- Single-run and multi-run layout are supported or explicitly documented.
- Tests can use explicit output_dir for deterministic behavior.
- No existing files are overwritten unless explicitly requested.

## Verification Commands

```bash
pytest -q tests/test_report_builder.py
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

