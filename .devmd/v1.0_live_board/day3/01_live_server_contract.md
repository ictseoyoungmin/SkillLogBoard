---
milestone: "v1.0"
phase: "Local-first Live Board"
slice: "01_live_server_contract"
title: "live server contract"
priority: "P0"
status: "completed"
target_version: "v1.0-live-board"
---

# 01_live_server_contract — live server contract

## Objective

Define local server app factory and API contract.

## Context

v1.0 adds a local-first live board on top of existing SkillLogBoard file-based evidence packages. It must remain optional, local, and additive.

## Target Files

- src/skilllogboard/live/server.py
- tests/test_live_server.py

## Implementation Steps

1. Create app factory `create_live_app(target_dir, options)` or equivalent.
2. Define endpoints: `/`, `/api/state`, `/api/health`.
3. Keep server import guarded by live extra dependencies.
4. Return readable optional dependency error when FastAPI/uvicorn is missing.
5. Add tests if FastAPI test client is available under live extra.

## Acceptance Criteria

- Server module imports in minimal environment.
- App factory works when live extra is installed.
- API contract is documented in tests.
- Tests pass or skip gracefully without live extra.

## Verification Commands

```bash
pytest -q tests/test_live_server.py
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

