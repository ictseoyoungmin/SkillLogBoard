---
milestone: "v1.0"
phase: "Local-first Live Board"
slice: "03_live_cli_watch_command"
title: "skilllog watch CLI command"
priority: "P0"
status: "completed"
target_version: "v1.0-live-board"
---

# 03_live_cli_watch_command — skilllog watch CLI command

## Objective

Add the user-facing `skilllog watch` command.

## Context

v1.0 adds a local-first live board on top of existing SkillLogBoard file-based evidence packages. It must remain optional, local, and additive.

## Target Files

- src/skilllogboard/cli/main.py
- src/skilllogboard/live/server.py
- tests/test_cli_live.py

## Implementation Steps

1. Add `skilllog watch TARGET_DIR`.
2. Support options: `--host`, `--port`, `--poll-interval`, `--project`, `--latest`, `--monitor-system`, `--monitor-gpu`, `--log-file`, `--no-open`.
3. If live extra is missing, show install guidance.
4. Do not automatically open browser in tests.
5. Add CLI tests for help and missing dependency path.

## Acceptance Criteria

- `skilllog watch --help` is readable.
- Command validates target path.
- Missing live extra message is actionable.
- CLI tests pass.

## Verification Commands

```bash
pytest -q tests/test_cli_live.py
skilllog watch --help || skilllog --help
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

