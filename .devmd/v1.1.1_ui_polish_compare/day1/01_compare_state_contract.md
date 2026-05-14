---
milestone: "v1.1.1"
phase: "UI Polish, True Compare, and Interaction Hardening"
day: "day1"
slice: "01_compare_state_contract"
title: "compare state contract"
priority: "P0"
status: "completed"
target_version: "v1.1.1-ui-polish-compare"
---

# 01_compare_state_contract — compare state contract

## Objective

Define a stable local API contract for true cross-run compare/overlay mode.

## Context

v1.1 changed the Live Board into a chart-first local research workspace. v1.1.1 turns that redesign into release-candidate quality by making compare/overlay real, refining visual layout and interactions, fixing artifact discovery, and hardening tests.

## Dependencies

- v1.1 UI/UX Redesign completed.
- v1.0 Live Board behavior remains compatible.
- Existing static dashboard/report/compare/agent/template-forge behavior remains green.

## Target Files

- src/skilllogboard/live/project.py
- src/skilllogboard/live/state.py
- src/skilllogboard/live/server.py
- tests/test_live_project.py
- tests/test_live_server.py
- docs/live_board.md

## Implementation Steps

1. Define a `compare` section in project state or `/api/state` response.
2. Include compare candidates with run_id, run_name, status, and role labels such as latest, best, completed, failed, current if available.
3. Include supported shared metric names across candidate runs.
4. Add bounded parameters for max compare runs and max points per series.
5. Keep existing `runs`, `leaderboard`, and status fields backward-compatible.
6. Document the compare state shape.

## Acceptance Criteria

- Project state exposes compare candidates.
- Shared metric names are available for compare UI.
- Runs missing the selected metric are represented clearly or omitted with warning metadata.
- Payload bounds are explicit.
- Existing project mode tests still pass.

## Verification Commands

```bash
pytest -q tests/test_live_project.py tests/test_live_server.py
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

