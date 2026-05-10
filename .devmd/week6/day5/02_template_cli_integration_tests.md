---
week: 6
day: 5
slice: "02_template_cli_integration_tests"
title: "template CLI integration tests"
priority: "P0"
status: "pending"
target_version: "v0.5-research-templates"
---

# 02_template_cli_integration_tests — template CLI integration tests

## Objective

Test CLI template listing/init end-to-end.

## Context

CLI template commands are main Week 6 deliverables.

## Dependencies

- Previous slices in order

## Target Files

- tests/test_cli_templates.py
- src/skilllogboard/cli/main.py

## Implementation Steps

1. Test template listing.
2. Test init --template ir-drop.
3. Test init --template trajectory.
4. Test planned template behavior.
5. Assert generated Skills.md parses.

## Acceptance Criteria

- Template CLI tests pass.
- Planned behavior explicit.

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

