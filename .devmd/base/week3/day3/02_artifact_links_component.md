---
week: 3
day: 3
slice: "02_artifact_links_component"
title: "artifact links component"
priority: "P0"
status: "completed"
target_version: "v0.2-dashboard"
---

# 02_artifact_links_component — artifact links component

## Objective

Render artifact, image, and table links from artifact indexes and file records.

## Context

Week 2 implemented artifact/image/table logging. Week 3 should expose those outputs in the dashboard.

## Dependencies

- day1 dashboard data contract
- Week 2 artifact/image/table logging

## Target Files

- src/skilllogboard/dashboards/components.py
- src/skilllogboard/dashboards/templates/run.html.j2
- tests/test_dashboard_config_artifacts.py

## Implementation Steps

1. Load artifact records from `artifact_index.json` or dashboard context.
2. Render artifact name, type, relative path, copy/reference mode, and size if available.
3. Create clickable links for files inside the run directory.
4. For reference-mode artifacts outside the run folder, show source path as text and avoid unsafe file links if needed.
5. Add tests using a run with artifact, image, and table records.

## Acceptance Criteria

- Dashboard contains an Artifacts section.
- Copied artifacts have clickable relative links.
- Image and table records appear in the artifact list.
- Missing artifact index produces a readable empty state.

## Verification Commands

```bash
pytest -q tests/test_dashboard_config_artifacts.py
```

## Non-goals

- Do not implement image thumbnail gallery here.

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
