---
milestone: "v0.7-cleanup"
phase: "Report Artifact Layer Cleanup"
slice: "04_readme_placeholder_and_docs_polish"
title: "README placeholder and docs polish"
priority: "P0"
status: "pending"
target_version: "v0.7-cleanup"
---

# 04_readme_placeholder_and_docs_polish — README placeholder and docs polish

## Objective

Fix Markdown placeholder rendering issues and synchronize v0.7 report docs with actual behavior.

## Context

v0.7 Report Artifact Layer is functionally complete and CI is green. This cleanup phase resolves API, documentation, optional figure testing, and CI polish issues before starting v0.8 Agent Research Layer.

## Dependencies

- v0.7 Report Artifact Layer completed.
- Latest main CI is green.

## Target Files

- README.md
- docs/report_artifact_layer.md
- docs/status_matrix.md
- docs/templates.md
- CHANGELOG.md

## Implementation Steps

1. Search README/docs for angle-bracket placeholders such as `<run_id>`, `<project>`, `<metric>`.
2. Replace ambiguous angle-bracket placeholders with `{run_id}`, `{project}`, `{metric}`, or `RUN_ID`.
3. Fix rendered text where placeholders disappeared, such as `runs/demo//`.
4. Ensure README v0.7 examples use actual CLI command names.
5. Ensure docs distinguish v0.7 implemented features from v0.8/v0.9/v1.0 planned features.
6. Update CHANGELOG with a small v0.7 cleanup note if appropriate.

## Acceptance Criteria

- README no longer contains broken `runs/demo//` style paths.
- Angle-bracket placeholders are replaced or escaped.
- Report docs match actual CLI/API behavior.
- Status matrix accurately marks v0.7 implemented and v0.8+ planned.
- Docs checks pass.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
for path in [Path('README.md'), Path('docs/report_artifact_layer.md')]:
    if path.exists():
        text = path.read_text(encoding='utf-8')
        assert 'runs/demo//' not in text, f'broken placeholder path in {path}'
print('README/docs placeholder check passed')
PY
```

## Non-goals

- Do not begin v0.8 Agent Research Layer implementation.
- Do not implement Template Forge or Live Board.
- Do not change public RunLogger APIs.
- Do not add heavy dependencies to core.

## Handoff Notes

- Keep this cleanup focused.
- Preserve v0.7 behavior and all existing tests.
- If an item is deferred, update docs and record the reason below.

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
**Verification command(s):** .venv/bin/ruff check .; .venv/bin/pytest -q; .venv/bin/pytest -q tests/test_report_figures.py tests/test_cli_report_artifacts.py; .venv/bin/python examples/basic_usage.py; .venv/bin/python examples/ir_drop_example.py; .venv/bin/python examples/trajectory_example.py; .venv/bin/python -m build --no-isolation
**Notes:** Completed v0.7 cleanup: public report API exports, ReportSpec FIG execution/skipped-warning behavior, optional report-extra tests and CI job, docs placeholder polish, and final local verification.

<!-- AGENT_STATUS: COMPLETED -->

