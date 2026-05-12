---
week: 2
day: 3
slice: "01_artifact_store_index_and_metadata"
title: "artifact store index and metadata"
priority: "P0"
status: "completed"
target_version: "v0.1-mvp"
---

# 01_artifact_store_index_and_metadata — artifact store index and metadata

## Objective

Implement a useful artifact store with `artifact_index.json` metadata.

## Context

Week 1 may have a placeholder artifact store. Week 2 should make artifacts traceable with name, source, relative path, copy mode, size, and timestamp.

## Dependencies

- week2/day1 lifecycle
- week2/day2 metric/config slices

## Target Files

- src/skilllogboard/core/artifact_store.py
- src/skilllogboard/core/logger.py
- tests/test_artifacts.py

## Implementation Steps

1. Create or refine `ArtifactStore`.
2. Create `artifacts/` under the run directory.
3. Implement `log_artifact(name, path, copy=True)`.
4. When `copy=True`, copy the file into `artifacts/` using a safe filename.
5. When `copy=False`, record the source path without copying or create a lightweight link record if symlinks are intentionally avoided.
6. Write or update `artifact_index.json`.
7. Emit artifact events from RunLogger.
8. Add tests for copy mode and reference/link mode.

## Acceptance Criteria

- `artifact_index.json` is created and updated.
- Copied artifacts exist under the run folder.
- Reference-mode artifacts preserve the original path in metadata.
- Artifact events include name and relative path or source path.

## Verification Commands

```bash
pytest -q tests/test_artifacts.py
```

## Non-goals

- Do not implement cloud artifact storage.

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
