---
week: 1
day: 4
slice: "03_event_jsonl_writer_tests"
title: "event and JSONL writer integration tests"
priority: "P1"
status: "completed"
target_version: "v0.1-dev"
---

# 03_event_jsonl_writer_tests — event and JSONL writer integration tests

## Objective

Add integration tests that write Event objects through JsonlWriter.

## Context

This slice verifies the connection between the event schema and append-only JSONL persistence.

## Dependencies

- 01_event_dataclass_schema
- 02_jsonl_writer_append_flush

## Target Files

- tests/test_events.py
- tests/test_jsonl_writer.py

## Implementation Steps

1. Create an Event with type `metric` and write it through JsonlWriter.
2. Create lifecycle and artifact events and write them.
3. Read lines back and validate key fields.
4. Assert no trailing invalid line exists.

## Acceptance Criteria

- Event objects can be written directly via JsonlWriter.
- Roundtrip checks validate type, key, value, and metadata.
- The test suite passes without optional dependencies.

## Verification Commands

```bash
pytest -q tests/test_events.py tests/test_jsonl_writer.py
```

## Non-goals

- Do not test RunLogger here; that belongs to Day 5 integration.

## Handoff Notes

- Keep changes minimal and local to the target files.
- Prefer simple, explicit implementation over clever abstractions.
- Do not implement future-week features unless explicitly required by this slice.
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
**Completed at:** 2026-05-09 21:49  
**Completed by:** coding agent  
**Verification command(s):** pytest -q tests/test_events.py tests/test_jsonl_writer.py  
**Notes:** Completed for Week 1 scope only.  

<!-- AGENT_STATUS: COMPLETED -->
