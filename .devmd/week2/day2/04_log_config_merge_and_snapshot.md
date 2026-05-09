---
week: 2
day: 2
slice: "04_log_config_merge_and_snapshot"
title: "log_config merge and snapshot"
priority: "P0"
status: "completed"
target_version: "v0.1-mvp"
---

# 04_log_config_merge_and_snapshot — log_config merge and snapshot

## Objective

Make `log_config(config)` update `config.yaml` and emit a config event.

## Context

Users may construct a RunLogger with a base config and later update or add fields. The config snapshot should remain readable and stable.

## Dependencies

- week1 config capture slices

## Target Files

- src/skilllogboard/core/logger.py
- src/skilllogboard/core/config_capture.py
- tests/test_logger_config.py

## Implementation Steps

1. Implement `log_config(config: dict)` to merge new keys into the current config.
2. For nested dictionaries, decide and document whether the merge is shallow or deep. Prefer shallow for MVP unless deep merge is already implemented.
3. Write the updated config to `config.yaml`.
4. Emit a config event to `events.jsonl`.
5. Update relevant manifest fields such as model_name, dataset_name, and seed if these keys change.
6. Add tests for initial config, updated config, and Unicode values.

## Acceptance Criteria

- `config.yaml` reflects updates after `log_config()`.
- Config update emits an event.
- Manifest metadata stays aligned with config where applicable.
- Tests verify YAML load-back behavior.

## Verification Commands

```bash
pytest -q tests/test_logger_config.py
```

## Non-goals

- Do not implement required_config validation; that belongs to Skills.md rule engine.

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
**Verification command(s):** pytest -q tests/test_logger_config.py  
**Notes:** Completed for Week 2 v0.1 MVP scope only.  

<!-- AGENT_STATUS: COMPLETED -->
