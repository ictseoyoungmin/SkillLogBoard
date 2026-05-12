---
milestone: "v0.7"
phase: "Report Artifact Layer"
day: "1"
slice: "04_report_spec_parser"
title: "report spec parser"
priority: "P0"
status: "pending"
target_version: "v0.7-report-artifacts"
---

# 04_report_spec_parser — report spec parser

## Objective

Implement parser support for `ReportSpec.md` and `.skilllog/report_spec.md`.

## Context

The report builder will use this parser to know which tables and figures to generate.

## Dependencies

- 03_report_spec_contract

## Target Files

- src/skilllogboard/reports/report_spec.py
- tests/test_report_spec.py

## Implementation Steps

1. Implement `ReportSpecItem` dataclass or dict schema.
2. Implement `parse_report_spec_text(text)`.
3. Implement `parse_report_spec(path)`.
4. Extract item IDs from headings like `## TABLE-LEADERBOARD`.
5. Infer item kind from heading prefix if kind is not explicitly provided.
6. Parse scalar and list metadata.
7. Add tests for multiple table/figure blocks.
8. Add tests for malformed block behavior.

## Acceptance Criteria

- `parse_report_spec_text()` returns ordered spec items.
- Each item includes id, kind, type, output, and params.
- Multiple blocks parse deterministically.
- Malformed required fields produce readable errors or warnings.

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

