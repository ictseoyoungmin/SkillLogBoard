---
week: 5
day: 1
slice: "04_run_index_build_and_export_json"
title: "run index build and JSON export"
priority: "P1"
status: "completed"
target_version: "v0.4-compare"
---

# 04_run_index_build_and_export_json — run index build and JSON export

## Objective

Build a multi-run index and optionally export it as JSON for debugging.

## Context

A debug JSON index makes Week 5 compare implementation easier to inspect and test.

## Dependencies

- 03_manifest_config_metric_indexer

## Target Files

- src/skilllogboard/compare/run_index.py
- tests/test_compare_index.py

## Implementation Steps

1. Implement `build_run_index(root_dir)` returning list of run records.
2. Implement optional `save_run_index(records, path)` or internal helper.
3. Ensure records are JSON-serializable.
4. Add tests for multiple run records and JSON serialization.

## Acceptance Criteria

- `build_run_index()` returns records for all discovered runs.
- Records can be JSON dumped.
- Ordering is deterministic.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_compare_index.py
```

## Non-goals

- Do not create compare.html yet.

## Handoff Notes

- Keep the slice small and focused.
- Preserve the public API already working after Week 4.
- Do not implement Week 6+ research plugins unless this slice explicitly asks for a placeholder.
- Do not hide unsupported or planned features in docs; label them clearly.
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
**Completed at:** 2026-05-10 00:36  
**Completed by:** coding agent  
**Verification command(s):** pytest -q tests/test_compare_index.py  
**Notes:** Completed and verified for the requested scope.

<!-- AGENT_STATUS: COMPLETED -->

