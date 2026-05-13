---
milestone: "v1.0"
phase: "Local-first Live Board"
slice: "04_active_monitor_loop"
title: "active monitor loop"
priority: "P0"
status: "completed"
target_version: "v1.0-live-board"
---

# 04_active_monitor_loop — active monitor loop

## Objective

Implement optional active monitor loop that appends `monitoring.jsonl` while server runs.

## Context

v1.0 adds a local-first live board on top of existing SkillLogBoard file-based evidence packages. It must remain optional, local, and additive.

## Target Files

- src/skilllogboard/live/monitor_loop.py
- src/skilllogboard/live/server.py
- tests/test_live_monitoring.py

## Implementation Steps

1. Implement a small monitor loop abstraction without starting threads in tests unless controlled.
2. Sample system/GPU/process monitors based on options.
3. Append to `monitoring.jsonl`.
4. Make interval configurable.
5. Provide start/stop hooks for server integration.
6. Add unit tests for one-shot sampling/append.

## Acceptance Criteria

- One-shot active monitor writes monitoring records.
- Loop can be disabled by default.
- Tests do not hang.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_live_monitoring.py tests/test_live_monitors.py
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

