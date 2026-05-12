---
milestone: "v0.7"
phase: "Report Artifact Layer"
day: "5"
slice: "04_backward_compatibility_regression"
title: "backward compatibility regression"
priority: "P0"
status: "pending"
target_version: "v0.7-report-artifacts"
---

# 04_backward_compatibility_regression — backward compatibility regression

## Objective

Run regression checks to ensure v0.7 did not break v0.6 functionality.

## Context

v0.7 is additive. Existing logger, dashboard, compare, templates, and release-hardening tests must remain green.

## Dependencies

- 03_docs_and_status_matrix_update

## Target Files

- tests/
- examples/
- .devmd/v0.7_report_artifact/day5/04_backward_compatibility_regression.md

## Implementation Steps

1. Run full test suite.
2. Run basic example.
3. Run IR-drop and trajectory examples.
4. Run compare-related tests.
5. Run dashboard packaging tests.
6. Fix only regressions caused by v0.7 changes.
7. Record results in this slice completion block.

## Acceptance Criteria

- `pytest -q` passes.
- `python examples/basic_usage.py` passes.
- `python examples/ir_drop_example.py` passes.
- `python examples/trajectory_example.py` passes.
- Existing compare/dashboard behavior remains intact.

## Verification Commands

```bash
pytest -q
python examples/basic_usage.py
python examples/ir_drop_example.py
python examples/trajectory_example.py
```

## Non-goals

- Do not add new features in this regression slice.

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

