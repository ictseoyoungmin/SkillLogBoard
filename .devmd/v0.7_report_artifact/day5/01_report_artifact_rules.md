---
milestone: "v0.7"
phase: "Report Artifact Layer"
day: "5"
slice: "01_report_artifact_rules"
title: "report artifact rules"
priority: "P0"
status: "pending"
target_version: "v0.7-report-artifacts"
---

# 01_report_artifact_rules — report artifact rules

## Objective

Implement report artifact validation rules: `required_table`, `required_figure`, `report_manifest_required`, and optionally `report_section_required`.

## Context

Report artifacts should be validated through the existing rule audit philosophy.

## Dependencies

- day4 report builder slices completed.

## Target Files

- src/skilllogboard/skills/report_rules.py
- src/skilllogboard/skills/rules.py
- tests/test_report_rules.py

## Implementation Steps

1. Add `report_rules.py` or extend existing rule registry cleanly.
2. Implement `required_table` rule.
3. Implement `required_figure` rule.
4. Implement `report_manifest_required` rule.
5. Optionally implement `report_section_required` if simple.
6. Rules should return structured RuleResult objects.
7. Missing report directory should produce readable warning/error, not crash.
8. Add tests.

## Acceptance Criteria

- `required_table` works.
- `required_figure` works.
- `report_manifest_required` works.
- Rules integrate with existing RuleEngine or are clearly callable from report check.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_report_rules.py tests/test_skills_rules.py
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

