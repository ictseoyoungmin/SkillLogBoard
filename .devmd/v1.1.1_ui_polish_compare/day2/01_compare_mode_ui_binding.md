---
milestone: "v1.1.1"
phase: "UI Polish, True Compare, and Interaction Hardening"
day: "day2"
slice: "01_compare_mode_ui_binding"
title: "compare mode UI binding"
priority: "P0"
status: "completed"
target_version: "v1.1.1-ui-polish-compare"
---

# 01_compare_mode_ui_binding — compare mode UI binding

## Objective

Make the Compare button trigger actual project compare behavior and overlay rendering.

## Context

v1.1 changed the Live Board into a chart-first local research workspace. v1.1.1 turns that redesign into release-candidate quality by making compare/overlay real, refining visual layout and interactions, fixing artifact discovery, and hardening tests.

## Dependencies

- v1.1 UI/UX Redesign completed.
- v1.0 Live Board behavior remains compatible.
- Existing static dashboard/report/compare/agent/template-forge behavior remains green.

## Target Files

- src/skilllogboard/live/templates/live.html
- tests/test_live_ui_snapshot.py
- tests/test_live_server.py

## Implementation Steps

1. When Compare is enabled in project mode, request `/api/state` with selected compare metric and selected run IDs.
2. Render compare data rather than single project leaderboard bars.
3. If not in project mode, show a helpful message that cross-run compare requires project watch mode.
4. Keep single-run multi-metric overlay working separately.
5. Add stable data attributes for compare-mode elements.

## Acceptance Criteria

- Compare toggle has real behavior in project mode.
- Single-run mode does not pretend to support cross-run compare unless project data exists.
- Compare state is visible to users.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_live_ui_snapshot.py tests/test_live_server.py
```

## Non-goals

- Do not implement TensorBoard/W&B import.
- Do not implement Prometheus/Grafana integration.
- Do not implement cloud sync.
- Do not implement multi-user auth.
- Do not add a database backend.
- Do not add React/Vue/Svelte build tooling unless separately approved.
- Do not add heavy dependencies to core.
- Do not perform TestPyPI/PyPI release work in this slice.

## Handoff Notes

- Keep this slice focused, but do not under-implement interaction details.
- Preserve local-first, file-based, inspectable behavior.
- Prefer additive API fields over breaking existing fields.
- Default UI should remain minimal; advanced detail belongs in drawer, tray, modal, or compare mode.
- If an item is deferred, update docs/status and record the reason in the Agent Completion Block.

---

## Agent Completion Block

- [x] Implementation completed
- [x] Acceptance criteria verified
- [x] Tests or smoke checks executed
- [x] No unrelated files changed
- [x] Notes added below if anything was skipped or deferred

**Status:** COMPLETED  
**Completed at:** 2026-05-14  
**Completed by:** Codex  
**Verification command(s):** `.venv/bin/python -m ruff check .`; `.venv/bin/python -m pytest`; `.venv/bin/python -m build --no-isolation`; `.venv/bin/python examples/live_demo.py --multi-run --runs 2`; `.venv/bin/python -c "import skilllogboard; print(skilllogboard.__version__)"`; `.venv/bin/skilllog --version`  
**Notes:** Completed locally. No deferred implementation items. Publishing and external CI execution were not performed.  

<!-- AGENT_STATUS: COMPLETED -->

