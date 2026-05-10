---
week: 5-cleanup
day: cleanup
slice: "04_convert_compare_template_to_standalone_html"
title: "convert compare template to standalone HTML"
priority: "P0"
status: "pending"
target_version: "v0.4-cleanup"
---

# 04_convert_compare_template_to_standalone_html — convert compare template to standalone HTML

## Objective

Convert compare template to valid static HTML.

## Context

compare.html.j2 should be standalone HTML.

## Dependencies

- Week 5 completed

## Target Files

- src/skilllogboard/dashboards/templates/compare.html.j2
- tests/test_compare_report.py
- tests/test_dashboard_packaging.py

## Implementation Steps

1. Add doctype/html/head/meta/title/body.
2. Keep Leaderboard, Config Diff, Ablation Axes, Seed Summary.
3. Keep relative run dashboard links.
4. Update tests for structure.

## Acceptance Criteria

- compare.html contains doctype/html/head/body.
- All compare sections present.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_compare_report.py tests/test_dashboard_packaging.py
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

