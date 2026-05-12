---
week: 2
day: 2
slice: "02_log_metrics_batch_behavior"
title: "log_metrics batch behavior"
priority: "P0"
status: "completed"
target_version: "v0.1-mvp"
---

# 02_log_metrics_batch_behavior — log_metrics batch behavior

## Objective

Implement `log_metrics(dict, step)` as a stable batch wrapper around `log_metric`.

## Context

The primary usage pattern in docs uses `logger.log_metrics({...}, step=epoch)`. This method should preserve metric names and write one record per metric.

## Dependencies

- 01_log_metric_scalar_validation

## Target Files

- src/skilllogboard/core/logger.py
- tests/test_logger_metrics.py

## Implementation Steps

1. Implement `log_metrics(metrics: dict[str, float], step=None, **metadata)`.
2. Call `log_metric()` for each metric to keep behavior consistent.
3. Preserve insertion order where Python dict order is available.
4. Pass shared metadata to each metric event/row.
5. Add tests for multiple metrics and shared metadata.

## Acceptance Criteria

- Batch logging writes one CSV row per metric.
- Batch logging writes one JSONL event per metric.
- Shared metadata appears in each metric record.
- `log_metrics({})` is safe or produces a clear no-op behavior.

## Verification Commands

```bash
pytest -q tests/test_logger_metrics.py
```

## Non-goals

- Do not implement asynchronous metric buffering.

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
