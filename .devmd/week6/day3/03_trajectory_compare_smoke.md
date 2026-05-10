---
week: 6
day: 3
slice: "03_trajectory_compare_smoke"
title: "trajectory compare smoke"
priority: "P0"
status: "pending"
target_version: "v0.5-research-templates"
---

# 03_trajectory_compare_smoke — trajectory compare smoke

## Objective

Verify trajectory runs work with compare.

## Context

Template outputs should work with Week 5 compare.

## Dependencies

- Previous slices in order

## Target Files

- tests/test_trajectory_template.py
- examples/trajectory_example.py

## Implementation Steps

1. Generate temporary trajectory runs.
2. Run compare using val/pb_score.
3. Assert compare outputs.
4. Assert PB score appears.

## Acceptance Criteria

- Trajectory compare test passes.
- val/pb_score appears in outputs.

## Verification Commands

```bash
pytest -q tests/test_trajectory_template.py
```

## Non-goals

- Do not implement unrelated future features.

## Handoff Notes

- Keep the slice small and focused.
- Preserve the public API already working after Week 5.
- Keep optional integrations optional; core install must not require heavy ML packages.
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

