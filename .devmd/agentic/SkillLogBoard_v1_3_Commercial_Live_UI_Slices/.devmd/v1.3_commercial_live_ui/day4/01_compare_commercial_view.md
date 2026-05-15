---
milestone: "v1.3"
phase: "Commercial Live UI"
day: "day4"
slice: "01_compare_commercial_view"
title: "commercial Compare view"
priority: "P0"
status: "pending"
target_version: "v1.3"
---

# 01_compare_commercial_view — commercial Compare view

## Objective

Implement polished Compare view using local compare API.

## Context

v1.3 upgrades the v1.2 app shell into a commercial-quality local Live Board frontend, using compiled static assets served by the Python package while preserving local-first semantics.

## Dependencies

- v1.2 App Shell Refactor completed.
- View-scoped API contracts are stable enough for frontend consumption.
- Static dashboard/report outputs remain separate portable evidence artifacts.

## Target Files

- frontend/live-board/src/views/CompareView.tsx
- frontend/live-board/src/components/charts/

## Implementation Steps

1. Render run picker, metric selector, x-axis, scale, smoothing, normalize, baseline controls.
2. Render overlay chart.
3. Render legend and compare summary table.
4. Render warnings for missing metrics/downsampling.
5. Do not claim automatic analysis.

## Acceptance Criteria

- Compare view is first-class.
- Overlay chart consumes compare API.
- Legend and delta table exist.
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

