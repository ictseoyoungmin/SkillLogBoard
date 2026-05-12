---
milestone: "v0.7"
phase: "Report Artifact Layer"
day: "1"
slice: "01_report_artifact_schema"
title: "report artifact schema"
priority: "P0"
status: "completed"
target_version: "v0.7-report-artifacts"
---

# 01_report_artifact_schema — report artifact schema

## Objective

Define the schema for generated report artifacts such as tables, figures, and report files.

## Context

v0.7 needs a common representation for report outputs before building tables, figures, or manifests.

## Dependencies

- v0.6 release candidate completed.

## Target Files

- src/skilllogboard/reports/__init__.py
- src/skilllogboard/reports/report_manifest.py
- tests/test_report_manifest.py

## Implementation Steps

1. Create the `src/skilllogboard/reports/` package if it does not exist.
2. Define a lightweight `ReportArtifact` dataclass or JSON-serializable dict schema.
3. Required fields: `id`, `type`, `path`, `kind`, `title`, `source_files`, `metadata`.
4. Use Python 3.9-compatible typing; avoid `list[str]` unless `from __future__ import annotations` is already used consistently.
5. Add helper to convert a report artifact to a plain dict.
6. Add tests for table, figure, and report artifact records.

## Acceptance Criteria

- `ReportArtifact` or equivalent schema exists.
- Schema can represent table, figure, and report outputs.
- Schema is JSON/YAML serializable.
- Tests pass on Python 3.9-compatible syntax.

## Verification Commands

```bash
pytest -q tests/test_report_manifest.py
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
**Verification command(s):** .venv/bin/pytest -q; .venv/bin/python -m build --no-isolation
**Notes:** Implemented v0.7 report artifact layer with optional figure dependency fallback and compatibility checks.

<!-- AGENT_STATUS: COMPLETED -->
