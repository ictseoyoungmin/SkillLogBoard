---
week: 6
day: 1
slice: "03_init_template_workspace_generation"
title: "init template workspace generation"
priority: "P0"
status: "pending"
target_version: "v0.5-research-templates"
---

# 03_init_template_workspace_generation — init template workspace generation

## Objective

Implement `skilllog init --template <name>`.

## Context

Template init should create safe workspace files.

## Dependencies

- Previous slices in order

## Target Files

- src/skilllogboard/cli/main.py
- src/skilllogboard/plugins/registry.py
- tests/test_cli_templates.py

## Implementation Steps

1. Extend init with --template.
2. For implemented templates, create Skills.md and optional config.
3. Do not overwrite existing files.
4. For Planned templates, print clear message.
5. Test implemented and planned behavior.

## Acceptance Criteria

- ir-drop and trajectory init create files.
- Planned template init is explicit.
- Existing Skills.md not overwritten.

## Verification Commands

```bash
pytest -q tests/test_cli_templates.py
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

