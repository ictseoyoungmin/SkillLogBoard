---
week: 2
day: 2
slice: "01_log_metric_scalar_validation"
title: "log_metric scalar validation"
priority: "P0"
status: "completed"
target_version: "v0.1-mvp"
---

# 01_log_metric_scalar_validation — log_metric scalar validation

## Objective

Make `log_metric(name, value, step)` reliable and validate scalar inputs.

## Context

Metrics are the core data source for summary and dashboard generation. Week 2 should guarantee that simple numeric metrics are written consistently to both CSV and event logs.

## Dependencies

- week2/day1 lifecycle slices

## Target Files

- src/skilllogboard/core/logger.py
- src/skilllogboard/writers/csv_writer.py
- tests/test_logger_metrics.py

## Implementation Steps

1. Ensure `log_metric()` accepts int and float values.
2. Convert values to a JSON/CSV-safe numeric representation.
3. Reject or clearly handle non-scalar values with a readable error.
4. Ensure `step` may be `None` or an integer.
5. Write a metric row to `metrics.csv`.
6. Write a metric event to `events.jsonl`.
7. Add unit/integration tests.

## Acceptance Criteria

- `logger.log_metric('val/acc', 0.9, step=1)` writes CSV and JSONL records.
- Metric event contains type `metric`, key, value, step, and metadata.
- Invalid metric values produce a clear exception.
- Tests verify both output files.

## Verification Commands

```bash
pytest -q tests/test_logger_metrics.py
```

## Non-goals

- Do not implement tensor/numpy serialization here.

## Handoff Notes

- Keep this slice focused on Week 2 MVP behavior.
- Preserve the public API described in the docs unless this slice explicitly changes it.
- Prefer backward-compatible changes to the Week 1 skeleton.
- Do not start Week 3 dashboard work beyond the placeholder hooks required by `finish()`.
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
**Completed at:** 2026-05-09 22:20  
**Completed by:** coding agent  
**Verification command(s):** pytest -q tests/test_logger_metrics.py  
**Notes:** Completed for Week 2 v0.1 MVP scope only.  

<!-- AGENT_STATUS: COMPLETED -->
