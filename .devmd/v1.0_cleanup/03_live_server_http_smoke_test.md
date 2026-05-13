---
milestone: "v1.0-cleanup"
phase: "Local-first Live Board Cleanup"
slice: "03_live_server_http_smoke_test"
title: "live server HTTP smoke test"
priority: "P0"
status: "completed"
target_version: "v1.0-cleanup"
---

# 03_live_server_http_smoke_test — live server HTTP smoke test

## Objective

Restore at least one actual HTTP-level test for `/api/health` and `/api/state` while preserving compatibility with optional live dependencies.

## Context

v1.0 Local-first Live Board is functionally complete and CI is green. This cleanup phase resolves practical usability, server behavior, performance, and test-coverage issues before release-candidate packaging.

## Dependencies

- v1.0 Local-first Live Board implementation completed.
- Latest main CI is green.
- v0.7 Report Artifact Layer, v0.8 Agent Research Layer, and v0.9 Template Forge remain compatible.

## Target Files

- tests/test_live_server.py
- tests/test_cli_live.py
- src/skilllogboard/live/server.py
- .github/workflows/ci.yml

## Implementation Steps

1. Keep existing direct route tests if they are useful for dependency compatibility.
2. Add a live-extra-only HTTP smoke test using FastAPI TestClient or a safe compatible alternative.
3. Test `/api/health` status code and JSON body.
4. Test `/api/state` status code and JSON body for a small temp run folder.
5. Skip gracefully if FastAPI/TestClient dependencies are unavailable in minimal environments.
6. Confirm the `live-extra` CI job executes this HTTP smoke test.

## Acceptance Criteria

- At least one test exercises actual HTTP response behavior.
- Minimal install tests still do not require live extra.
- Live-extra CI validates `/api/health` and `/api/state`.
- Tests do not start a long-running uvicorn server.

## Verification Commands

```bash
pytest -q tests/test_live_server.py tests/test_cli_live.py
pip install -e ".[dev,dashboard,live]"
pytest -q tests/test_live_server.py
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

- If FastAPI/TestClient has version incompatibility, use a small compatibility wrapper but keep one HTTP-level assertion if possible.

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

