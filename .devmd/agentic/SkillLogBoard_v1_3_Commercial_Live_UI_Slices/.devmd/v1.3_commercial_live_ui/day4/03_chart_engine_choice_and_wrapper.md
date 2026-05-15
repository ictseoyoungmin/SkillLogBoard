---
milestone: "v1.3"
phase: "Commercial Live UI"
day: "day4"
slice: "03_chart_engine_choice_and_wrapper"
title: "chart engine wrapper"
priority: "P0"
status: "completed"
target_version: "v1.3"
---

# 03_chart_engine_choice_and_wrapper — chart engine wrapper

## Objective

Create a chart wrapper that can later swap chart engine without rewriting views.

## Context

v1.3 upgrades the v1.2 app shell into a commercial-quality local Live Board frontend, using compiled static assets served by the Python package while preserving local-first semantics.

## Dependencies

- v1.2 App Shell Refactor completed.
- View-scoped API contracts are stable enough for frontend consumption.
- Static dashboard/report outputs remain separate portable evidence artifacts.

## Target Files

- frontend/live-board/src/components/charts/
- docs/adr/live_board_chart_engine.md

## Implementation Steps

1. Choose current implementation: custom SVG/canvas/uPlot if dependency approved.
2. Document decision and tradeoffs.
3. Create LineChart/OverlayChart component interface.
4. Support markers, legend data, smoothing-ready input.
5. Keep bundle size reasonable.

## Acceptance Criteria

- Chart wrapper exists.
- Decision doc exists.
- Compare and Lab use wrapper.
- Build passes.

## Verification Commands

```bash
cd frontend/live-board && npm run build
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
