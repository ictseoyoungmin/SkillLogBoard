---
milestone: "v0.7"
phase: "Report Artifact Layer"
day: "4"
slice: "04_report_manifest_integration"
title: "report manifest integration"
priority: "P0"
status: "pending"
target_version: "v0.7-report-artifacts"
---

# 04_report_manifest_integration — report manifest integration

## Objective

Integrate report manifest generation into the report builder.

## Context

Report artifacts need provenance so humans and agents can verify where tables and figures came from.

## Dependencies

- 03_report_html_builder

## Target Files

- src/skilllogboard/reports/report_builder.py
- src/skilllogboard/reports/report_manifest.py
- tests/test_report_builder.py
- tests/test_report_manifest.py

## Implementation Steps

1. Generate `report_manifest.yaml` during report build.
2. Record source root/run directories.
3. Record generated reports, tables, and figures.
4. Record parameters such as metric, mode, group_by, spec path.
5. Record warnings/skipped optional figures.
6. Add tests for manifest contents.

## Acceptance Criteria

- `report_manifest.yaml` is generated.
- Manifest lists generated table artifacts.
- Manifest lists generated figure artifacts or skipped warnings.
- Manifest records source and parameters.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_report_builder.py tests/test_report_manifest.py
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

