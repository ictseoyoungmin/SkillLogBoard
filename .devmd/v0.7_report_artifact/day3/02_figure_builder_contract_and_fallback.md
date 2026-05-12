---
milestone: "v0.7"
phase: "Report Artifact Layer"
day: "3"
slice: "02_figure_builder_contract_and_fallback"
title: "figure builder contract and fallback"
priority: "P0"
status: "pending"
target_version: "v0.7-report-artifacts"
---

# 02_figure_builder_contract_and_fallback — figure builder contract and fallback

## Objective

Define the figure builder interface and graceful fallback behavior when optional plotting dependencies are missing.

## Context

Figure generation should be robust in minimal installs and CI environments without optional extras.

## Dependencies

- 01_report_extra_dependency_policy

## Target Files

- src/skilllogboard/reports/figure_builder.py
- tests/test_report_figures.py

## Implementation Steps

1. Create `figure_builder.py`.
2. Define a `ReportFigure` schema or dict contract.
3. Implement optional import helper for matplotlib.
4. If matplotlib is unavailable, return a readable skipped result or raise a documented optional dependency error.
5. Do not import matplotlib at module import time unless guarded.
6. Add tests that skip gracefully when matplotlib is absent.

## Acceptance Criteria

- Figure builder module imports without matplotlib installed.
- Optional dependency error is readable.
- Figure schema includes figure_id, figure_type, path, metric, source_files, metadata.
- Tests pass or skip correctly.

## Verification Commands

```bash
pytest -q tests/test_report_figures.py
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

