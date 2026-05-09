---
week: 4-cleanup
day: cleanup
slice: "06_finalize_dashboard_html_template_structure"
title: "finalize dashboard HTML template structure"
priority: "P1"
status: "completed"
target_version: "v0.3-cleanup"
---

# 06_finalize_dashboard_html_template_structure — finalize dashboard HTML template structure

## Objective

Finalize the dashboard template as a standalone static HTML file while preserving Week 4 Rule Audit output.

## Context

The dashboard template should be a valid HTML document before Week 5 compare dashboard work begins.

## Dependencies

- Week 4 completed

## Target Files

- src/skilllogboard/dashboards/templates/run.html.j2
- tests/test_dashboard_packaging.py
- tests/test_dashboard_rule_trace.py
- tests/test_dashboard_smoke.py

## Implementation Steps

1. Ensure `run.html.j2` begins with `<!doctype html>` and contains `<html>`, `<head>`, `<meta charset>`, `<title>`, and `<body>`.
2. Keep all existing dashboard sections including Rule Audit.
3. Keep CSS minimal and inline.
4. Ensure generated dashboard remains self-contained and file-system openable.
5. Strengthen tests to assert HTML structure and Rule Audit presence.
6. Run dashboard smoke tests.

## Acceptance Criteria

- Template has valid standalone HTML structure.
- Generated dashboard includes Rule Audit when skill_trace exists.
- Packaging test checks meaningful template content.
- Dashboard tests pass.

## Verification Commands

```bash
pytest -q tests/test_dashboard_packaging.py tests/test_dashboard_rule_trace.py tests/test_dashboard_smoke.py
```

## Non-goals

- Do not implement compare dashboard here.

## Handoff Notes

- Keep the slice small and focused.
- Preserve the public API already working after Week 4.
- Do not implement Week 6+ research plugins unless this slice explicitly asks for a placeholder.
- Do not hide unsupported or planned features in docs; label them clearly.
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
**Completed at:** 2026-05-10 00:36  
**Completed by:** coding agent  
**Verification command(s):** pytest -q tests/test_dashboard_packaging.py tests/test_dashboard_rule_trace.py tests/test_dashboard_smoke.py  
**Notes:** Completed and verified for the requested scope.

<!-- AGENT_STATUS: COMPLETED -->

