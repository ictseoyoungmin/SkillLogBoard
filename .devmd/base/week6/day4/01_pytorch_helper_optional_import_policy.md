---
week: 6
day: 4
slice: "01_pytorch_helper_optional_import_policy"
title: "PyTorch helper optional import policy"
priority: "P0"
status: "completed"
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

- [x] Implementation completed
- [x] Acceptance criteria verified
- [x] Tests or smoke checks executed
- [x] No unrelated files changed
- [x] Notes added below if anything was skipped or deferred

**Status:** COMPLETED  
**Completed at:** 2026-05-10 19:51  
**Completed by:** coding agent  
**Verification command(s):** .venv/bin/pytest -q tests/test_optional_integrations.py tests/test_examples.py  
**Notes:** Added lazy PyTorch helper functions and clear optional dependency errors; torch remains optional.

<!-- AGENT_STATUS: COMPLETED -->
