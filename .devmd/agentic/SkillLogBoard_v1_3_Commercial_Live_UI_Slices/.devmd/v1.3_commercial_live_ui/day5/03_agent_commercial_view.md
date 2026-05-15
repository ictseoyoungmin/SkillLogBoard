---
milestone: "v1.3"
phase: "Commercial Live UI"
day: "day5"
slice: "03_agent_commercial_view"
title: "commercial Agent view"
priority: "P0"
status: "pending"
target_version: "v1.3"
---

# 03_agent_commercial_view — commercial Agent view

## Objective

Implement polished Agent Evidence view.

## Context

v1.3 upgrades the v1.2 app shell into a commercial-quality local Live Board frontend, using compiled static assets served by the Python package while preserving local-first semantics.

## Dependencies

- v1.2 App Shell Refactor completed.
- View-scoped API contracts are stable enough for frontend consumption.
- Static dashboard/report outputs remain separate portable evidence artifacts.

## Target Files

- frontend/live-board/src/views/AgentView.tsx
- frontend/live-board/src/components/agent/

## Implementation Steps

1. Render agent activity timeline.
2. Render safety gate, rules status, evidence files, handoff details.
3. Show next actions if structured handoff exists.
4. Avoid implying SkillLogBoard executes agents unless future feature exists.
5. Add empty state for no agent evidence.

## Acceptance Criteria

- Agent view is polished and honest.
- Local evidence paths are visible.
- No unsupported LLM execution claims.
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

