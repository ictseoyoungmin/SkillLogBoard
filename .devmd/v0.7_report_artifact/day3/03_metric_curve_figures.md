---
milestone: "v0.7"
phase: "Report Artifact Layer"
day: "3"
slice: "03_metric_curve_figures"
title: "metric curve figures"
priority: "P0"
status: "pending"
target_version: "v0.7-report-artifacts"
---

# 03_metric_curve_figures — metric curve figures

## Objective

Implement single-run and multi-run metric curve figure generation.

## Context

Metric curves are the minimum useful research figure output.

## Dependencies

- 02_figure_builder_contract_and_fallback

## Target Files

- src/skilllogboard/reports/figure_builder.py
- tests/test_report_figures.py

## Implementation Steps

1. Implement `build_metric_curve_figure(run_dir, metrics, output_path, format='png')`.
2. Implement `build_metric_curve_overlay_figure(root_dir, metric, output_path, mode=None)`.
3. Read from existing `metrics.csv` files.
4. Mark best metric point if best metadata is available.
5. Support PNG when matplotlib is available.
6. Optionally support lightweight HTML output using existing dashboard/plotly extra if already available.
7. Add tests with temporary metrics.csv data.

## Acceptance Criteria

- Single-run metric curve can be generated.
- Multi-run metric overlay can be generated.
- Missing metric produces readable error/warning.
- Tests pass or skip cleanly without matplotlib.

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

