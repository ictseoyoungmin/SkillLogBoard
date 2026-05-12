---
milestone: "v0.7"
phase: "Report Artifact Layer"
day: "4"
slice: "05_report_build_cli"
title: "report build CLI"
priority: "P0"
status: "pending"
target_version: "v0.7-report-artifacts"
---

# 05_report_build_cli — report build CLI

## Objective

Add or extend CLI support for `skilllog report build`.

## Context

Users need a single command to generate the full report artifact package.

## Dependencies

- 04_report_manifest_integration

## Target Files

- src/skilllogboard/cli/main.py
- src/skilllogboard/reports/report_builder.py
- tests/test_cli_report_artifacts.py

## Implementation Steps

1. Add `skilllog report build ROOT_OR_RUN_DIR` subcommand or extend existing report command safely.
2. Support options: `--metric`, `--mode`, `--spec`, `--output-dir`, `--group-by`.
3. Generate report.md, report.html, report_manifest.yaml, tables, and figures according to available dependencies.
4. Return readable output paths.
5. Add CLI tests.

## Acceptance Criteria

- `skilllog report build` appears in help.
- Command generates report.md/report.html/report_manifest.yaml.
- Command works for at least a temporary multi-run fixture.
- Missing optional figure dependency does not fail table/report generation.
- CLI tests pass.

## Verification Commands

```bash
pytest -q tests/test_cli_report_artifacts.py
skilllog --help
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

