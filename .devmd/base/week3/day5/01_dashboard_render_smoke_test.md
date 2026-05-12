---
week: 3
day: 5
slice: "01_dashboard_render_smoke_test"
title: "dashboard render smoke test"
priority: "P0"
status: "completed"
target_version: "v0.2-dashboard"
---

# 01_dashboard_render_smoke_test — dashboard render smoke test

## Objective

Add a Week 3 smoke test that validates dashboard generation from `examples/basic_usage.py`-style output.

## Context

The v0.2 candidate must produce a dashboard.html that can be opened in a browser and contains core sections.

## Dependencies

- week3/day1-day4 slices

## Target Files

- tests/test_dashboard_smoke.py
- examples/basic_usage.py

## Implementation Steps

1. Create a run using RunLogger in a temporary directory.
2. Log metrics, config, artifact, image path if practical, and table if supported.
3. Finish with dashboard and report enabled.
4. Assert dashboard.html exists and is non-empty.
5. Assert rendered HTML contains Run Summary, Metrics, Config, Artifacts, and Files sections.

## Acceptance Criteria

- Dashboard smoke test passes.
- Generated dashboard contains all core sections.
- The test does not require a browser, server, torch, or pandas.

## Verification Commands

```bash
pytest -q tests/test_dashboard_smoke.py
```

## Non-goals

- Do not add screenshot testing.

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
**Verification command(s):** pytest -q tests/test_dashboard_smoke.py  
**Notes:** Completed for Week 3 v0.2 dashboard scope.  

<!-- AGENT_STATUS: COMPLETED -->
