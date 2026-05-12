---
milestone: "v0.7"
phase: "Report Artifact Layer"
day: "2"
slice: "05_export_table_compatibility_update"
title: "export-table compatibility update"
priority: "P0"
status: "pending"
target_version: "v0.7-report-artifacts"
---

# 05_export_table_compatibility_update — export-table compatibility update

## Objective

Extend existing `export-table` behavior to support report table types without breaking current CLI usage.

## Context

Week 5 already implemented `export-table`. v0.7 should extend the command, not replace it.

## Dependencies

- 04_ablation_and_rule_audit_tables

## Target Files

- src/skilllogboard/cli/main.py
- src/skilllogboard/reports/table_builder.py
- tests/test_cli_report_artifacts.py
- tests/test_cli_compare.py

## Implementation Steps

1. Add or extend CLI options: `--table leaderboard|seed-summary|ablation-summary|config-diff|rule-audit`.
2. Support output formats: `csv`, `md`, `latex`, `html`, and optionally `json`.
3. Preserve existing Week 5 `export-table` invocation compatibility.
4. Return readable errors for unsupported table type or missing metric.
5. Add CLI tests.

## Acceptance Criteria

- `skilllog export-table` existing tests still pass.
- `--table seed-summary` works.
- `--table leaderboard` works.
- Markdown/CSV/LaTeX outputs work.
- CLI tests pass.

## Verification Commands

```bash
pytest -q tests/test_cli_report_artifacts.py tests/test_cli_compare.py
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

