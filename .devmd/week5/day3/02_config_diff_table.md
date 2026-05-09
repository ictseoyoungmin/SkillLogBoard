---
week: 5
day: 3
slice: "02_config_diff_table"
title: "config diff table"
priority: "P0"
status: "pending"
target_version: "v0.4-compare"
---

# 02_config_diff_table — config diff table

## Objective

Build a table showing config keys that differ across runs.

## Context

Config diff helps users identify ablation axes without manually opening config.yaml.

## Dependencies

- 01_config_flattening_helper

## Target Files

- src/skilllogboard/compare/config_diff.py
- tests/test_config_diff.py

## Implementation Steps

1. Implement `build_config_diff(records, include_constant=False)`.
2. Compare flattened config keys across run records.
3. Return rows with key and per-run values, or key/value variation summary.
4. By default, include only keys with more than one distinct value.
5. Add tests for differing and constant keys.

## Acceptance Criteria

- Diff table includes keys that vary across runs.
- Constant keys are excluded by default.
- `include_constant=True` includes constant keys.
- Tests verify per-run value output or variation summary.

## Verification Commands

```bash
pytest -q tests/test_config_diff.py
```

## Non-goals

- Do not render compare.html here.

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

