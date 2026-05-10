---
week: 6
day: 4
slice: "04_example_smoke_test_suite"
title: "example smoke test suite"
priority: "P0"
status: "pending"
target_version: "v0.5-research-templates"
---

# 04_example_smoke_test_suite — example smoke test suite

## Objective

Add smoke tests for lightweight examples.

## Context

Examples should not rot.

## Dependencies

- Previous slices in order

## Target Files

- tests/test_examples.py
- examples/basic_usage.py
- examples/ir_drop_example.py
- examples/trajectory_example.py

## Implementation Steps

1. Test basic_usage, ir_drop_example, trajectory_example.
2. Use temp output directories where practical.
3. Assert dashboard/report/skill_trace.
4. No internet or heavy deps.

## Acceptance Criteria

- Example smoke tests pass.
- No external data required.

## Verification Commands

```bash
pytest -q tests/test_examples.py
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

