---
week: 5-cleanup
day: cleanup
slice: "03_convert_run_dashboard_template_to_standalone_html"
title: "convert run dashboard template to standalone HTML"
priority: "P0"
status: "pending"
target_version: "v0.4-cleanup"
---

# 03_convert_run_dashboard_template_to_standalone_html — convert run dashboard template to standalone HTML

## Objective

Convert run dashboard template to valid HTML document.

## Context

run.html.j2 still looks Markdown-like.

## Dependencies

- Week 5 completed

## Target Files

- src/skilllogboard/dashboards/templates/run.html.j2
- tests/test_dashboard_packaging.py
- tests/test_dashboard_smoke.py
- tests/test_dashboard_rule_trace.py

## Implementation Steps

1. Add doctype/html/head/meta/title/body.
2. Keep Run Summary, Metrics, Config, Artifacts, Files, Rule Audit.
3. Add minimal inline CSS only.
4. Update tests for structure and sections.

## Acceptance Criteria

- dashboard.html contains doctype/html/head/body.
- Rule Audit remains visible when skill_trace exists.
- Dashboard tests pass.

## Verification Commands

```bash
pytest -q tests/test_dashboard_packaging.py tests/test_dashboard_smoke.py tests/test_dashboard_rule_trace.py
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

