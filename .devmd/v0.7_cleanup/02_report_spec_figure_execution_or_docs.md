---
milestone: "v0.7-cleanup"
phase: "Report Artifact Layer Cleanup"
slice: "02_report_spec_figure_execution_or_docs"
title: "ReportSpec figure execution or docs clarification"
priority: "P0"
status: "pending"
target_version: "v0.7-cleanup"
---

# 02_report_spec_figure_execution_or_docs — ReportSpec figure execution or docs clarification

## Objective

Align `ReportSpec.md` FIG block support with actual `report build` behavior.

## Context

v0.7 Report Artifact Layer is functionally complete and CI is green. This cleanup phase resolves API, documentation, optional figure testing, and CI polish issues before starting v0.8 Agent Research Layer.

## Dependencies

- v0.7 Report Artifact Layer completed.
- Latest main CI is green.

## Target Files

- src/skilllogboard/reports/report_builder.py
- src/skilllogboard/reports/report_spec.py
- tests/test_report_builder.py
- tests/test_report_spec.py
- docs/report_artifact_layer.md
- README.md

## Implementation Steps

1. Confirm FIG blocks are parsed by ReportSpec parser.
2. Inspect current report builder behavior for spec-driven figure generation.
3. Choose path A or B: A) execute FIG items in report build, B) explicitly document v0.7 limitation.
4. Preferred path A: dispatch supported FIG types to figure builder.
5. For unsupported figure types, record a warning in `report_manifest.yaml` instead of failing the whole report.
6. If optional report dependency is missing, keep table/report generation working and record a skipped figure warning.
7. Add tests for a spec containing at least one TABLE block and one FIG block.

## Acceptance Criteria

- FIG block behavior is no longer ambiguous.
- Either FIG blocks are executed, or docs clearly state the limitation.
- Unsupported or missing optional figure generation does not break report generation.
- `report_manifest.yaml` records generated or skipped figure outputs.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_report_spec.py tests/test_report_builder.py tests/test_report_figures.py
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

