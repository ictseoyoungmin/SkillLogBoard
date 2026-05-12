---
week: 1
day: 4
slice: "01_event_dataclass_schema"
title: "event dataclass schema"
priority: "P0"
status: "completed"
target_version: "v0.1-dev"
---

# 01_event_dataclass_schema — event dataclass schema

## Objective

Implement the append-only event schema.

## Context

`events.jsonl` should capture lifecycle, metric, artifact, note, config, and rule events in a uniform structure.

## Dependencies

- day1/02_src_layout_and_public_api

## Target Files

- src/skilllogboard/core/events.py
- tests/test_events.py

## Implementation Steps

1. Create an `Event` dataclass.
2. Include fields: timestamp, step, type, key, value, path, metadata.
3. Use ISO timestamp default.
4. Implement `to_dict()`.
5. Add tests for minimal and full event serialization.

## Acceptance Criteria

- Event serialization returns a JSON-compatible dictionary.
- Missing optional fields are represented safely.
- Timestamp is automatically set.
- Metadata defaults to an empty dict.

## Verification Commands

```bash
pytest -q tests/test_events.py
```

## Non-goals

- Do not implement rule-specific event logic here.

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
**Verification command(s):** pytest -q tests/test_events.py  
**Notes:** Completed for Week 1 scope only.  

<!-- AGENT_STATUS: COMPLETED -->
