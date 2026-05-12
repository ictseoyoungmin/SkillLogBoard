---
week: 5-cleanup
day: cleanup
slice: "05_compare_html_render_smoke_test_strengthening"
title: "compare HTML render smoke test strengthening"
priority: "P0"
status: "completed"
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

- [x] Implementation completed
- [x] Acceptance criteria verified
- [x] Tests or smoke checks executed
- [x] No unrelated files changed
- [x] Notes added below if anything was skipped or deferred

**Status:** COMPLETED  
**Completed at:** 2026-05-10 19:40  
**Completed by:** coding agent  
**Verification command(s):** .venv/bin/pytest -q tests/test_dashboard_smoke.py tests/test_compare_report.py tests/test_dashboard_packaging.py tests/test_dashboard_rule_trace.py; .venv/bin/pytest -q  
**Notes:** Added no-browser HTML document and core-section assertions for dashboard and compare outputs.

<!-- AGENT_STATUS: COMPLETED -->
