---
week: 2
day: 3
slice: "04_table_writer_csv_html_support"
title: "table writer CSV and optional HTML support"
priority: "P1"
status: "completed"
target_version: "v0.1-mvp"
---

# 04_table_writer_csv_html_support — table writer CSV and optional HTML support

## Objective

Implement `log_table()` with dependency-light CSV support and optional HTML behavior.

## Context

Tables are important for leaderboard, ablation, and report outputs. Week 2 should provide a simple table logging foundation without requiring pandas in core.

## Dependencies

- 01_artifact_store_index_and_metadata

## Target Files

- src/skilllogboard/writers/table_writer.py
- src/skilllogboard/core/logger.py
- tests/test_table_writer.py

## Implementation Steps

1. Implement `log_table(name, table, **metadata)` in RunLogger.
2. Support a list of dictionaries as the dependency-free MVP table input.
3. If pandas is installed and a DataFrame is provided, support `to_csv` and optionally `to_html`.
4. Store tables under `tables/`.
5. Record table metadata in an index or artifact index.
6. Emit a table event.
7. Add tests for list-of-dicts input.
8. Add pandas-specific test only if it can be skipped when pandas is unavailable.

## Acceptance Criteria

- List-of-dicts table logging writes a CSV file.
- Table event is appended to `events.jsonl`.
- Core package does not require pandas.
- Tests pass without pandas unless optional tests are skipped correctly.

## Verification Commands

```bash
pytest -q tests/test_table_writer.py
```

## Non-goals

- Do not implement multi-run ablation export here.

## Handoff Notes

- Keep this slice focused on Week 2 MVP behavior.
- Preserve the public API described in the docs unless this slice explicitly changes it.
- Prefer backward-compatible changes to the Week 1 skeleton.
- Do not start Week 3 dashboard work beyond the placeholder hooks required by `finish()`.
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
**Completed at:** 2026-05-09 22:20  
**Completed by:** coding agent  
**Verification command(s):** pytest -q tests/test_table_writer.py  
**Notes:** Completed for Week 2 v0.1 MVP scope only.  

<!-- AGENT_STATUS: COMPLETED -->
