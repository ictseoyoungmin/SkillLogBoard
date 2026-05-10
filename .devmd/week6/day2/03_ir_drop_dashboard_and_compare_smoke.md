---
week: 6
day: 2
slice: "03_ir_drop_dashboard_and_compare_smoke"
title: "IR-drop dashboard and compare smoke"
priority: "P0"
status: "pending"
target_version: "v0.5-research-templates"
---

# 03_ir_drop_dashboard_and_compare_smoke — IR-drop dashboard and compare smoke

## Objective

Verify IR-drop runs work with dashboard/compare.

## Context

Templates should be compatible with Week 3-5 features.

## Dependencies

- Previous slices in order

## Target Files

- tests/test_ir_drop_template.py
- examples/ir_drop_example.py

## Implementation Steps

1. Generate temporary IR-drop runs.
2. Build dashboards.
3. Run compare using val/high_drop_f1.
4. Assert compare outputs.
5. Assert metric appears.

## Acceptance Criteria

- IR-drop runs work with compare.
- high_drop_f1 appears in outputs.

## Verification Commands

```bash
pytest -q tests/test_ir_drop_template.py
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

