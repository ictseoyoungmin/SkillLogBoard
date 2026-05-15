---
milestone: "v1.3"
phase: "Commercial Live UI"
day: "day3"
slice: "01_overview_commercial_view"
title: "commercial Overview view"
priority: "P0"
status: "pending"
target_version: "v1.3"
---

# 01_overview_commercial_view — commercial Overview view

## Objective

Implement polished project Overview view.

## Context

v1.3 upgrades the v1.2 app shell into a commercial-quality local Live Board frontend, using compiled static assets served by the Python package while preserving local-first semantics.

## Dependencies

- v1.2 App Shell Refactor completed.
- View-scoped API contracts are stable enough for frontend consumption.
- Static dashboard/report outputs remain separate portable evidence artifacts.

## Target Files

- frontend/live-board/src/views/OverviewView.tsx
- frontend/live-board/src/components/charts/

## Implementation Steps

1. Render project command center.
2. Render summary KPIs, capability hints, run health, metric groups, onboarding card.
3. Use summary-only API.
4. Avoid full series load unless preview chart explicitly requests bounded data.
5. Handle no-run state.

## Acceptance Criteria

- Overview looks polished.
- Overview uses summary data.
- No-run state is useful.
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

