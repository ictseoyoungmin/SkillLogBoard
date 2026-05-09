---
week: 5
day: 4
slice: "02_seed_metric_aggregation"
title: "seed metric aggregation"
priority: "P0"
status: "pending"
target_version: "v0.4-compare"
---

# 02_seed_metric_aggregation — seed metric aggregation

## Objective

Aggregate metric values across seed groups.

## Context

This computes mean, std, count, best, median for metric values by group.

## Dependencies

- 01_seed_detection_and_group_key

## Target Files

- src/skilllogboard/compare/seed_group.py
- tests/test_seed_group.py

## Implementation Steps

1. Implement `group_runs_by_seed(records, metric, mode)` or equivalent.
2. Collect metric values per group.
3. Compute count, mean, std, median, best value, best run id.
4. Use standard library only for MVP.
5. Handle missing metric values gracefully.
6. Add tests for count/mean/std/median/best.

## Acceptance Criteria

- Aggregation computes count, mean, std, median.
- Best value respects max/min mode.
- Missing metric values do not crash aggregation.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_seed_group.py
```

## Non-goals

- Do not implement confidence intervals.

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

