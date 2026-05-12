---
milestone: "v0.7"
phase: "Report Artifact Layer"
day: "3"
slice: "05_export_figure_cli"
title: "export-figure CLI"
priority: "P0"
status: "pending"
target_version: "v0.7-report-artifacts"
---

# 05_export_figure_cli — export-figure CLI

## Objective

Add CLI support for generating report figures.

## Context

Users should be able to export figures independently of full report generation.

## Dependencies

- 04_seed_errorbar_and_ablation_bar_figures

## Target Files

- src/skilllogboard/cli/main.py
- src/skilllogboard/reports/figure_builder.py
- tests/test_cli_report_artifacts.py

## Implementation Steps

1. Add `skilllog export-figure ROOT_OR_RUN_DIR` command.
2. Support `--type metric-curve|metric-curve-overlay|seed-errorbar|ablation-bar`.
3. Support `--metric`, `--metrics`, `--group-by`, `--format`, and `--output` where applicable.
4. Return readable message if report extra is missing.
5. Add CLI tests for at least metric-curve and missing dependency path.

## Acceptance Criteria

- `skilllog export-figure` appears in help.
- Metric curve figure export works when dependencies are available.
- Missing optional dependency is handled clearly.
- CLI tests pass or skip correctly.

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

