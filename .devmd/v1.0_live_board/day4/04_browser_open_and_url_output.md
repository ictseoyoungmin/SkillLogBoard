---
milestone: "v1.0"
phase: "Local-first Live Board"
slice: "04_browser_open_and_url_output"
title: "browser open and URL output"
priority: "P0"
status: "completed"
target_version: "v1.0-live-board"
---

# 04_browser_open_and_url_output — browser open and URL output

## Objective

Implement safe URL printing and optional browser open behavior.

## Context

v1.0 adds a local-first live board on top of existing SkillLogBoard file-based evidence packages. It must remain optional, local, and additive.

## Target Files

- src/skilllogboard/cli/main.py
- tests/test_cli_live.py

## Implementation Steps

1. Print local URL on watch start.
2. Support `--no-open` to disable browser opening.
3. Only call webbrowser.open when not disabled and server startup is successful.
4. Add tests using monkeypatch/mocking.
5. Avoid blocking tests on actual uvicorn server.

## Acceptance Criteria

- CLI prints URL.
- `--no-open` prevents browser open.
- Tests do not start a long-running server.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_cli_live.py
```

## Non-goals

- Do not implement TensorBoard/W&B import.
- Do not implement Prometheus/Grafana integration.
- Do not implement cloud sync.
- Do not implement multi-user auth.
- Do not add database backend.
- Do not replace static dashboard/report/compare.
- Do not add heavy dependencies to core.

## Handoff Notes

- Keep this slice focused and small.
- Preserve all existing v0.6-v0.9 behavior.
- Missing optional live dependencies must produce readable messages or skipped tests.
- The Live Board should watch local files; it should not become a SaaS/observability platform.

---

## Agent Completion Block

- [x] Implementation completed
- [x] Acceptance criteria verified
- [x] Tests or smoke checks executed
- [x] No unrelated files changed
- [x] Notes added below if anything was skipped or deferred

**Status:** COMPLETED  
**Completed at:** 2026-05-13
**Completed by:** Codex
**Verification command(s):** .venv/bin/python -m ruff check .; .venv/bin/python -m pytest -q; .venv/bin/python -m build --no-isolation; .venv/bin/python examples/live_demo.py
**Notes:** Isolated python -m build could not create an ensurepip venv in this environment, so package verification was rerun successfully with --no-isolation.

<!-- AGENT_STATUS: COMPLETED -->

