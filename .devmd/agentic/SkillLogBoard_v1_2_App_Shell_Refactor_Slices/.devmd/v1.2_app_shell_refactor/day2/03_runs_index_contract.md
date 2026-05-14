---
milestone: "v1.2"
phase: "Live Board App Shell Refactor"
day: "day2"
slice: "03_runs_index_contract"
title: "runs index contract"
priority: "P0"
status: "completed"
target_version: "v1.2"
---

# 03_runs_index_contract — runs index contract

## Objective

Create a lightweight runs index for the Runs view.

## Context

v1.2 restructures Live Board into a screen-based local app shell with project overview as the default project-watch landing page and lazy, view-scoped data loading.

## Dependencies

- v1.1.2 Showcase / Visual Parity completed.
- Current Live Board compare/artifact/agent features remain available.
- Static dashboard/report outputs remain portable and separate from Live Board.

## Target Files

- src/skilllogboard/live/project.py
- tests/test_live_project.py
- src/skilllogboard/live/templates/live.html

## Implementation Steps

1. Define run index fields: run_id, name, status, branch/tag, key metric, duration, updated time, artifact count, warning count.
2. Support pagination or bounded result size if needed.
3. Do not read full series for run table.
4. Add tests for sorting/filtering-friendly metadata.

## Acceptance Criteria

- Runs index is lightweight.
- Runs view has enough fields for table rendering.
- Full series is not loaded for table metadata.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_live_project.py
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
