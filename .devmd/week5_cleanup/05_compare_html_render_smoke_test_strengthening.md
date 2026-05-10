---
week: 5-cleanup
day: cleanup
slice: "05_compare_html_render_smoke_test_strengthening"
title: "compare HTML render smoke test strengthening"
priority: "P0"
status: "pending"
target_version: "v0.4-cleanup"
---

# 05_compare_html_render_smoke_test_strengthening — compare HTML render smoke test strengthening

## Objective

Strengthen tests against pseudo-HTML regressions.

## Context

HTML outputs should be tested as document artifacts.

## Dependencies

- Week 5 completed

## Target Files

- tests/test_dashboard_smoke.py
- tests/test_compare_report.py
- tests/test_dashboard_packaging.py

## Implementation Steps

1. Add helper assertions for HTML structure.
2. Assert dashboard core sections.
3. Assert compare core sections.
4. Avoid browser dependencies.
5. Run full tests.

## Acceptance Criteria

- Dashboard and compare HTML structure tested.
- Core section names tested.
- No browser dependency introduced.

## Verification Commands

```bash
pytest -q tests/test_dashboard_smoke.py tests/test_compare_report.py tests/test_dashboard_packaging.py
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

