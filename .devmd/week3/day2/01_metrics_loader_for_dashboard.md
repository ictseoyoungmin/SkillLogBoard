---
week: 3
day: 2
slice: "01_metrics_loader_for_dashboard"
title: "metrics loader for dashboard"
priority: "P0"
status: "completed"
target_version: "v0.2-dashboard"
---

# 01_metrics_loader_for_dashboard — metrics loader for dashboard

## Objective

Implement a dependency-light metrics loader for dashboard panels.

## Context

Metric curves and metric tables must be generated from `metrics.csv` without requiring pandas.

## Dependencies

- day1/01_dashboard_data_contract

## Target Files

- src/skilllogboard/dashboards/components.py
- src/skilllogboard/dashboards/static_builder.py
- tests/test_dashboard_metrics.py

## Implementation Steps

1. Create or refine a function to read `metrics.csv` using the standard library `csv` module.
2. Return metrics grouped by metric name.
3. Preserve step, value, timestamp, group, and metadata where available.
4. Handle empty or missing metrics.csv.
5. Add tests for multiple metric names and multiple steps.

## Acceptance Criteria

- Metrics loader returns grouped metric series.
- Numeric values are parsed as floats.
- Missing metrics file results in an empty state rather than a crash.
- Tests pass without pandas.

## Verification Commands

```bash
pytest -q tests/test_dashboard_metrics.py
```

## Non-goals

- Do not compute aggregate statistics beyond what panels need.

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
**Verification command(s):** pytest -q tests/test_dashboard_metrics.py  
**Notes:** Completed for Week 3 v0.2 dashboard scope.  

<!-- AGENT_STATUS: COMPLETED -->
