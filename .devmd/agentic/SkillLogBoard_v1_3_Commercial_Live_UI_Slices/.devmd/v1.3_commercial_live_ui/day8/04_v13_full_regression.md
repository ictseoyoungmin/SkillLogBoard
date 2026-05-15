---
milestone: "v1.3"
phase: "Commercial Live UI"
day: "day8"
slice: "04_v13_full_regression"
title: "v1.3 full regression"
priority: "P1"
status: "completed"
target_version: "v1.3"
---

# 04_v13_full_regression — v1.3 full regression

## Objective

Run full regression and frontend build verification.

## Context

v1.3 upgrades the v1.2 app shell into a commercial-quality local Live Board frontend, using compiled static assets served by the Python package while preserving local-first semantics.

## Dependencies

- v1.2 App Shell Refactor completed.
- View-scoped API contracts are stable enough for frontend consumption.
- Static dashboard/report outputs remain separate portable evidence artifacts.

## Target Files

- .github/workflows/ci.yml
- tests/
- frontend/live-board/
- .devmd/v1.3_commercial_live_ui/**/*.md

## Implementation Steps

1. Run frontend install/build/lint/test if Node environment exists.
2. Run ruff.
3. Run full pytest.
4. Run live-specific tests.
5. Run rich demo.
6. Run build no-isolation.
7. Confirm GitHub Actions green after push.

## Acceptance Criteria

- Frontend build passes or environment limitation is recorded.
- Ruff passes.
- Full pytest passes.
- Live tests pass.
- Wheel build passes.
- Latest CI is green or noted.

## Verification Commands

```bash
cd frontend/live-board && npm ci
cd frontend/live-board && npm run lint
cd frontend/live-board && npm run test -- --run
cd frontend/live-board && npm run build
pip install -e ".[dev,dashboard,live]"
ruff check .
pytest -q
python examples/live_demo.py --multi-run --runs 5 --rich
python -m build --no-isolation
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

## Agent Completion Block## Agent Completion Block

- [x] Implementation completed
- [x] Acceptance criteria verified
- [x] Tests or smoke checks executed
- [x] No unrelated files changed
- [x] Notes added below if anything was skipped or deferred

**Status:** COMPLETED  
**Completed at:** 2026-05-15  
**Completed by:** Codex  
**Verification command(s):** `npm run lint`; `npm run test`; `npm run build`; `.venv/bin/python -m ruff check .`; `.venv/bin/python -m pytest -q`; `.venv/bin/python -m build --no-isolation`  
**Notes:** Implemented and verified in the v1.3 commercial Live UI completion pass. The packaged React Live Board now includes the commercial app shell, routed views, command palette, inspector, responsive layouts, fallback states, and wheel-packaged static assets. CI now runs frontend lint/test/build and Python no-isolation package build.

<!-- AGENT_STATUS: COMPLETED -->
