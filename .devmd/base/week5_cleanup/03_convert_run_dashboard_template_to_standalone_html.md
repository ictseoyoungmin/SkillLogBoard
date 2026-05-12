---
week: 5-cleanup
day: cleanup
slice: "03_convert_run_dashboard_template_to_standalone_html"
title: "convert run dashboard template to standalone HTML"
priority: "P0"
status: "completed"
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

- [x] Implementation completed
- [x] Acceptance criteria verified
- [x] Tests or smoke checks executed
- [x] No unrelated files changed
- [x] Notes added below if anything was skipped or deferred

**Status:** COMPLETED  
**Completed at:** 2026-05-10 19:40  
**Completed by:** coding agent  
**Verification command(s):** .venv/bin/pytest -q tests/test_dashboard_smoke.py tests/test_compare_report.py tests/test_dashboard_packaging.py tests/test_dashboard_rule_trace.py; .venv/bin/pytest -q  
**Notes:** Run dashboard template was already standalone HTML; strengthened tests to assert document structure and core sections.

<!-- AGENT_STATUS: COMPLETED -->
