---
week: 5
day: 2
slice: "01_metric_aggregation_helpers"
title: "metric aggregation helpers"
priority: "P0"
status: "pending"
target_version: "v0.4-compare"
---

# 01_metric_aggregation_helpers — metric aggregation helpers

## Objective

Implement helper functions to extract metric values for leaderboard and comparison.

## Context

D22 requires leaderboard and metric aggregation. Aggregation should support best metric and latest metric values.

## Dependencies

- day1 run index slices

## Target Files

- src/skilllogboard/compare/leaderboard.py
- tests/test_leaderboard.py

## Implementation Steps

1. Implement helpers to get latest metric value by name from a RunRecord.
2. Implement helpers to get best metric value from manifest.best_metric.
3. Support metric mode `max` or `min` for sorting.
4. Handle missing metric values with `None` and stable ordering.
5. Add tests for latest/best extraction.

## Acceptance Criteria

- Latest metric extraction works.
- Best metric extraction works.
- Missing metrics are handled.
- Mode-aware sort direction is defined.

## Verification Commands

```bash
pytest -q tests/test_leaderboard.py
```

## Non-goals

- Do not implement seed grouping here.

## Handoff Notes

- Keep the slice small and focused.
- Preserve the public API already working after Week 4.
- Do not implement Week 6+ research plugins unless this slice explicitly asks for a placeholder.
- Do not hide unsupported or planned features in docs; label them clearly.
- If a blocker appears, document it in the Agent Completion Block instead of expanding scope.

---

## Agent Completion Block

> The agent must update this block after finishing the slice.

- [ ] Implementation completed
- [ ] Acceptance criteria verified
- [ ] Tests or smoke checks executed
- [ ] No unrelated files changed
- [ ] Notes added below if anything was skipped or deferred

**Status:** PENDING  
**Completed at:**  
**Completed by:**  
**Verification command(s):**  
**Notes:**  

<!-- AGENT_STATUS: PENDING -->

