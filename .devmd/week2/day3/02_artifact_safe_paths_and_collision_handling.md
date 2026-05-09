---
week: 2
day: 3
slice: "02_artifact_safe_paths_and_collision_handling"
title: "artifact safe paths and collision handling"
priority: "P0"
status: "completed"
target_version: "v0.1-mvp"
---

# 02_artifact_safe_paths_and_collision_handling — artifact safe paths and collision handling

## Objective

Prevent unsafe artifact paths and accidental overwrites.

## Context

Artifact names may contain spaces or unsafe characters. Multiple artifacts may have the same source basename. The store must choose safe relative paths.

## Dependencies

- 01_artifact_store_index_and_metadata

## Target Files

- src/skilllogboard/core/artifact_store.py
- tests/test_artifacts.py

## Implementation Steps

1. Add a safe name helper for artifact names and filenames.
2. Prevent path traversal such as `../../file` from escaping the run directory.
3. When an artifact destination already exists, append a numeric suffix or use a deterministic collision strategy.
4. Record the final relative path in artifact metadata.
5. Add tests for duplicate artifact names, unsafe names, and path traversal attempts.

## Acceptance Criteria

- Artifact paths never escape the run directory.
- Duplicate artifacts do not overwrite each other silently.
- Unsafe names are normalized to safe filenames.
- Tests cover collisions and unsafe paths.

## Verification Commands

```bash
pytest -q tests/test_artifacts.py
```

## Non-goals

- Do not implement content-addressable storage in Week 2.

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
**Verification command(s):** pytest -q tests/test_artifacts.py  
**Notes:** Completed for Week 2 v0.1 MVP scope only.  

<!-- AGENT_STATUS: COMPLETED -->
