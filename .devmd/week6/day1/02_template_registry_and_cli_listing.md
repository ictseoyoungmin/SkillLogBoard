---
week: 6
day: 1
slice: "02_template_registry_and_cli_listing"
title: "template registry and CLI listing"
priority: "P0"
status: "pending"
target_version: "v0.5-research-templates"
---

# 02_template_registry_and_cli_listing — template registry and CLI listing

## Objective

Expose templates from CLI.

## Context

Users should see implemented and planned templates.

## Dependencies

- Previous slices in order

## Target Files

- src/skilllogboard/plugins/registry.py
- src/skilllogboard/cli/main.py
- tests/test_cli_templates.py

## Implementation Steps

1. Add `skilllog templates` or equivalent.
2. Show name/status/description.
3. Show ir-drop and trajectory.
4. Show classification/segmentation/finance-dashboard as Planned.
5. Test output.

## Acceptance Criteria

- Template list command exits 0.
- Output includes implemented and planned templates.

## Verification Commands

```bash
pytest -q tests/test_cli_templates.py
skilllog templates || true
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

