---
milestone: "v1.1.1"
phase: "UI Polish, True Compare, and Interaction Hardening"
day: "day7"
slice: "01_live_board_docs_compare_mode"
title: "Live Board docs for compare mode"
priority: "P0"
status: "completed"
target_version: "v1.1.1-ui-polish-compare"
---

# 01_live_board_docs_compare_mode — Live Board docs for compare mode

## Objective

Document true compare/overlay mode, metric selection, and payload limits.

## Context

v1.1 changed the Live Board into a chart-first local research workspace. v1.1.1 turns that redesign into release-candidate quality by making compare/overlay real, refining visual layout and interactions, fixing artifact discovery, and hardening tests.

## Dependencies

- v1.1 UI/UX Redesign completed.
- v1.0 Live Board behavior remains compatible.
- Existing static dashboard/report/compare/agent/template-forge behavior remains green.

## Target Files

- docs/live_board.md
- README.md

## Implementation Steps

1. Add project compare quickstart.
2. Explain compare candidates, run picker, shared metric selection, and overlay legend.
3. Explain alignment, smoothing, raw/normalized behavior, and limitations.
4. Explain payload limits and downsampling behavior.
5. Add example commands using `examples/live_demo.py`.

## Acceptance Criteria

- Docs explain how to use compare mode.
- Docs explain limitations clearly.
- README includes concise compare reference or points to docs.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
text = Path('docs/live_board.md').read_text(encoding='utf-8').lower()
assert 'compare' in text and 'overlay' in text
print('compare docs check passed')
PY
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

