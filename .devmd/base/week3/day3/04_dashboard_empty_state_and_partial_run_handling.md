---
week: 3
day: 3
slice: "04_dashboard_empty_state_and_partial_run_handling"
title: "dashboard empty state and partial run handling"
priority: "P1"
status: "completed"
target_version: "v0.2-dashboard"
---

# 04_dashboard_empty_state_and_partial_run_handling — dashboard empty state and partial run handling

## Objective

Make dashboard generation robust for incomplete or partial run folders.

## Context

Users may inspect failed or incomplete runs. The dashboard should degrade gracefully instead of crashing.

## Dependencies

- day1-day3 dashboard components

## Target Files

- src/skilllogboard/dashboards/static_builder.py
- src/skilllogboard/dashboards/templates/run.html.j2
- tests/test_dashboard_partial_runs.py

## Implementation Steps

1. Create tests for a run directory missing metrics.csv.
2. Create tests for a run directory missing artifact_index.json.
3. Create tests for a failed manifest status.
4. Render warning/empty-state messages in the dashboard.
5. Ensure dashboard generation still writes HTML for partial runs.

## Acceptance Criteria

- Dashboard builds for partial run folders.
- Missing optional files are represented with warnings or empty states.
- Failed run status is visible in the dashboard.

## Verification Commands

```bash
pytest -q tests/test_dashboard_partial_runs.py
```

## Non-goals

- Do not implement full failed-run recovery logic.

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
**Verification command(s):** pytest -q tests/test_dashboard_partial_runs.py  
**Notes:** Completed for Week 3 v0.2 dashboard scope.  

<!-- AGENT_STATUS: COMPLETED -->
