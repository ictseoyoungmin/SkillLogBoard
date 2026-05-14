---
milestone: "v1.1.2"
phase: "Showcase, Visual Parity, and Demo Depth"
day: "day1"
slice: "02_rich_metric_set"
title: "rich metric set"
priority: "P0"
status: "completed"
target_version: "v1.1.2-showcase-visual-parity"
---

# 02_rich_metric_set — rich metric set

## Objective

Expand demo metrics so the Metric Workspace looks meaningfully populated.

## Context

v1.1.1 implemented true compare/overlay and core UI interaction hardening. However, the actual UI can still look less capable than the design mockups because many advanced features are hidden behind drawers, sparse demo data, and minimal affordances. v1.1.2 should improve perceived product completeness without violating local-first or lightweight-package principles.

## Dependencies

- v1.1.1 UI Polish / True Compare completed.
- Live Board core APIs remain compatible.
- Existing static dashboard/report/compare/agent/template-forge behavior remains green.

## Target Files

- examples/live_demo.py
- tests/test_live_project.py
- tests/test_live_state.py

## Implementation Steps

1. Add shared metrics: train/loss, val/loss, val/acc, val/f1, lr, grad_norm.
2. Add system-like metrics: throughput, step_time, gpu/memory if consistent with current metric schema.
3. Ensure each run has enough points to draw curves.
4. Make failed/overfit runs visibly different.
5. Update tests to assert shared metrics exist across demo-like runs.

## Acceptance Criteria

- Rich demo includes at least six shared metrics.
- Compare shared metric list is meaningfully populated.
- Curves differ across runs.
- Tests pass.

## Verification Commands

```bash
python examples/live_demo.py --multi-run --runs 5 --rich
pytest -q tests/test_live_project.py tests/test_live_state.py
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

- This milestone is about visible product completeness, not broad backend expansion.
- Prefer better demo data, empty states, affordances, and layout polish over complex systems.
- Keep the default UI minimal, but make hidden capabilities discoverable.
- Avoid fake functionality. Showcase hints must reflect actual local state or clearly available actions.

---

## Agent Completion Block

> The agent must update this block after finishing the slice.

- [x] Implementation completed
- [x] Acceptance criteria verified
- [x] Tests or smoke checks executed
- [x] No unrelated files changed
- [x] Notes added below if anything was skipped or deferred

**Status:** COMPLETED  
**Completed at:** 2026-05-14  
**Completed by:** Codex  
**Verification command(s):** .venv/bin/python -m ruff check .; .venv/bin/python -m pytest -q; .venv/bin/python examples/live_demo.py --multi-run --runs 5 --rich; .venv/bin/python examples/basic_usage.py; .venv/bin/python examples/ir_drop_example.py; .venv/bin/python examples/trajectory_example.py; .venv/bin/python -m build --no-isolation  
**Notes:** Local implementation and verification completed. Remote GitHub Actions status was not checked from this session.  

<!-- AGENT_STATUS: COMPLETED -->

