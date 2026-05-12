---
milestone: "v0.7"
phase: "Report Artifact Layer"
day: "1"
slice: "03_report_spec_contract"
title: "report spec contract"
priority: "P0"
status: "pending"
target_version: "v0.7-report-artifacts"
---

# 03_report_spec_contract — report spec contract

## Objective

Define the supported `ReportSpec.md` block syntax.

## Context

ReportSpec should use a simple Markdown/YAML-like block style aligned with the existing Skills.md parser philosophy.

## Dependencies

- 02_report_manifest_read_write

## Target Files

- src/skilllogboard/reports/report_spec.py
- tests/test_report_spec.py
- docs/report_artifact_layer.md

## Implementation Steps

1. Create `report_spec.py`.
2. Document supported blocks: `REPORT-*`, `TABLE-*`, `FIG-*`.
3. Support simple bullet metadata such as `- type: leaderboard`, `- metric: val/acc`, `- output: report/tables/leaderboard.md`.
4. Support list values such as `- group_by: [model_name, seed]`.
5. Define spec item fields: `id`, `kind`, `type`, `metric`, `mode`, `group_by`, `metrics`, `output`, `title`.
6. Add parser contract tests with one report block, one table block, and one figure block.

## Acceptance Criteria

- ReportSpec syntax is documented in code or docs.
- Contract tests cover REPORT/TABLE/FIG blocks.
- Unsupported arbitrary Markdown is ignored safely or reported clearly.
- No complex DSL is introduced.

## Verification Commands

```bash
pytest -q tests/test_report_spec.py
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

