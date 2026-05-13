---
milestone: "v1.0"
phase: "Local-first Live Board"
slice: "02_live_file_readers"
title: "live file readers"
priority: "P0"
status: "completed"
target_version: "v1.0-live-board"
---

# 02_live_file_readers — live file readers

## Objective

Implement safe readers for manifest, metrics, events, skill trace, and artifact index.

## Context

v1.0 adds a local-first live board on top of existing SkillLogBoard file-based evidence packages. It must remain optional, local, and additive.

## Target Files

- src/skilllogboard/live/readers.py
- tests/test_live_readers.py

## Implementation Steps

1. Implement readers for `manifest.yaml`, `metrics.csv`, `events.jsonl`, `skill_trace.jsonl`, and artifact index if present.
2. Readers must handle missing files gracefully.
3. Implement simple tail/limit behavior for events and traces.
4. Avoid pandas dependency.
5. Add tests with temporary run folders.

## Acceptance Criteria

- Readers work without pandas.
- Missing files produce warnings, not crashes.
- Metrics/events/traces can be read from fixtures.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_live_readers.py
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

