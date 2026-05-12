---
milestone: "v0.7-cleanup"
phase: "Report Artifact Layer Cleanup"
slice: "01_reports_public_api_exports"
title: "reports public API exports"
priority: "P0"
status: "pending"
target_version: "v0.7-cleanup"
---

# 01_reports_public_api_exports — reports public API exports

## Objective

Expose intended v0.7 report APIs from `skilllogboard.reports` so documentation examples are importable.

## Context

v0.7 Report Artifact Layer is functionally complete and CI is green. This cleanup phase resolves API, documentation, optional figure testing, and CI polish issues before starting v0.8 Agent Research Layer.

## Dependencies

- v0.7 Report Artifact Layer completed.
- Latest main CI is green.

## Target Files

- src/skilllogboard/reports/__init__.py
- tests/test_reports_public_api.py
- README.md
- docs/report_artifact_layer.md

## Implementation Steps

1. Inspect current exports in `src/skilllogboard/reports/__init__.py`.
2. Export manifest objects/helpers that already exist.
3. Export table builder public entry point, using the actual implemented name or a stable alias.
4. Export report builder public entry point, such as `build_report_package` or a documented alias.
5. Export intended figure builder public entry points.
6. Export ReportSpec parser helpers if implemented.
7. Add `__all__` if consistent with package style.
8. Add tests that import documented names from `skilllogboard.reports`.
9. Update README/docs examples if function names differ from the original plan.

## Acceptance Criteria

- `from skilllogboard.reports import ...` works for documented report APIs.
- A public API test covers the exported names.
- README/docs examples match actual exported names.
- No circular import or optional matplotlib import error occurs on minimal install.

## Verification Commands

```bash
pytest -q tests/test_reports_public_api.py
python - <<'PY'
import skilllogboard.reports as reports
print('reports public API import OK:', reports.__name__)
PY
pytest -q tests/test_report_manifest.py tests/test_report_spec.py tests/test_report_tables.py tests/test_report_builder.py
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

