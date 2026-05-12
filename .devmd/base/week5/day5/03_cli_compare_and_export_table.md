---
week: 5
day: 5
slice: "03_cli_compare_and_export_table"
title: "CLI compare and export-table"
priority: "P0"
status: "completed"
target_version: "v0.4-compare"
---

# 03_cli_compare_and_export_table — CLI compare and export-table

## Objective

Implement final Week 5 CLI workflows for compare and table export.

## Context

D25 requires CLI compare/export-table. Replace planned placeholders with working commands.

## Dependencies

- 01_compare_report_builder
- 02_compare_html_builder

## Target Files

- src/skilllogboard/cli/main.py
- tests/test_cli_compare.py

## Implementation Steps

1. Implement `skilllog compare RUNS_DIR --metric METRIC --mode max|min --output-dir DIR`.
2. Command should generate compare.html, compare.md, and compare.csv.
3. Implement `skilllog export-table RUNS_DIR --metric METRIC --format csv|md|latex --output PATH`.
4. For LaTeX, generate a simple tabular-like text output; do not require external dependencies.
5. Return readable errors for missing runs or no metrics.
6. Add CLI tests.

## Acceptance Criteria

- `skilllog compare` generates compare outputs.
- `skilllog export-table --format csv` works.
- `skilllog export-table --format md` works.
- `skilllog export-table --format latex` creates a usable text table.
- CLI tests pass.

## Verification Commands

```bash
pytest -q tests/test_cli_compare.py
```

## Non-goals

- Do not implement W&B export/import.

## Handoff Notes

- Keep the slice small and focused.
- Preserve the public API already working after Week 4.
- Do not implement Week 6+ research plugins unless this slice explicitly asks for a placeholder.
- Do not hide unsupported or planned features in docs; label them clearly.
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
**Completed at:** 2026-05-10 00:36  
**Completed by:** coding agent  
**Verification command(s):** pytest -q tests/test_cli_compare.py  
**Notes:** Completed and verified for the requested scope.

<!-- AGENT_STATUS: COMPLETED -->

