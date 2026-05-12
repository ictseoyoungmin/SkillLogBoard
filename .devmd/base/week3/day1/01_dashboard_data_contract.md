---
week: 3
day: 1
slice: "01_dashboard_data_contract"
title: "dashboard data contract"
priority: "P0"
status: "completed"
target_version: "v0.2-dashboard"
---

# 01_dashboard_data_contract — dashboard data contract

## Objective

Define the data contract consumed by the single-run static dashboard builder.

## Context

The dashboard must be generated from existing run files, not from live training state. This slice defines how manifest, config, metrics, events, and artifact index are loaded into a dashboard context.

## Dependencies

- week2 cleanup complete
- Week 2 v0.1 integration test passing

## Target Files

- src/skilllogboard/dashboards/static_builder.py
- src/skilllogboard/dashboards/components.py
- tests/test_dashboard_data.py

## Implementation Steps

1. Create a function such as `load_run_context(run_dir)`.
2. Load `manifest.yaml`, `config.yaml`, `metrics.csv`, `events.jsonl`, and `artifact_index.json` if present.
3. Gracefully handle missing optional files with empty defaults and warning messages.
4. Keep the context JSON-serializable or template-friendly.
5. Add tests using a temporary v0.1 run.

## Acceptance Criteria

- Dashboard context includes manifest, config, metrics, events summary, artifact records, and file links.
- Missing optional files do not crash context loading.
- The loader does not require pandas.
- Tests cover complete and partial run directories.

## Verification Commands

```bash
pytest -q tests/test_dashboard_data.py
```

## Non-goals

- Do not render the final HTML layout in this slice.

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
**Verification command(s):** pytest -q tests/test_dashboard_data.py  
**Notes:** Completed for Week 3 v0.2 dashboard scope.  

<!-- AGENT_STATUS: COMPLETED -->
