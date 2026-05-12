---
milestone: "v0.7"
phase: "Report Artifact Layer"
day: "5"
slice: "05_v07_final_verification"
title: "v0.7 final verification"
priority: "P0"
status: "pending"
target_version: "v0.7-report-artifacts"
---

# 05_v07_final_verification — v0.7 final verification

## Objective

Complete final v0.7 verification and prepare candidate notes.

## Context

This closes the Report Artifact Layer milestone.

## Dependencies

- 04_backward_compatibility_regression

## Target Files

- CHANGELOG.md
- README.md
- .devmd/v0.7_report_artifact/**/*.md

## Implementation Steps

1. Run editable install with dev/dashboard extras.
2. Run optional report extra install if report extra was added.
3. Run full tests.
4. Run report-specific tests.
5. Run build no-isolation.
6. Generate at least one report artifact package in a temporary or example run.
7. Confirm report.md, report.html, report_manifest.yaml, tables, and at least one figure or skipped figure warning.
8. Update all completion blocks or document blockers.

## Acceptance Criteria

- Full test suite passes.
- Report artifact tests pass.
- Build no-isolation passes.
- Report package can be generated.
- Core dependency boundary remains intact.
- Docs are synchronized.

## Verification Commands

```bash
pip install -e ".[dev,dashboard]"
pytest -q
pytest -q tests/test_report_manifest.py tests/test_report_spec.py tests/test_report_tables.py tests/test_report_builder.py tests/test_report_rules.py tests/test_cli_report_artifacts.py
python -m build --no-isolation
```

## Non-goals

- Do not begin v0.8 Agent Research Layer implementation.

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

