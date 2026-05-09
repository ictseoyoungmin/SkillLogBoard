---
week: 3
day: 1
slice: "04_dashboard_builder_api_and_manifest_hook"
title: "dashboard builder API and manifest hook"
priority: "P0"
status: "completed"
target_version: "v0.2-dashboard"
---

# 04_dashboard_builder_api_and_manifest_hook — dashboard builder API and manifest hook

## Objective

Ensure Python API and CLI can call dashboard generation consistently and update manifest file mapping.

## Context

Users call `logger.finish(build_dashboard=True)` and `skilllog dashboard RUN_DIR`. Both should use the same builder and produce the same file path.

## Dependencies

- 03_single_run_dashboard_skeleton_layout

## Target Files

- src/skilllogboard/core/logger.py
- src/skilllogboard/dashboards/static_builder.py
- src/skilllogboard/cli/main.py
- tests/test_dashboard_render.py
- tests/test_cli.py

## Implementation Steps

1. Expose `build_dashboard(run_dir, output_path=None)` or equivalent.
2. Ensure `RunLogger.build_dashboard()` calls the builder.
3. Ensure `finish(build_dashboard=True)` updates `manifest.files['dashboard']`.
4. Ensure CLI `dashboard RUN_DIR` calls the same builder.
5. Add tests for API and CLI paths.

## Acceptance Criteria

- `logger.finish(build_dashboard=True)` creates dashboard and updates manifest.
- `skilllog dashboard <run_dir>` creates or rewrites dashboard.
- Both paths produce non-empty HTML.
- Tests cover API and CLI dashboard generation.

## Verification Commands

```bash
pytest -q tests/test_dashboard_render.py tests/test_cli.py
```

## Non-goals

- Do not implement multi-run dashboard.

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
**Verification command(s):** pytest -q tests/test_dashboard_render.py tests/test_cli.py  
**Notes:** Completed for Week 3 v0.2 dashboard scope.  

<!-- AGENT_STATUS: COMPLETED -->
