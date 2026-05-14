---
milestone: "v1.1.2"
phase: "Showcase, Visual Parity, and Demo Depth"
day: "day1"
slice: "01_rich_demo_mode"
title: "rich demo mode"
priority: "P0"
status: "completed"
target_version: "v1.1.2-showcase-visual-parity"
---

# 01_rich_demo_mode — rich demo mode

## Objective

Add a rich demo mode that produces visually useful local run evidence for manual UI review and screenshots.

## Context

v1.1.1 implemented true compare/overlay and core UI interaction hardening. However, the actual UI can still look less capable than the design mockups because many advanced features are hidden behind drawers, sparse demo data, and minimal affordances. v1.1.2 should improve perceived product completeness without violating local-first or lightweight-package principles.

## Dependencies

- v1.1.1 UI Polish / True Compare completed.
- Live Board core APIs remain compatible.
- Existing static dashboard/report/compare/agent/template-forge behavior remains green.

## Target Files

- examples/live_demo.py
- tests/test_live_project.py
- docs/live_board.md

## Implementation Steps

1. Add `--rich` option to `examples/live_demo.py`.
2. When `--rich` is combined with `--multi-run`, generate at least five runs: baseline, best, overfit, failed, current.
3. Use deterministic synthetic curves with visible differences between runs.
4. Keep runtime short and deterministic; avoid long sleeps.
5. Print exact single-run and project-watch commands after generation.
6. Document the rich demo command.

## Acceptance Criteria

- `python examples/live_demo.py --multi-run --runs 5 --rich` creates a project folder with multiple runs.
- Runs have distinct names and statuses.
- Runtime remains short.
- Docs include the rich demo command.

## Verification Commands

```bash
python examples/live_demo.py --multi-run --runs 5 --rich
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

