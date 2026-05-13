---
milestone: "v1.0-cleanup"
phase: "Local-first Live Board Cleanup"
slice: "02_project_watch_discovery_performance"
title: "project watch discovery performance"
priority: "P0"
status: "completed"
target_version: "v1.0-cleanup"
---

# 02_project_watch_discovery_performance — project watch discovery performance

## Objective

Reduce project watch overhead caused by unrestricted recursive `manifest.yaml` discovery in large run directories.

## Context

v1.0 Local-first Live Board is functionally complete and CI is green. This cleanup phase resolves practical usability, server behavior, performance, and test-coverage issues before release-candidate packaging.

## Dependencies

- v1.0 Local-first Live Board implementation completed.
- Latest main CI is green.
- v0.7 Report Artifact Layer, v0.8 Agent Research Layer, and v0.9 Template Forge remain compatible.

## Target Files

- src/skilllogboard/live/project.py
- src/skilllogboard/live/server.py
- src/skilllogboard/cli/main.py
- tests/test_live_project.py
- tests/test_live_server.py
- docs/live_board.md

## Implementation Steps

1. Inspect current project discovery logic and identify where `root.rglob('manifest.yaml')` is used.
2. Add bounded discovery options such as `max_depth`, `exclude_dirs`, or layout-aware discovery under `runs/{project}/{run_id}`.
3. Skip obvious non-run folders such as `.git`, `.venv`, `__pycache__`, `report`, `_reports`, `artifacts`, and hidden/cache folders where appropriate.
4. Consider a simple mtime-throttled cache if it can be implemented safely without a database.
5. Expose CLI option only if needed; otherwise keep the optimization internal.
6. Add tests with nested non-run folders to ensure discovery remains correct and avoids irrelevant folders.

## Acceptance Criteria

- Project mode still finds valid run directories.
- Discovery ignores irrelevant/deep cache folders where configured.
- `--latest` still works.
- Tests cover nested directories and multiple runs.
- No database or persistent index is introduced.

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
- Do not replace static dashboard/report/compare artifacts.
- Do not add heavy dependencies to core.
- Do not perform PyPI/TestPyPI release work in this cleanup slice.

## Required Notes

- This is a performance cleanup, not a full project index database.
- Keep API response schema stable unless a change is clearly necessary.

## Handoff Notes

- Keep this cleanup focused and small.
- Preserve local-first, file-based, inspectable behavior.
- Missing optional live dependencies must produce readable messages or skipped tests.
- If an item is deferred, update docs/status and record the reason in the Agent Completion Block.
- Do not expand this cleanup into a v1.1 UI redesign.

---

## Agent Completion Block

> The agent must update this block after finishing the slice.

- [x] Implementation completed
- [x] Acceptance criteria verified
- [x] Tests or smoke checks executed
- [x] No unrelated files changed
- [x] Notes added below if anything was skipped or deferred

**Status:** COMPLETED  
**Completed at:** 2026-05-13
**Completed by:** Codex
**Verification command(s):** .venv/bin/python -m ruff check .; .venv/bin/python -m pytest -q; .venv/bin/python -m build --no-isolation; .venv/bin/skilllog --help; .venv/bin/skilllog watch --help; .venv/bin/python examples/basic_usage.py; .venv/bin/python examples/ir_drop_example.py; .venv/bin/python examples/trajectory_example.py; .venv/bin/python examples/live_demo.py; .venv/bin/pip install -e .[dev,dashboard,live]; .venv/bin/python -m pytest -q tests/test_live_state.py tests/test_live_readers.py tests/test_live_project.py tests/test_live_server.py tests/test_live_monitoring.py tests/test_live_monitors.py tests/test_cli_live.py tests/test_live_packaging.py tests/test_live_ui_snapshot.py; .venv/bin/pip install -e .[dev,dashboard,report]; .venv/bin/python -m pytest -q tests/test_report_figures.py tests/test_cli_report_artifacts.py
**Notes:** Local verification completed. GitHub Actions was not checked after push because no push was performed in this session.

<!-- AGENT_STATUS: COMPLETED -->

