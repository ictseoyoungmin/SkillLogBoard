---
milestone: "v1.0-cleanup"
phase: "Local-first Live Board Cleanup"
slice: "01_live_poll_interval_and_health_config"
title: "live poll interval and health/config exposure"
priority: "P0"
status: "completed"
target_version: "v1.0-cleanup"
---

# 01_live_poll_interval_and_health_config — live poll interval and health/config exposure

## Objective

Make `--poll-interval` semantics consistent across active monitor sampling, server state/config, and browser UI refresh.

## Context

v1.0 Local-first Live Board is functionally complete and CI is green. This cleanup phase resolves practical usability, server behavior, performance, and test-coverage issues before release-candidate packaging.

## Dependencies

- v1.0 Local-first Live Board implementation completed.
- Latest main CI is green.
- v0.7 Report Artifact Layer, v0.8 Agent Research Layer, and v0.9 Template Forge remain compatible.

## Target Files

- src/skilllogboard/live/server.py
- src/skilllogboard/live/templates/live.html
- tests/test_live_server.py
- tests/test_live_ui_snapshot.py
- docs/live_board.md
- README.md

## Implementation Steps

1. Inspect current `LiveServerOptions.poll_interval` usage.
2. Expose `poll_interval` through `/api/health`, `/api/config`, or the existing `/api/state` response.
3. Update `live.html` JavaScript to use the server-provided poll interval for refresh timing.
4. Ensure minimum refresh interval is bounded to avoid accidental excessive polling.
5. Clarify in docs whether `--poll-interval` controls UI refresh, monitor sampling, or both.
6. Add tests that verify the interval is visible in server output and referenced by the HTML template.

## Acceptance Criteria

- `--poll-interval` has documented behavior.
- Server exposes poll interval to the UI or state/config endpoint.
- Browser refresh interval uses the configured value or a safe bounded fallback.
- Tests cover server/config and UI template behavior.
- Existing `skilllog watch` behavior remains compatible.

## Verification Commands

```bash
pytest -q tests/test_live_server.py tests/test_live_ui_snapshot.py tests/test_cli_live.py
python - <<'PY'
from skilllogboard.live.server import LiveServerOptions
opts = LiveServerOptions(poll_interval=2.5)
assert opts.poll_interval == 2.5
print('poll interval option check passed')
PY
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

- If `/api/config` is added, keep `/api/health` backward-compatible.
- Avoid adding WebSocket/SSE in this cleanup; polling is enough.

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

