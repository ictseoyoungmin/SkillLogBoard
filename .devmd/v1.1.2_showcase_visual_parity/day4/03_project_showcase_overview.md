---
milestone: "v1.1.2"
phase: "Showcase, Visual Parity, and Demo Depth"
day: "day4"
slice: "03_project_showcase_overview"
title: "project showcase overview"
priority: "P0"
status: "completed"
target_version: "v1.1.2-showcase-visual-parity"
---

# 03_project_showcase_overview — project showcase overview

## Objective

Make project mode immediately communicate that multiple runs and compare are available.

## Context

v1.1.1 implemented true compare/overlay and core UI interaction hardening. However, the actual UI can still look less capable than the design mockups because many advanced features are hidden behind drawers, sparse demo data, and minimal affordances. v1.1.2 should improve perceived product completeness without violating local-first or lightweight-package principles.

## Dependencies

- v1.1.1 UI Polish / True Compare completed.
- Live Board core APIs remain compatible.
- Existing static dashboard/report/compare/agent/template-forge behavior remains green.

## Target Files

- src/skilllogboard/live/templates/live.html
- src/skilllogboard/live/templates/ui_tokens.css
- tests/test_live_ui_snapshot.py

## Implementation Steps

1. Show compact project summary: run count, active/completed/failed count, shared metrics, compare ready.
2. Make run picker and compare actions visually discoverable.
3. Keep detailed run table collapsed or secondary.
4. Add tests for project summary elements.

## Acceptance Criteria

- Project mode does not look empty when rich demo data exists.
- Compare affordance is obvious.
- Detailed run list is accessible but not dominant.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_live_ui_snapshot.py tests/test_live_project.py
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

- This milestone is about visible product completeness, not broad backend expansion.
- Prefer better demo data, empty states, affordances, and layout polish over complex systems.
- Keep the default UI minimal, but make hidden capabilities discoverable.
- Avoid fake functionality. Showcase hints must reflect actual local state or clearly available actions.

---

## Agent Completion Block

> The agent must update this block after finishing the slice.

- [x] Implementation completed
- [x] Acceptance criteria verified
- [x] Tests or smoke checks executed
- [x] No unrelated files changed
- [x] Notes added below if anything was skipped or deferred

**Status:** COMPLETED  
**Completed at:** 2026-05-14  
**Completed by:** Codex  
**Verification command(s):** .venv/bin/python -m ruff check .; .venv/bin/python -m pytest -q; .venv/bin/python examples/live_demo.py --multi-run --runs 5 --rich; .venv/bin/python examples/basic_usage.py; .venv/bin/python examples/ir_drop_example.py; .venv/bin/python examples/trajectory_example.py; .venv/bin/python -m build --no-isolation  
**Notes:** Local implementation and verification completed. Remote GitHub Actions status was not checked from this session.  

<!-- AGENT_STATUS: COMPLETED -->

