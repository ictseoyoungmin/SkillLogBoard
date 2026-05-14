---
milestone: "v1.1.1"
phase: "UI Polish, True Compare, and Interaction Hardening"
day: "day6"
slice: "02_multi_run_live_demo"
title: "multi-run live demo"
priority: "P0"
status: "completed"
target_version: "v1.1.1-ui-polish-compare"
---

# 02_multi_run_live_demo — multi-run live demo

## Objective

Ensure `examples/live_demo.py` can demonstrate v1.1.1 compare/overlay and UI states.

## Context

v1.1 changed the Live Board into a chart-first local research workspace. v1.1.1 turns that redesign into release-candidate quality by making compare/overlay real, refining visual layout and interactions, fixing artifact discovery, and hardening tests.

## Dependencies

- v1.1 UI/UX Redesign completed.
- v1.0 Live Board behavior remains compatible.
- Existing static dashboard/report/compare/agent/template-forge behavior remains green.

## Target Files

- examples/live_demo.py
- tests/test_live_project.py
- docs/live_board.md

## Implementation Steps

1. Add a command-line option or default behavior to generate multiple runs for project mode.
2. Generate metrics with realistic curve shapes, not identical straight lines.
3. Generate at least one warning/event/artifact per run.
4. Print clear next commands for single-run watch and project watch.
5. Keep runtime short and deterministic.
6. Add/update tests for generated project structure if feasible.

## Acceptance Criteria

- Demo produces visually useful data.
- Demo supports compare/overlay manual testing.
- Runtime remains short.
- Docs include demo commands.

## Verification Commands

```bash
python examples/live_demo.py
pytest -q tests/test_live_project.py
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

