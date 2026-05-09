---
week: 5
day: 3
slice: "01_config_flattening_helper"
title: "config flattening helper"
priority: "P0"
status: "pending"
target_version: "v0.4-compare"
---

# 01_config_flattening_helper — config flattening helper

## Objective

Implement config flattening for diff and ablation axis extraction.

## Context

D23 requires config diff and ablation axis extraction. Nested config dictionaries should be flattened into stable dotted keys.

## Dependencies

- day1 run index slices

## Target Files

- src/skilllogboard/compare/config_diff.py
- tests/test_config_diff.py

## Implementation Steps

1. Implement `flatten_config(config, prefix='')`.
2. Use dotted keys such as `optimizer.lr`.
3. Represent lists/scalars in JSON/CSV-friendly form.
4. Handle empty config.
5. Add tests for nested dictionaries, lists, booleans, and strings.

## Acceptance Criteria

- Nested config is flattened deterministically.
- Scalar and list values are represented safely.
- Empty config returns empty dict.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_config_diff.py
```

## Non-goals

- Do not compute diff yet.

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

