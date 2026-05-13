---
milestone: "v1.0"
phase: "Local-first Live Board"
slice: "05_live_docs_initial"
title: "initial live docs"
priority: "P0"
status: "completed"
target_version: "v1.0-live-board"
---

# 05_live_docs_initial — initial live docs

## Objective

Write initial user documentation for Live Board.

## Context

v1.0 adds a local-first live board on top of existing SkillLogBoard file-based evidence packages. It must remain optional, local, and additive.

## Target Files

- docs/live_board.md
- README.md
- docs/status_matrix.md

## Implementation Steps

1. Create `docs/live_board.md`.
2. Document install extra, `skilllog watch`, run mode, project mode, monitoring options, and non-goals.
3. Add README link and short example.
4. Mark Live Board v1.0 as in progress or implemented depending on completion state.

## Acceptance Criteria

- Live docs exist.
- Docs include CLI examples.
- Docs explicitly state no cloud sync/no auth/no external integrations.
- README links to live docs.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
text = Path('docs/live_board.md').read_text(encoding='utf-8')
assert 'skilllog watch' in text
print('live docs check passed')
PY
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

