---
milestone: "v0.7"
phase: "Report Artifact Layer"
day: "1"
slice: "02_report_manifest_read_write"
title: "report manifest read/write"
priority: "P0"
status: "pending"
target_version: "v0.7-report-artifacts"
---

# 02_report_manifest_read_write — report manifest read/write

## Objective

Implement `report_manifest.yaml` read/write helpers.

## Context

Every generated report package should include provenance: what was generated, from which source files, and with what parameters.

## Dependencies

- 01_report_artifact_schema

## Target Files

- src/skilllogboard/reports/report_manifest.py
- tests/test_report_manifest.py

## Implementation Steps

1. Define `ReportManifest` schema or dict contract.
2. Include fields: `report_id`, `created_at`, `source`, `outputs`, `parameters`, `warnings`.
3. Implement `write_report_manifest(path, manifest)`.
4. Implement `read_report_manifest(path)`.
5. Use PyYAML already available in core dependencies.
6. Ensure output paths are stored as relative paths when practical.
7. Add tests for write/read roundtrip.

## Acceptance Criteria

- `report_manifest.yaml` can be written and read.
- Manifest includes generated table and figure outputs.
- Source metadata can include root_dir, run_count, and source files.
- Roundtrip test passes.

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
**Verification command(s):** .venv/bin/pytest -q; .venv/bin/python examples/basic_usage.py; .venv/bin/python examples/ir_drop_example.py; .venv/bin/python examples/trajectory_example.py; .venv/bin/python -m build --no-isolation
**Notes:** Implemented and verified as part of the v0.7 report artifact layer pass. Optional figure generation keeps a readable skipped-dependency fallback when matplotlib is unavailable.

<!-- AGENT_STATUS: COMPLETED -->

