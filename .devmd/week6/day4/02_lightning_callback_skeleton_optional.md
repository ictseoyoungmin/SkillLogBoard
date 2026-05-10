---
week: 6
day: 4
slice: "02_lightning_callback_skeleton_optional"
title: "Lightning callback skeleton optional"
priority: "P0"
status: "pending"
target_version: "v0.5-research-templates"
---

# 02_lightning_callback_skeleton_optional — Lightning callback skeleton optional

## Objective

Provide optional Lightning callback skeleton.

## Context

Lightning should not be required.

## Dependencies

- Previous slices in order

## Target Files

- src/skilllogboard/integrations/lightning.py
- tests/test_optional_integrations.py
- docs/templates.md

## Implementation Steps

1. Implement guarded callback/factory.
2. Do not import lightning at module import time unguarded.
3. Document optional nature.
4. Skip tests when unavailable.

## Acceptance Criteria

- Core tests pass without Lightning.
- Optional dependency error is clear.

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

