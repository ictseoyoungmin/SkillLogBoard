---
milestone: "v1.0"
phase: "Local-first Live Board"
slice: "01_live_ui_layout_single_run"
title: "live UI single-run layout"
priority: "P0"
status: "completed"
target_version: "v1.0-live-board"
---

# 01_live_ui_layout_single_run — live UI single-run layout

## Objective

Implement browser UI layout for single-run live dashboard.

## Context

v1.0 adds a local-first live board on top of existing SkillLogBoard file-based evidence packages. It must remain optional, local, and additive.

## Target Files

- src/skilllogboard/live/templates/live.html
- tests/test_live_ui_snapshot.py

## Implementation Steps

1. Build a clean static HTML layout with topbar, sidebar, run header, KPI cards, metric chart placeholders, rule audit, event timeline, artifact feed, and log panel.
2. Use vanilla JS polling `/api/state`.
3. Keep CSS inline or packaged locally.
4. Add lightweight snapshot/string tests.

## Acceptance Criteria

- Single-run UI contains required panels.
- UI polls `/api/state`.
- No external CDN usage.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_live_ui_snapshot.py tests/test_live_packaging.py
```

## Non-goals

- Do not implement TensorBoard/W&B import.
- Do not implement Prometheus/Grafana integration.
- Do not implement cloud sync.
- Do not implement multi-user auth.
- Do not add database backend.
- Do not replace static dashboard/report/compare.
- Do not add heavy dependencies to core.

## Handoff Notes

- Keep this slice focused and small.
- Preserve all existing v0.6-v0.9 behavior.
- Missing optional live dependencies must produce readable messages or skipped tests.
- The Live Board should watch local files; it should not become a SaaS/observability platform.

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
**Verification command(s):** .venv/bin/python -m ruff check .; .venv/bin/python -m pytest -q; .venv/bin/python -m build --no-isolation; .venv/bin/python examples/live_demo.py
**Notes:** Isolated python -m build could not create an ensurepip venv in this environment, so package verification was rerun successfully with --no-isolation.

<!-- AGENT_STATUS: COMPLETED -->

