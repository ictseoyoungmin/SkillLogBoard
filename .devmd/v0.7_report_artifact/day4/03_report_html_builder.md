---
milestone: "v0.7"
phase: "Report Artifact Layer"
day: "4"
slice: "03_report_html_builder"
title: "report HTML builder"
priority: "P0"
status: "pending"
target_version: "v0.7-report-artifacts"
---

# 03_report_html_builder — report HTML builder

## Objective

Generate a static `report.html` version of the report.

## Context

HTML report should be static and file-system openable, consistent with existing SkillLogBoard static dashboard philosophy.

## Dependencies

- 02_report_markdown_builder

## Target Files

- src/skilllogboard/reports/report_builder.py
- src/skilllogboard/reports/templates/report.html.j2
- tests/test_report_builder.py

## Implementation Steps

1. Create an HTML report template or a minimal fallback renderer.
2. Use standalone HTML structure with doctype, html, head, body.
3. Render summary, generated tables, generated figures, and provenance.
4. Keep styling minimal.
5. Avoid external CDN dependencies.
6. Add tests for HTML structure and core sections.

## Acceptance Criteria

- `report.html` is generated.
- HTML contains doctype/html/head/body.
- HTML includes tables/figures/provenance sections.
- No external server is required.
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

