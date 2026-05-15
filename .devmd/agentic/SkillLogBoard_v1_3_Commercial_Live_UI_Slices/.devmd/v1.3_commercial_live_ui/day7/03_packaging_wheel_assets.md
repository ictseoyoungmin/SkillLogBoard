---
milestone: "v1.3"
phase: "Commercial Live UI"
day: "day7"
slice: "03_packaging_wheel_assets"
title: "package wheel assets"
priority: "P0"
status: "pending"
target_version: "v1.3"
---

# 03_packaging_wheel_assets — package wheel assets

## Objective

Ensure built frontend assets are included in wheel/sdist.

## Context

v1.3 upgrades the v1.2 app shell into a commercial-quality local Live Board frontend, using compiled static assets served by the Python package while preserving local-first semantics.

## Dependencies

- v1.2 App Shell Refactor completed.
- View-scoped API contracts are stable enough for frontend consumption.
- Static dashboard/report outputs remain separate portable evidence artifacts.

## Target Files

- pyproject.toml
- MANIFEST.in
- tests/test_live_packaging.py

## Implementation Steps

1. Add package data for built frontend assets.
2. Add test that package resource can locate app entry and CSS/JS.
3. Run build no-isolation.
4. Do not include node_modules in package.

## Acceptance Criteria

- Wheel includes built assets.
- node_modules is excluded.
- Build passes.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_live_packaging.py
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

