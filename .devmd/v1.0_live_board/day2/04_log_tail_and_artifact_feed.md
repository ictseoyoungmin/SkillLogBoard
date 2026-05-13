---
milestone: "v1.0"
phase: "Local-first Live Board"
slice: "04_log_tail_and_artifact_feed"
title: "log tail and artifact feed"
priority: "P0"
status: "completed"
target_version: "v1.0-live-board"
---

# 04_log_tail_and_artifact_feed — log tail and artifact feed

## Objective

Implement optional log tailing and artifact feed extraction.

## Context

v1.0 adds a local-first live board on top of existing SkillLogBoard file-based evidence packages. It must remain optional, local, and additive.

## Target Files

- src/skilllogboard/live/readers.py
- tests/test_live_readers.py

## Implementation Steps

1. Implement log tail helper for a configured log file.
2. Limit output lines and bytes.
3. Implement artifact feed from artifact index or artifacts directory fallback.
4. Do not read huge files fully.
5. Add tests.

## Acceptance Criteria

- Log tail returns last N lines.
- Large files are bounded by limit.
- Artifact feed returns recent artifacts when available.
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

