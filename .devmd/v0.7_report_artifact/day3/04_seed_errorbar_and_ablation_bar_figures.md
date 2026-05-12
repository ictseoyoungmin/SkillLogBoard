---
milestone: "v0.7"
phase: "Report Artifact Layer"
day: "3"
slice: "04_seed_errorbar_and_ablation_bar_figures"
title: "seed errorbar and ablation bar figures"
priority: "P0"
status: "pending"
target_version: "v0.7-report-artifacts"
---

# 04_seed_errorbar_and_ablation_bar_figures — seed errorbar and ablation bar figures

## Objective

Implement report-ready seed errorbar and ablation bar figures.

## Context

Seed and ablation visualizations are important for research reports and paper-style summaries.

## Dependencies

- 03_metric_curve_figures

## Target Files

- src/skilllogboard/reports/figure_builder.py
- tests/test_report_figures.py

## Implementation Steps

1. Implement `build_seed_errorbar_figure(...)` using seed summary data.
2. Implement `build_ablation_bar_figure(...)` using ablation summary data.
3. Reuse table builder or compare helpers to avoid duplicate aggregation logic.
4. Support deterministic ordering.
5. Add tests using fake aggregated data or temporary runs.

## Acceptance Criteria

- Seed errorbar figure can be generated when report extra is installed.
- Ablation bar figure can be generated when report extra is installed.
- Both figure builders handle empty/missing data gracefully.
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

