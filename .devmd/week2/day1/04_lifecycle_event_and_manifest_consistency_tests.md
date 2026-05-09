---
week: 2
day: 1
slice: "04_lifecycle_event_and_manifest_consistency_tests"
title: "lifecycle event and manifest consistency tests"
priority: "P1"
status: "completed"
target_version: "v0.1-mvp"
---

# 04_lifecycle_event_and_manifest_consistency_tests — lifecycle event and manifest consistency tests

## Objective

Add regression tests that verify lifecycle events and manifest status remain consistent.

## Context

Week 2 should establish confidence that lifecycle state and event logs agree. This prevents future dashboard/report modules from reading contradictory state.

## Dependencies

- 03_finish_fail_and_close_idempotency

## Target Files

- tests/test_logger_lifecycle.py
- tests/helpers.py

## Implementation Steps

1. Add a small helper to read JSONL event files in tests.
2. Test that a successful run has start and finish/completed lifecycle events.
3. Test that a failed run has start and fail lifecycle events.
4. Test that manifest status matches the final lifecycle event.
5. Keep tests independent of dashboard implementation details.

## Acceptance Criteria

- Lifecycle tests can parse `events.jsonl`.
- Manifest final status matches the lifecycle event sequence.
- Tests pass without optional dependencies.

## Verification Commands

```bash
pytest -q tests/test_logger_lifecycle.py
```

## Non-goals

- Do not add dashboard snapshot tests here.

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
**Verification command(s):** pytest -q tests/test_logger_lifecycle.py  
**Notes:** Completed for Week 2 v0.1 MVP scope only.  

<!-- AGENT_STATUS: COMPLETED -->
