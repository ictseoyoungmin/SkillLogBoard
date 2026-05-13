---
milestone: "v1.0"
phase: "Local-first Live Board"
slice: "02_system_process_monitor"
title: "system and process monitor"
priority: "P0"
status: "completed"
target_version: "v1.0-live-board"
---

# 02_system_process_monitor — system and process monitor

## Objective

Implement optional psutil-based system/process monitor.

## Context

v1.0 adds a local-first live board on top of existing SkillLogBoard file-based evidence packages. It must remain optional, local, and additive.

## Target Files

- src/skilllogboard/live/monitors.py
- tests/test_live_monitors.py

## Implementation Steps

1. Guard psutil import.
2. Implement system metrics: cpu_percent, ram_percent, disk_percent if available.
3. Implement process metrics: rss_mb and cpu_percent if available.
4. Return skipped warning if psutil is unavailable.
5. Add tests with monkeypatch or graceful skip.

## Acceptance Criteria

- Monitor imports without psutil installed.
- System/process metrics work when psutil is available.
- Missing psutil is a readable skip, not crash.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_live_monitors.py
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

