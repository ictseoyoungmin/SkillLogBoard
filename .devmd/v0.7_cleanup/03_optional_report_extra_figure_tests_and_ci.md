---
milestone: "v0.7-cleanup"
phase: "Report Artifact Layer Cleanup"
slice: "03_optional_report_extra_figure_tests_and_ci"
title: "optional report extra figure tests and CI"
priority: "P0"
status: "pending"
target_version: "v0.7-cleanup"
---

# 03_optional_report_extra_figure_tests_and_ci — optional report extra figure tests and CI

## Objective

Strengthen confidence that figure generation works when optional `report` extra is installed while keeping minimal install lightweight.

## Context

v0.7 Report Artifact Layer is functionally complete and CI is green. This cleanup phase resolves API, documentation, optional figure testing, and CI polish issues before starting v0.8 Agent Research Layer.

## Dependencies

- v0.7 Report Artifact Layer completed.
- Latest main CI is green.

## Target Files

- pyproject.toml
- .github/workflows/ci.yml
- tests/test_report_figures.py
- tests/test_cli_report_artifacts.py
- README.md
- docs/report_artifact_layer.md

## Implementation Steps

1. Confirm `report` extra exists and includes the plotting dependency.
2. Confirm the plotting dependency is not in core dependencies.
3. Ensure `tests/test_report_figures.py` tests metric curve and at least one aggregate figure when plotting dependency is available.
4. Ensure figure tests skip gracefully when optional dependency is absent.
5. Add CI step or job that installs `.[dev,dashboard,report]` and runs figure-specific tests.
6. Keep default lightweight CI path intact.
7. Document optional report extra install command.

## Acceptance Criteria

- Core dependencies remain lightweight.
- `pip install -e ".[dev,dashboard,report]"` is documented.
- Figure tests pass when report extra is installed.
- Minimal tests do not fail when plotting dependency is absent.
- CI includes optional report-extra verification or a documented deferral.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
import tomllib
p = tomllib.loads(Path('pyproject.toml').read_text(encoding='utf-8'))
core = '\n'.join(p['project'].get('dependencies', [])).lower()
assert 'matplotlib' not in core
assert 'report' in p['project'].get('optional-dependencies', {})
print('report extra boundary OK')
PY
pip install -e ".[dev,dashboard,report]"
pytest -q tests/test_report_figures.py tests/test_cli_report_artifacts.py
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

