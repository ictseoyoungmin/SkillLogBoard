---
week: 6
day: N
slice: "NN_slice_name"
title: "Slice Title"
priority: "P0"
status: "pending"
target_version: "v0.5-research-templates"
---

# NN_slice_name — Slice Title

## Objective

Describe the objective.

## Context

Explain context.

## Dependencies

- Previous slices in order

## Target Files

- path/to/file.py

## Implementation Steps

1. Step one.
2. Step two.

## Acceptance Criteria

- Criterion one.

## Verification Commands

```bash
pytest -q
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

