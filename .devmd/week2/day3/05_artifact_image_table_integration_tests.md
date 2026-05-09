---
week: 2
day: 3
slice: "05_artifact_image_table_integration_tests"
title: "artifact/image/table integration tests"
priority: "P1"
status: "completed"
target_version: "v0.1-mvp"
---

# 05_artifact_image_table_integration_tests — artifact/image/table integration tests

## Objective

Add integration tests that verify artifact, image, and table outputs work together in one run.

## Context

The summary and future dashboard will rely on consistent indexes and events. This slice verifies the writer stack as an integrated flow.

## Dependencies

- 01_artifact_store_index_and_metadata
- 03_image_writer_basic_png_support
- 04_table_writer_csv_html_support

## Target Files

- tests/test_artifact_integration.py
- src/skilllogboard/core/logger.py

## Implementation Steps

1. Create a temporary run with RunLogger.
2. Log one artifact file, one image file path, and one table.
3. Finish the run.
4. Assert output directories and indexes exist.
5. Assert event types include artifact, image, and table.
6. Assert manifest files map contains any newly required indexes if the implementation tracks them there.

## Acceptance Criteria

- Integrated artifact/image/table run completes successfully.
- Events are valid JSONL.
- Indexes are valid JSON where applicable.
- No optional dependency is required for the integration test.

## Verification Commands

```bash
pytest -q tests/test_artifact_integration.py
```

## Non-goals

- Do not implement dashboard artifact gallery here.

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
**Verification command(s):** pytest -q tests/test_artifact_integration.py  
**Notes:** Completed for Week 2 v0.1 MVP scope only.  

<!-- AGENT_STATUS: COMPLETED -->
