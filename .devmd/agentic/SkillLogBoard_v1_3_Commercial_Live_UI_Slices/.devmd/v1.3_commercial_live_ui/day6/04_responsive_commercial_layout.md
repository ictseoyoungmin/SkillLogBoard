---
milestone: "v1.3"
phase: "Commercial Live UI"
day: "day6"
slice: "04_responsive_commercial_layout"
title: "responsive commercial layout"
priority: "P0"
status: "pending"
target_version: "v1.3"
---

# 04_responsive_commercial_layout — responsive commercial layout

## Objective

Make commercial UI responsive on laptop and narrower screens.

## Context

v1.3 upgrades the v1.2 app shell into a commercial-quality local Live Board frontend, using compiled static assets served by the Python package while preserving local-first semantics.

## Dependencies

- v1.2 App Shell Refactor completed.
- View-scoped API contracts are stable enough for frontend consumption.
- Static dashboard/report outputs remain separate portable evidence artifacts.

## Target Files

- frontend/live-board/src/styles/
- frontend/live-board/src/components/shell/

## Implementation Steps

1. Define layout breakpoints.
2. Collapse sidebar labels on narrow screens.
3. Stack compare/runs/artifacts views cleanly.
4. Ensure charts remain usable.
5. Update visual QA docs.

## Acceptance Criteria

- Responsive behavior exists.
- No major view overflows on laptop/narrow widths.
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

