---
milestone: "v1.1"
phase: "UI/UX Redesign and Metric Workspace"
day: "day6"
slice: "02_docs_design_guidelines_update"
title: "docs and design guideline update"
priority: "P0"
status: "completed"
target_version: "v1.1-ui-ux-redesign"
---

# 02_docs_design_guidelines_update — docs and design guideline update

## Objective

Document the v1.1 interaction model, metric workspace, compare mode, and visual guidelines.

## Context

v1.1 upgrades the Live Board from a functional MVP into a polished open-source research tool. The default screen must be minimal. Advanced monitoring, compare, event correlation, logs, reports, and agent evidence should appear through drawers, expandable panels, full-screen metric lab, or compare mode.

## Dependencies

- v1.0 Live Board and v1.0 cleanup completed.
- Existing static dashboard/report/compare/agent/template-forge behavior remains green.
- The UI remains local-first and file-backed.

## Target Files

- docs/live_board.md
- docs/ui_design_guidelines.md
- README.md
- docs/status_matrix.md
- CHANGELOG.md

## Implementation Steps

1. Create/update `docs/ui_design_guidelines.md`.
2. Document visual direction, tokens, layout regions, drawers, metric workspace, compare mode, local-first constraints.
3. Update live docs with v1.1 interactions.
4. Update README, status matrix, and changelog.
5. Keep unsupported integrations out of scope.

## Acceptance Criteria

- UI guideline doc exists.
- Docs explain metric selection and compare/overlay mode.
- Docs explain drawer/tray detail model.
- Status/changelog reflect v1.1.
- Docs do not claim unsupported features.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
text = Path('docs/ui_design_guidelines.md').read_text(encoding='utf-8')
assert 'Metric Workspace' in text or 'metric workspace' in text.lower()
assert 'compare' in text.lower()
print('UI guideline docs check passed')
PY
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

