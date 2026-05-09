---
week: 3-cleanup
day: cleanup
slice: "02_valid_html_template_and_packaging_test_cleanup"
title: "valid HTML template and packaging test cleanup"
priority: "P0"
status: "completed"
target_version: "v0.2-cleanup"
---

# 02_valid_html_template_and_packaging_test_cleanup — valid HTML template and packaging test cleanup

## Objective

Make the dashboard template a valid standalone HTML document and strengthen packaging tests.

## Context

The dashboard template should include doctype/html/head/body and packaging tests should assert real content.

## Dependencies

- Week 3 completed

## Target Files

- src/skilllogboard/dashboards/templates/run.html.j2
- tests/test_dashboard_packaging.py
- src/skilllogboard/dashboards/static_builder.py

## Implementation Steps

1. Add `<!doctype html>`, `<html>`, `<head>`, `<meta charset>`, `<title>`, minimal `<style>`, and `<body>` to `run.html.j2`.
2. Keep sections: Run Summary, Metrics, Config, Artifacts, Files.
3. Update packaging tests to assert actual template content.
4. Recommended assertions: `SkillLogBoard Dashboard`, `Run Summary`, `Metrics`, `<html`, `<!doctype html>`.
5. Ensure package template loading still works.

## Acceptance Criteria

- Dashboard template is standalone HTML.
- Packaging test no longer uses trivially true assertions.
- Generated dashboard still contains all core sections.
- Packaging/render/smoke tests pass.

## Verification Commands

```bash
pytest -q tests/test_dashboard_packaging.py tests/test_dashboard_render.py tests/test_dashboard_smoke.py
```

## Non-goals

- Do not implement final visual polish.

## Handoff Notes

- Keep the slice small and focused.
- Preserve the public API already working after Week 3.
- Do not implement Week 5+ features unless this file explicitly asks for a placeholder.
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
**Completed at:** 2026-05-09 23:49  
**Completed by:** coding agent  
**Verification command(s):** pytest -q tests/test_dashboard_packaging.py tests/test_dashboard_render.py tests/test_dashboard_smoke.py  
**Notes:** Dashboard template validity and packaging smoke checks passed.

<!-- AGENT_STATUS: COMPLETED -->

