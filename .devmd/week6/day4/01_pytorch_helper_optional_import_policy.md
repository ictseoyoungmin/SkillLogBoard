---
week: 6
day: 4
slice: "01_pytorch_helper_optional_import_policy"
title: "PyTorch helper optional import policy"
priority: "P0"
status: "pending"
target_version: "v0.5-research-templates"
---

# 01_pytorch_helper_optional_import_policy — PyTorch helper optional import policy

## Objective

Ensure PyTorch helpers remain optional.

## Context

Core must not require torch.

## Dependencies

- Previous slices in order

## Target Files

- src/skilllogboard/integrations/pytorch.py
- tests/test_optional_integrations.py
- pyproject.toml

## Implementation Steps

1. Review pytorch integration.
2. Use lazy/guarded imports.
3. Add only dependency-light helpers.
4. Test import without torch.
5. Confirm torch optional extra only.

## Acceptance Criteria

- Core import works without torch.
- Optional error message readable.

## Verification Commands

```bash
pytest -q tests/test_optional_integrations.py
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

