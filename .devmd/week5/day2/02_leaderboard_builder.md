---
week: 5
day: 2
slice: "02_leaderboard_builder"
title: "leaderboard builder"
priority: "P0"
status: "pending"
target_version: "v0.4-compare"
---

# 02_leaderboard_builder — leaderboard builder

## Objective

Build a leaderboard table from multiple run records.

## Context

Users need a top-level comparison table ordered by a chosen metric.

## Dependencies

- 01_metric_aggregation_helpers

## Target Files

- src/skilllogboard/compare/leaderboard.py
- tests/test_leaderboard.py

## Implementation Steps

1. Implement `build_leaderboard(records, metric=None, mode=None, value_source='best_or_latest')`.
2. Include columns: rank, run_id, run_name, status, metric_name, metric_value, best_step, created_at, warning_count, error_count.
3. Sort by metric value using mode max/min.
4. Place missing metric values at the bottom.
5. Add tests for max/min sorting and missing values.

## Acceptance Criteria

- Leaderboard ranks runs correctly for max mode.
- Leaderboard ranks runs correctly for min mode.
- Missing values appear after valid values.
- Table rows are CSV/Markdown friendly dicts.

## Verification Commands

```bash
pytest -q tests/test_leaderboard.py
```

## Non-goals

- Do not render HTML in this slice.

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

