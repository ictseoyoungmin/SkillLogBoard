---
milestone: "v1.1"
phase: "UI/UX Redesign and Metric Workspace"
day: "day2"
slice: "01_metric_catalog_schema"
title: "metric catalog schema"
priority: "P0"
status: "completed"
target_version: "v1.1-ui-ux-redesign"
---

# 01_metric_catalog_schema — metric catalog schema

## Objective

Add a metric catalog abstraction for search, grouping, and pinning.

## Context

v1.1 upgrades the Live Board from a functional MVP into a polished open-source research tool. The default screen must be minimal. Advanced monitoring, compare, event correlation, logs, reports, and agent evidence should appear through drawers, expandable panels, full-screen metric lab, or compare mode.

## Dependencies

- v1.0 Live Board and v1.0 cleanup completed.
- Existing static dashboard/report/compare/agent/template-forge behavior remains green.
- The UI remains local-first and file-backed.

## Target Files

- src/skilllogboard/live/state.py
- src/skilllogboard/live/readers.py
- tests/test_live_state.py
- tests/test_live_readers.py

## Implementation Steps

1. Inspect current metric series structure.
2. Add `metric_catalog` with name, group, latest value, point count, min/max, inferred type.
3. Group metrics by prefix before `/`.
4. Infer primary metric from manifest if available.
5. Keep existing fields backward-compatible.
6. Add tests with many train/val/system/custom metrics.

## Acceptance Criteria

- Metric catalog exists.
- Grouping works for prefixed/unprefixed metrics.
- Existing `latest_metrics` and `metric_series` remain available.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_live_state.py tests/test_live_readers.py
```

## Non-goals

- Do not implement TensorBoard/W&B import.
- Do not implement Prometheus/Grafana integration.
- Do not implement cloud sync.
- Do not implement multi-user auth.
- Do not add database backend.
- Do not add React/Vue/Svelte build tooling unless separately approved.
- Do not add heavy dependencies to core.
- Do not perform TestPyPI/PyPI release work in this slice.

## Handoff Notes

- Keep the default UI minimal.
- Move complexity into interaction: drawer, expand, modal, compare mode, or metric lab.
- Preserve existing API fields unless a tested additive extension is necessary.
- If an item is deferred, document the reason in the Agent Completion Block.

---

## Agent Completion Block

- [x] Implementation completed
- [x] Acceptance criteria verified
- [x] Tests or smoke checks executed
- [x] No unrelated files changed
- [x] Notes added below if anything was skipped or deferred

**Status:** COMPLETED  
**Completed at:** 2026-05-13
**Completed by:** Codex
**Verification command(s):** .venv/bin/python -m ruff check .; .venv/bin/python -m pytest -q; .venv/bin/python -m pytest -q tests/test_live_state.py tests/test_live_readers.py tests/test_live_project.py tests/test_live_server.py tests/test_live_monitoring.py tests/test_live_monitors.py tests/test_cli_live.py tests/test_live_packaging.py tests/test_live_ui_snapshot.py; .venv/bin/skilllog --help; .venv/bin/skilllog watch --help; .venv/bin/python examples/live_demo.py; .venv/bin/python examples/basic_usage.py; .venv/bin/python examples/ir_drop_example.py; .venv/bin/python examples/trajectory_example.py; .venv/bin/python -m build --no-isolation; .venv/bin/python -m skilllogboard.cli.main --version
**Notes:** Local verification completed. GitHub Actions was not checked after push because no push was performed in this session.

<!-- AGENT_STATUS: COMPLETED -->

