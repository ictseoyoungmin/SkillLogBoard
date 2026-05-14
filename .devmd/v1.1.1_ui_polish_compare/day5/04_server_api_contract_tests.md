---
milestone: "v1.1.1"
phase: "UI Polish, True Compare, and Interaction Hardening"
day: "day5"
slice: "04_server_api_contract_tests"
title: "server API contract tests"
priority: "P0"
status: "completed"
target_version: "v1.1.1-ui-polish-compare"
---

# 04_server_api_contract_tests — server API contract tests

## Objective

Add server tests for `/api/config`, default `/api/state`, and compare-mode `/api/state`.

## Context

v1.1 changed the Live Board into a chart-first local research workspace. v1.1.1 turns that redesign into release-candidate quality by making compare/overlay real, refining visual layout and interactions, fixing artifact discovery, and hardening tests.

## Dependencies

- v1.1 UI/UX Redesign completed.
- v1.0 Live Board behavior remains compatible.
- Existing static dashboard/report/compare/agent/template-forge behavior remains green.

## Target Files

- tests/test_live_server.py
- src/skilllogboard/live/server.py

## Implementation Steps

1. Add HTTP or route-level test for `/api/config` target identity and poll interval.
2. Add default project `/api/state` test.
3. Add compare metric `/api/state` test.
4. Add invalid compare run ID test.
5. Keep tests safe without long-running server process unless existing smoke helper is used.

## Acceptance Criteria

- `/api/config` contract is tested.
- Default `/api/state` remains tested.
- Compare query behavior is tested.
- Invalid run IDs are safe.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_live_server.py tests/test_live_project.py
```

## Non-goals

- Do not implement TensorBoard/W&B import.
- Do not implement Prometheus/Grafana integration.
- Do not implement cloud sync.
- Do not implement multi-user auth.
- Do not add a database backend.
- Do not add React/Vue/Svelte build tooling unless separately approved.
- Do not add heavy dependencies to core.
- Do not perform TestPyPI/PyPI release work in this slice.

## Handoff Notes

- Keep this slice focused, but do not under-implement interaction details.
- Preserve local-first, file-based, inspectable behavior.
- Prefer additive API fields over breaking existing fields.
- Default UI should remain minimal; advanced detail belongs in drawer, tray, modal, or compare mode.
- If an item is deferred, update docs/status and record the reason in the Agent Completion Block.

---

## Agent Completion Block

- [x] Implementation completed
- [x] Acceptance criteria verified
- [x] Tests or smoke checks executed
- [x] No unrelated files changed
- [x] Notes added below if anything was skipped or deferred

**Status:** COMPLETED  
**Completed at:** 2026-05-14  
**Completed by:** Codex  
**Verification command(s):** `.venv/bin/python -m ruff check .`; `.venv/bin/python -m pytest`; `.venv/bin/python -m build --no-isolation`; `.venv/bin/python examples/live_demo.py --multi-run --runs 2`; `.venv/bin/python -c "import skilllogboard; print(skilllogboard.__version__)"`; `.venv/bin/skilllog --version`  
**Notes:** Completed locally. No deferred implementation items. Publishing and external CI execution were not performed.  

<!-- AGENT_STATUS: COMPLETED -->

