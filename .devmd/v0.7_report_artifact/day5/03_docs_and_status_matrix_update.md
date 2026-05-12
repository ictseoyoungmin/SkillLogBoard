---
milestone: "v0.7"
phase: "Report Artifact Layer"
day: "5"
slice: "03_docs_and_status_matrix_update"
title: "docs and status matrix update"
priority: "P0"
status: "pending"
target_version: "v0.7-report-artifacts"
---

# 03_docs_and_status_matrix_update — docs and status matrix update

## Objective

Document v0.7 report artifact features and update implementation status.

## Context

Docs must distinguish implemented report artifact features from planned agent/live/template-forge features.

## Dependencies

- 02_report_check_cli

## Target Files

- README.md
- CHANGELOG.md
- docs/status_matrix.md
- docs/report_artifact_layer.md
- docs/reporting.md

## Implementation Steps

1. Create or update `docs/report_artifact_layer.md`.
2. Document `skilllog report build`.
3. Document `skilllog export-table --table ...`.
4. Document `skilllog export-figure` and optional report extra.
5. Update status matrix for report artifact features.
6. Keep AgentSkills, Template Forge, and Live Board marked Planned.
7. Add CHANGELOG v0.7 entry.

## Acceptance Criteria

- Report artifact docs exist.
- README contains report build/export-table/export-figure examples.
- Status matrix marks v0.7 implemented features accurately.
- Planned features remain Planned.
- CHANGELOG contains v0.7 entry.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
readme = Path('README.md').read_text(encoding='utf-8')
assert 'report build' in readme or 'skilllog report' in readme
status = Path('docs/status_matrix.md').read_text(encoding='utf-8')
assert 'Report' in status
print('docs/status checks passed')
PY
```

## Non-goals

- Do not implement unrelated future features.

## Handoff Notes

- Keep this slice focused and small.
- Preserve existing v0.6 public APIs and run folder compatibility.
- Existing `summary.md`, `dashboard.html`, `compare.md`, `compare.html`, and `export-table` behavior must not regress.
- Core install must remain lightweight. Do not add matplotlib, pandas, torch, lightning, sklearn, or domain packages to core dependencies.
- If a blocker appears, document it in the Agent Completion Block instead of expanding scope.

---

## Agent Completion Block

> The agent must update this block after finishing the slice.

- [x] Implementation completed
- [x] Acceptance criteria verified
- [x] Tests or smoke checks executed
- [x] No unrelated files changed
- [x] Notes added below if anything was skipped or deferred

**Status:** COMPLETED
**Completed at:** 2026-05-12
**Completed by:** Codex
**Verification command(s):** .venv/bin/pytest -q; .venv/bin/python examples/basic_usage.py; .venv/bin/python examples/ir_drop_example.py; .venv/bin/python examples/trajectory_example.py; .venv/bin/python -m build --no-isolation
**Notes:** Implemented and verified as part of the v0.7 report artifact layer pass. Optional figure generation keeps a readable skipped-dependency fallback when matplotlib is unavailable.

<!-- AGENT_STATUS: COMPLETED -->

