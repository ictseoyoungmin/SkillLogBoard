---
milestone: "v1.1.1"
phase: "UI Polish, True Compare, and Interaction Hardening"
day: "day4"
slice: "01_report_package_artifact_discovery"
title: "v0.7 report package artifact discovery"
priority: "P0"
status: "completed"
target_version: "v1.1.1-ui-polish-compare"
---

# 01_report_package_artifact_discovery — v0.7 report package artifact discovery

## Objective

Make artifact discovery compatible with root-level and `report/` subdirectory report packages.

## Context

v1.1 changed the Live Board into a chart-first local research workspace. v1.1.1 turns that redesign into release-candidate quality by making compare/overlay real, refining visual layout and interactions, fixing artifact discovery, and hardening tests.

## Dependencies

- v1.1 UI/UX Redesign completed.
- v1.0 Live Board behavior remains compatible.
- Existing static dashboard/report/compare/agent/template-forge behavior remains green.

## Target Files

- src/skilllogboard/live/state.py
- src/skilllogboard/live/readers.py
- tests/test_live_state.py
- tests/test_live_readers.py
- docs/live_board.md

## Implementation Steps

1. Update report artifact discovery to check both root-level and `report/` paths.
2. Detect `report.md`, `report.html`, `report_manifest.yaml`.
3. Detect files under `report/tables/` and `report/figures/`.
4. Include type, name, path, relative path, size, and modified time when available.
5. Avoid recursively scanning huge arbitrary directories.
6. Add tests for root-level report files and nested report package files.

## Acceptance Criteria

- Root-level report artifacts are still discovered.
- `report/report.md`, `report/report.html`, `report/report_manifest.yaml` are discovered.
- `report/tables/*` and `report/figures/*` are discovered.
- Artifact metadata includes path and type.
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

