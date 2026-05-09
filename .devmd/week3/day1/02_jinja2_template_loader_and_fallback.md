---
week: 3
day: 1
slice: "02_jinja2_template_loader_and_fallback"
title: "Jinja2 template loader and fallback"
priority: "P0"
status: "completed"
target_version: "v0.2-dashboard"
---

# 02_jinja2_template_loader_and_fallback — Jinja2 template loader and fallback

## Objective

Implement a template rendering path for dashboard.html with a graceful fallback if Jinja2 is unavailable.

## Context

Jinja2 is part of the dashboard extra, but the package should fail gracefully or generate a minimal fallback dashboard when the optional extra is missing.

## Dependencies

- 01_dashboard_data_contract

## Target Files

- src/skilllogboard/dashboards/static_builder.py
- src/skilllogboard/dashboards/templates/run.html.j2
- pyproject.toml
- tests/test_dashboard_render.py

## Implementation Steps

1. Confirm `jinja2` is included in the `dashboard` optional extra.
2. Implement a template loading helper using package resources or a reliable path.
3. Create or update `run.html.j2` as the single-run dashboard template.
4. If Jinja2 import fails, render a minimal plain HTML fallback with clear message.
5. Add tests for normal rendering path where Jinja2 is installed.

## Acceptance Criteria

- `build_dashboard(run_dir)` writes `dashboard.html`.
- Dashboard generation works when installed with `.[dashboard]`.
- The template is packaged and accessible after editable install.
- Fallback path is documented or tested where practical.

## Verification Commands

```bash
pip install -e ".[dev,dashboard]"
pytest -q tests/test_dashboard_render.py
```

## Non-goals

- Do not implement Plotly metric curves yet.

## Handoff Notes

- Keep the slice small and focused.
- Preserve the public API already working after Week 2.
- Do not implement Week 4+ features unless this file explicitly asks for a placeholder.
- Prefer deterministic, file-based output over complex runtime behavior.
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
**Completed at:** 2026-05-09 22:53  
**Completed by:** coding agent  
**Verification command(s):** pip install -e ".[dev,dashboard]"; pytest -q tests/test_dashboard_render.py  
**Notes:** Completed for Week 3 v0.2 dashboard scope.  

<!-- AGENT_STATUS: COMPLETED -->
