---
week: 3
day: 1
slice: "03_single_run_dashboard_skeleton_layout"
title: "single-run dashboard skeleton layout"
priority: "P0"
status: "completed"
target_version: "v0.2-dashboard"
---

# 03_single_run_dashboard_skeleton_layout — single-run dashboard skeleton layout

## Objective

Create a readable single-run dashboard skeleton with core sections.

## Context

Week 3 v0.2 should generate a browser-openable dashboard. The first layout should be simple, static, and deterministic.

## Dependencies

- 02_jinja2_template_loader_and_fallback

## Target Files

- src/skilllogboard/dashboards/templates/run.html.j2
- src/skilllogboard/dashboards/static_builder.py
- tests/test_dashboard_render.py

## Implementation Steps

1. Add sections: Run Summary, Main Metric, Metrics, Config, Artifacts, Files.
2. Include basic inline CSS for readability.
3. Show project, run name, status, created_at, updated_at, and run_id.
4. Show links to manifest, config, metrics, events, summary, and artifact index when present.
5. Ensure the HTML is self-contained and can be opened from the file system.

## Acceptance Criteria

- Generated `dashboard.html` contains a visible Run Summary section.
- Generated `dashboard.html` includes links to core files.
- The dashboard can be opened without a server.
- Tests assert key section labels are present.

## Verification Commands

```bash
pytest -q tests/test_dashboard_render.py
python examples/basic_usage.py
```

## Non-goals

- Do not spend time on final brand polish; keep it functional.

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
**Verification command(s):** pytest -q tests/test_dashboard_render.py; python examples/basic_usage.py  
**Notes:** Completed for Week 3 v0.2 dashboard scope.  

<!-- AGENT_STATUS: COMPLETED -->
