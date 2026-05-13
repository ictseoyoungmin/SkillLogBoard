---
milestone: "v1.0"
phase: "Local-first Live Board"
slice: "03_state_api_project_mode"
title: "state API project mode"
priority: "P0"
status: "completed"
target_version: "v1.0-live-board"
---

# 03_state_api_project_mode — state API project mode

## Objective

Implement `/api/state` for project watch mode.

## Context

v1.0 adds a local-first live board on top of existing SkillLogBoard file-based evidence packages. It must remain optional, local, and additive.

## Target Files

- src/skilllogboard/live/server.py
- src/skilllogboard/live/project.py
- tests/test_live_server.py
- tests/test_live_project.py

## Implementation Steps

1. Add project mode option to app factory.
2. Return project-level run list, status counts, active alerts, and leaderboard-lite data.
3. Add tests with multiple temporary runs.
4. Keep response schema stable.

## Acceptance Criteria

- /api/state returns project state in project mode.
- Status counts and run summaries are included.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_live_server.py tests/test_live_project.py
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

