---
milestone: "v0.7"
phase: "Report Artifact Layer"
day: "2"
slice: "01_table_builder_contract"
title: "table builder contract"
priority: "P0"
status: "pending"
target_version: "v0.7-report-artifacts"
---

# 01_table_builder_contract — table builder contract

## Objective

Define the common interface and row schema for report table generation.

## Context

Tables should be deterministic, exportable, and reusable from CLI, report builder, and tests.

## Dependencies

- day1 report spec/manifest slices completed.

## Target Files

- src/skilllogboard/reports/table_builder.py
- tests/test_report_tables.py

## Implementation Steps

1. Create `table_builder.py`.
2. Define a common `ReportTable` schema or dict contract.
3. Include fields: `table_id`, `table_type`, `columns`, `rows`, `metadata`.
4. Implement helper `table_to_markdown(table)`.
5. Implement helper `table_to_csv(table, path_or_file)` or CSV string helper.
6. Implement helper `table_to_latex(table)` with simple tabular output.
7. Add tests for deterministic column order and exports.

## Acceptance Criteria

- ReportTable schema exists.
- Markdown table includes delimiter row.
- CSV export includes headers.
- Simple LaTeX export works without external dependencies.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_report_tables.py
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

