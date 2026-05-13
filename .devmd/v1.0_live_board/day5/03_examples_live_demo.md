---
milestone: "v1.0"
phase: "Local-first Live Board"
slice: "03_examples_live_demo"
title: "live demo example"
priority: "P0"
status: "completed"
target_version: "v1.0-live-board"
---

# 03_examples_live_demo — live demo example

## Objective

Add a small live demo example or instructions for generating a watchable run.

## Context

v1.0 adds a local-first live board on top of existing SkillLogBoard file-based evidence packages. It must remain optional, local, and additive.

## Target Files

- examples/live_demo.py
- docs/live_board.md
- README.md

## Implementation Steps

1. Create an example that writes a small run with metrics/events over a few steps.
2. Do not require server startup inside the example unless safe.
3. Document how to run `skilllog watch` against the generated run.
4. Keep runtime short.
5. Add smoke test if practical.

## Acceptance Criteria

- Example creates a watchable run folder.
- Docs explain how to watch it.
- Example runs quickly.
- No heavy dependencies required.

## Verification Commands

```bash
python examples/live_demo.py
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

