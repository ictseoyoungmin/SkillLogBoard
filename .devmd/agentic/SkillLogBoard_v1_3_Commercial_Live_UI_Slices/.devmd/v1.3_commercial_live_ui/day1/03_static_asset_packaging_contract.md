---
milestone: "v1.3"
phase: "Commercial Live UI"
day: "day1"
slice: "03_static_asset_packaging_contract"
title: "static asset packaging contract"
priority: "P0"
status: "completed"
target_version: "v1.3"
---

# 03_static_asset_packaging_contract — static asset packaging contract

## Objective

Define where compiled frontend assets live in the Python package.

## Context

v1.3 upgrades the v1.2 app shell into a commercial-quality local Live Board frontend, using compiled static assets served by the Python package while preserving local-first semantics.

## Dependencies

- v1.2 App Shell Refactor completed.
- View-scoped API contracts are stable enough for frontend consumption.
- Static dashboard/report outputs remain separate portable evidence artifacts.

## Target Files

- pyproject.toml
- src/skilllogboard/live/static/
- src/skilllogboard/live/server.py
- tests/test_live_packaging.py

## Implementation Steps

1. Choose build output path under `src/skilllogboard/live/static/`.
2. Ensure package data includes compiled JS/CSS/assets.
3. Update server to serve compiled app assets if present.
4. Keep old template fallback if needed during transition.
5. Add packaging tests.

## Acceptance Criteria

- Compiled assets can be included in wheel.
- Server can serve frontend app entry.
- Fallback path is clear.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_live_packaging.py tests/test_live_server.py
```

## Non-goals

- Do not require Node.js at runtime for end users.
- Do not add GraphQL/Apollo/Redux unless separately approved.
- Do not include node_modules in the Python package.
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
**Completed at:** 2026-05-15  
**Completed by:** Codex  
**Verification command(s):** `.venv/bin/python -m pytest -q tests/test_live_packaging.py tests/test_live_server.py`; `cd frontend/live-board && npm run build`  
**Notes:** Build output path is `src/skilllogboard/live/static/app/`. FastAPI serves the compiled app at `/` when present and mounts assets under `/live-static`; otherwise it falls back to the bundled v1.2 template. Package data and MANIFEST include the static output.  

<!-- AGENT_STATUS: COMPLETED -->
