---
milestone: "v1.2"
phase: "Live Board App Shell Refactor"
day: "day4"
slice: "02_metric_lab_independent_view"
title: "Metric Lab independent view"
priority: "P0"
status: "completed"
target_version: "v1.2"
---

# 02_metric_lab_independent_view — Metric Lab independent view

## Objective

Move Metric Lab into its own scalar exploration screen.

## Context

v1.2 restructures Live Board into a screen-based local app shell with project overview as the default project-watch landing page and lazy, view-scoped data loading.

## Dependencies

- v1.1.2 Showcase / Visual Parity completed.
- Current Live Board compare/artifact/agent features remain available.
- Static dashboard/report outputs remain portable and separate from Live Board.

## Target Files

- src/skilllogboard/live/templates/live.html
- src/skilllogboard/live/server.py
- tests/test_live_ui_snapshot.py

## Implementation Steps

1. Render expanded chart workspace.
2. Render scalar catalog/search/pin controls.
3. Support smoothing, scale, alignment, marker legend.
4. Avoid claiming automatic insight/diagnosis.
5. Add tests for Metric Lab landmarks.

## Acceptance Criteria

- Metric Lab is independent.
- Scalar catalog exists.
- Controls match actual supported transformations.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_live_ui_snapshot.py
```

## Non-goals

- Do not migrate to React/Vite in v1.2 unless explicitly approved; v1.3 owns the commercial frontend stack.
- Do not implement TensorBoard/W&B import.
- Do not implement Prometheus/Grafana integration.
- Do not implement cloud sync.
- Do not implement multi-user auth.
- Do not add a database backend.
- Do not perform TestPyPI/PyPI publishing in this slice.
- Do not weaken local-first, inspectable-file behavior.

## Handoff Notes

- Keep the slice focused and reviewable.
- Prefer additive state/API fields over breaking existing contracts.
- Keep static dashboard/report portability separate from Live Board app behavior.
- If an item is deferred, document the reason in the Agent Completion Block.
- Update related docs/status/changelog when user-visible behavior changes.

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
**Verification command(s):** .venv/bin/python -m ruff check src/skilllogboard/live src/skilllogboard/cli/main.py tests/test_live_readers.py tests/test_live_project.py tests/test_live_server.py tests/test_cli_live.py tests/test_live_ui_snapshot.py; .venv/bin/python -m pytest -q; .venv/bin/python examples/live_demo.py --multi-run --runs 5 --rich; .venv/bin/python examples/basic_usage.py; .venv/bin/python examples/ir_drop_example.py; .venv/bin/python examples/trajectory_example.py; .venv/bin/python -m build --no-isolation  
**Notes:** Implemented v1.2 app shell scope with view routing, project/run default views, view-scoped state, summary-first project payloads, bounded compare/lab series, docs, tests, and v1.3 handoff. Remote CI was not checked because no push/CI run was requested.  

<!-- AGENT_STATUS: COMPLETED -->
