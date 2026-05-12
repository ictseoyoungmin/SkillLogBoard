---
milestone: "v0.7"
phase: "Report Artifact Layer"
day: "4"
slice: "02_report_markdown_builder"
title: "report Markdown builder"
priority: "P0"
status: "pending"
target_version: "v0.7-report-artifacts"
---

# 02_report_markdown_builder — report Markdown builder

## Objective

Generate `report.md` with references to generated tables, figures, and provenance.

## Context

Markdown is the primary report artifact because it is Git-friendly and easy for humans and agents to read.

## Dependencies

- 01_report_output_layout

## Target Files

- src/skilllogboard/reports/report_builder.py
- tests/test_report_builder.py

## Implementation Steps

1. Implement Markdown report generation.
2. Include sections: Summary, Source Runs, Leaderboard, Tables, Figures, Rule Audit, Provenance, Warnings.
3. Reference generated table and figure file paths.
4. Include placeholder `Key Findings` section without attempting LLM narrative generation.
5. Add tests that assert section headings and links.

## Acceptance Criteria

- `report.md` is generated.
- Report contains expected sections.
- Report references generated tables and figures.
- Report includes provenance section.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_report_builder.py
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

