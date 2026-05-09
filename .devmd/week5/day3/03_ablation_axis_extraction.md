---
week: 5
day: 3
slice: "03_ablation_axis_extraction"
title: "ablation axis extraction"
priority: "P0"
status: "pending"
target_version: "v0.4-compare"
---

# 03_ablation_axis_extraction — ablation axis extraction

## Objective

Extract likely ablation axes from config differences.

## Context

D23 calls out activation/norm/loss axis extraction. This slice should produce a general mechanism, not hardcode only one project.

## Dependencies

- 02_config_diff_table

## Target Files

- src/skilllogboard/compare/config_diff.py
- tests/test_config_diff.py

## Implementation Steps

1. Implement `extract_ablation_axes(records, candidate_keys=None)`.
2. If candidate_keys is provided, return variation for those keys.
3. If candidate_keys is absent, infer axes as flattened config keys with more than one distinct value.
4. Include distinct values and affected run counts.
5. Add tests for activation, norm, loss_name, lr examples.

## Acceptance Criteria

- Ablation axes include varying config keys.
- Distinct values are listed.
- Candidate key filtering works.
- Tests cover inferred and explicit axes.

## Verification Commands

```bash
pytest -q tests/test_config_diff.py
```

## Non-goals

- Do not compute statistical significance.

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

