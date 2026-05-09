---
week: 5
day: 2
slice: "03_leaderboard_csv_markdown_export"
title: "leaderboard CSV and Markdown export"
priority: "P1"
status: "completed"
target_version: "v0.4-compare"
---

# 03_leaderboard_csv_markdown_export — leaderboard CSV and Markdown export

## Objective

Export leaderboard rows to CSV and Markdown table.

## Context

Week 5 output includes compare.csv/md. Start with leaderboard exports.

## Dependencies

- 02_leaderboard_builder

## Target Files

- src/skilllogboard/compare/leaderboard.py
- src/skilllogboard/reports/markdown_report.py
- tests/test_leaderboard.py

## Implementation Steps

1. Implement `write_leaderboard_csv(rows, path)` or equivalent.
2. Implement `leaderboard_to_markdown(rows)`.
3. Use stable column order.
4. Escape Markdown pipes in text fields if needed.
5. Add tests for CSV file and Markdown string.

## Acceptance Criteria

- CSV export writes header and rows.
- Markdown export contains a valid table delimiter row.
- Exports are deterministic.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_leaderboard.py
```

## Non-goals

- Do not implement LaTeX export here.

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
**Verification command(s):** pytest -q tests/test_leaderboard.py  
**Notes:** Completed and verified for the requested scope.

<!-- AGENT_STATUS: COMPLETED -->

