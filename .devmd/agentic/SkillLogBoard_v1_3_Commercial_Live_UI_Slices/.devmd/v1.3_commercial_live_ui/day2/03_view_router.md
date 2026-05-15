---
milestone: "v1.3"
phase: "Commercial Live UI"
day: "day2"
slice: "03_view_router"
title: "frontend view router"
priority: "P0"
status: "pending"
target_version: "v1.3"
---

# 03_view_router — frontend view router

## Objective

Implement view-level routing without introducing a heavy router unless needed.

## Context

v1.3 upgrades the v1.2 app shell into a commercial-quality local Live Board frontend, using compiled static assets served by the Python package while preserving local-first semantics.

## Dependencies

- v1.2 App Shell Refactor completed.
- View-scoped API contracts are stable enough for frontend consumption.
- Static dashboard/report outputs remain separate portable evidence artifacts.

## Target Files

- frontend/live-board/src/App.tsx
- frontend/live-board/src/routes/

## Implementation Steps

1. Represent views: overview, runs, compare, metrics, artifacts, reports, agent, settings.
2. Sync view state to URL hash or query for shareable local state.
3. Set project default to overview.
4. Set run default to metric lab or run view.
5. Add not-found fallback.

## Acceptance Criteria

- All target views route correctly.
- URL state is usable.
- Default view policy matches v1.2.
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

## Agent Completion Block

- [ ] Implementation completed
- [ ] Acceptance criteria verified
- [ ] Tests or smoke checks executed
- [ ] No unrelated files changed
- [ ] Notes added below if anything was skipped or deferred

**Status:** PENDING  
**Completed at:**  
**Completed by:**  
**Verification command(s):**  
**Notes:**  

<!-- AGENT_STATUS: PENDING -->

