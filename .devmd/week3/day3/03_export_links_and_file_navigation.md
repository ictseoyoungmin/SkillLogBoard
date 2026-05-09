---
week: 3
day: 3
slice: "03_export_links_and_file_navigation"
title: "export links and file navigation"
priority: "P0"
status: "completed"
target_version: "v0.2-dashboard"
---

# 03_export_links_and_file_navigation — export links and file navigation

## Objective

Add links to core run files and export outputs in the dashboard.

## Context

The dashboard is a viewer over the run folder. Users should be able to open source files such as metrics, config, manifest, summary, and events from the dashboard.

## Dependencies

- 01_config_table_component
- 02_artifact_links_component

## Target Files

- src/skilllogboard/dashboards/templates/run.html.j2
- src/skilllogboard/dashboards/components.py
- tests/test_dashboard_config_artifacts.py

## Implementation Steps

1. Add a Files or Export Links section.
2. Link to manifest.yaml, config.yaml, metrics.csv, events.jsonl, summary.md, artifact_index.json when present.
3. Use only relative links.
4. Do not link to missing files.
5. Add tests that expected file links are present.

## Acceptance Criteria

- Dashboard includes links to core run files.
- Only existing files are linked.
- Links are relative and work when opening dashboard.html from the run folder.

## Verification Commands

```bash
pytest -q tests/test_dashboard_config_artifacts.py
```

## Non-goals

- Do not generate new export formats in Week 3.

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
**Verification command(s):** pytest -q tests/test_dashboard_config_artifacts.py  
**Notes:** Completed for Week 3 v0.2 dashboard scope.  

<!-- AGENT_STATUS: COMPLETED -->
