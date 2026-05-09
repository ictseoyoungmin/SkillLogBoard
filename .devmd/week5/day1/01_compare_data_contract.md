---
week: 5
day: 1
slice: "01_compare_data_contract"
title: "compare data contract"
priority: "P0"
status: "pending"
target_version: "v0.4-compare"
---

# 01_compare_data_contract — compare data contract

## Objective

Define the data contract for multi-run comparison outputs.

## Context

Week 5 compares multiple run folders. Before implementation, define a stable in-memory representation for discovered runs, metrics, configs, best metrics, and warnings.

## Dependencies

- Week 4 cleanup completed

## Target Files

- src/skilllogboard/compare/run_index.py
- src/skilllogboard/compare/__init__.py
- tests/test_compare_index.py

## Implementation Steps

1. Define a lightweight `RunRecord` dataclass or dictionary schema.
2. Fields should include project, run_id, run_name, run_dir, status, created_at, updated_at, main_metric, best_metric, config, metrics summary, artifact count, warning/error counts if available.
3. Keep the representation JSON/CSV-friendly.
4. Add tests for constructing or loading a basic RunRecord.
5. Document assumptions in comments.

## Acceptance Criteria

- RunRecord or equivalent schema exists.
- Schema can represent completed and failed/partial runs.
- Schema includes manifest/config/metric fields needed by leaderboard and config diff.
- Tests pass without pandas.

## Verification Commands

```bash
pytest -q tests/test_compare_index.py
```

## Non-goals

- Do not implement leaderboard ranking in this slice.

## Handoff Notes

- Keep the slice small and focused.
- Preserve the public API already working after Week 4.
- Do not implement Week 6+ research plugins unless this slice explicitly asks for a placeholder.
- Do not hide unsupported or planned features in docs; label them clearly.
- If a blocker appears, document it in the Agent Completion Block instead of expanding scope.

---

## Agent Completion Block

> The agent must update this block after finishing the slice.

- [ ] Implementation completed
- [ ] Acceptance criteria verified
- [ ] Tests or smoke checks executed
- [ ] No unrelated files changed
- [ ] Notes added below if anything was skipped or deferred

**Status:** PENDING  
**Completed at:**  
**Completed by:**  
**Verification command(s):**  
**Notes:**  

<!-- AGENT_STATUS: PENDING -->

