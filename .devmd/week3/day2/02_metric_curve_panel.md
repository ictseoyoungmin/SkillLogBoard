---
week: 3
day: 2
slice: "02_metric_curve_panel"
title: "metric curve panel"
priority: "P0"
status: "completed"
target_version: "v0.2-dashboard"
---

# 02_metric_curve_panel — metric curve panel

## Objective

Render a metric curve panel in the static dashboard.

## Context

The Week 3 acceptance criterion includes train/val curve display. For v0.2, a simple static curve is sufficient.

## Dependencies

- 01_metrics_loader_for_dashboard

## Target Files

- src/skilllogboard/dashboards/components.py
- src/skilllogboard/dashboards/templates/run.html.j2
- tests/test_dashboard_metrics.py

## Implementation Steps

1. Choose the rendering strategy: Plotly HTML snippet if plotly is installed via dashboard extra, or a simple SVG/table fallback.
2. Render curves for common metrics such as `train/loss`, `val/loss`, and all available metrics if feasible.
3. Ensure embedded chart output is self-contained.
4. Add empty-state text when no metrics are available.
5. Add tests that generated HTML contains metric names and a chart/table container.

## Acceptance Criteria

- Dashboard displays metric names from `metrics.csv`.
- Dashboard includes a visible metric curve or fallback metric table.
- No server is required.
- Missing metrics produce a readable empty state.

## Verification Commands

```bash
pytest -q tests/test_dashboard_metrics.py
python examples/basic_usage.py
```

## Non-goals

- Do not implement interactive run comparison charts.

## Handoff Notes

- Keep the slice small and focused.
- Preserve the public API already working after Week 2.
- Do not implement Week 4+ features unless this file explicitly asks for a placeholder.
- Prefer deterministic, file-based output over complex runtime behavior.
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
**Completed at:** 2026-05-09 22:53  
**Completed by:** coding agent  
**Verification command(s):** pytest -q tests/test_dashboard_metrics.py; python examples/basic_usage.py  
**Notes:** Completed with a self-contained metric table/curve-data fallback, no server required.  

<!-- AGENT_STATUS: COMPLETED -->
