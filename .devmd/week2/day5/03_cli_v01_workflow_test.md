---
week: 2
day: 5
slice: "03_cli_v01_workflow_test"
title: "CLI v0.1 workflow test"
priority: "P1"
status: "completed"
target_version: "v0.1-mvp"
---

# 03_cli_v01_workflow_test — CLI v0.1 workflow test

## Objective

Verify the CLI can inspect and regenerate report/dashboard for a v0.1 run.

## Context

The CLI should work on runs created by the Python API. This provides a useful after-the-fact workflow.

## Dependencies

- 02_v01_integration_test

## Target Files

- tests/test_cli_v01_workflow.py
- src/skilllogboard/cli/main.py

## Implementation Steps

1. Create a temporary run with RunLogger.
2. Call CLI `inspect` on the run directory.
3. Call CLI `report` on the run directory.
4. Call CLI `dashboard` on the run directory.
5. Assert commands exit successfully.
6. Assert generated files exist and are not empty.

## Acceptance Criteria

- CLI workflow test passes.
- `inspect`, `report`, and `dashboard` work on an existing run.
- CLI errors remain readable for missing paths.

## Verification Commands

```bash
pytest -q tests/test_cli_v01_workflow.py
```

## Non-goals

- Do not implement full compare CLI here.

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
**Verification command(s):** pytest -q tests/test_cli_v01_workflow.py  
**Notes:** Completed for Week 2 v0.1 MVP scope only.  

<!-- AGENT_STATUS: COMPLETED -->
