---
week: 2
day: 1
slice: "03_finish_fail_and_close_idempotency"
title: "finish/fail/close idempotency"
priority: "P0"
status: "completed"
target_version: "v0.1-mvp"
---

# 03_finish_fail_and_close_idempotency — finish/fail/close idempotency

## Objective

Make `finish()`, `fail()`, and optional `close()` safe to call more than once.

## Context

Agents, notebooks, and training scripts often call cleanup methods redundantly. The logger should not corrupt files or duplicate events if cleanup is called twice.

## Dependencies

- 01_runlogger_lifecycle_state_model
- 02_context_manager_success_and_failure

## Target Files

- src/skilllogboard/core/logger.py
- tests/test_logger_lifecycle.py

## Implementation Steps

1. Add an internal `_finished` or `_closed` flag if not already present.
2. Make `finish()` a no-op or safe update if called after completion.
3. Make `fail()` safe if called after a terminal state, but do not overwrite completed runs unless explicitly intended.
4. Add optional `close()` alias if useful for user ergonomics.
5. Add tests for double `finish()`, `finish()` after `fail()`, and `fail()` after `finish()`.

## Acceptance Criteria

- Double `finish()` does not duplicate completion events.
- Terminal status is stable after repeated cleanup calls.
- Manifest remains valid YAML after repeated calls.
- Events remain valid JSONL after repeated calls.

## Verification Commands

```bash
pytest -q tests/test_logger_lifecycle.py
```

## Non-goals

- Do not implement retention policy or artifact cleanup.

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
