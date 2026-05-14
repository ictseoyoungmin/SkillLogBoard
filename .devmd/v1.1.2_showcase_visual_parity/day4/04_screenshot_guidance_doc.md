---
milestone: "v1.1.2"
phase: "Showcase, Visual Parity, and Demo Depth"
day: "day4"
slice: "04_screenshot_guidance_doc"
title: "screenshot guidance doc"
priority: "P0"
status: "completed"
target_version: "v1.1.2-showcase-visual-parity"
---

# 04_screenshot_guidance_doc — screenshot guidance doc

## Objective

Document how to generate screenshots that represent the intended UI.

## Context

v1.1.1 implemented true compare/overlay and core UI interaction hardening. However, the actual UI can still look less capable than the design mockups because many advanced features are hidden behind drawers, sparse demo data, and minimal affordances. v1.1.2 should improve perceived product completeness without violating local-first or lightweight-package principles.

## Dependencies

- v1.1.1 UI Polish / True Compare completed.
- Live Board core APIs remain compatible.
- Existing static dashboard/report/compare/agent/template-forge behavior remains green.

## Target Files

- docs/ui_design_guidelines.md
- docs/live_board.md
- docs/release_candidate_checklist.md

## Implementation Steps

1. Add commands to generate rich demo data.
2. Add recommended screen sizes for screenshots.
3. Add checklist for screenshots: project overview, compare mode, metric lab, artifact drawer, agent workspace.
4. Clarify that rich demo is synthetic local evidence.

## Acceptance Criteria

- Screenshot guidance exists.
- Guidance covers main visual states.
- Commands are copy-pasteable.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
text = Path('docs/ui_design_guidelines.md').read_text(encoding='utf-8').lower()
assert 'screenshot' in text and 'rich demo' in text
print('screenshot guidance check passed')
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

