---
week: 2
day: 5
slice: "02_v01_integration_test"
title: "v0.1 integration test"
priority: "P0"
status: "completed"
target_version: "v0.1-mvp"
---

# 02_v01_integration_test — v0.1 integration test

## Objective

Create an end-to-end test for the v0.1 single-run evidence package.

## Context

This is the main Week 2 acceptance test. It should verify the complete output package from the Python API.

## Dependencies

- 01_basic_usage_example_update

## Target Files

- tests/test_integration_v01.py
- tests/helpers.py

## Implementation Steps

1. Create a RunLogger in a `tmp_path` root.
2. Log config updates, multiple metrics, a note, an artifact, an image path if supported, and a table if supported.
3. Finish with report and dashboard enabled.
4. Assert required files exist.
5. Assert manifest status is completed.
6. Assert metrics CSV and events JSONL contain expected records.
7. Assert summary contains key run and metric information.

## Acceptance Criteria

- `pytest -q tests/test_integration_v01.py` passes.
- The test verifies all v0.1 core output files.
- The test is deterministic and does not require optional dependencies.

## Verification Commands

```bash
pytest -q tests/test_integration_v01.py
```

## Non-goals

- Do not test multi-run compare here.

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
**Verification command(s):** pytest -q tests/test_integration_v01.py  
**Notes:** Completed for Week 2 v0.1 MVP scope only.  

<!-- AGENT_STATUS: COMPLETED -->
