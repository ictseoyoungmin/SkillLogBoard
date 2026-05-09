---
week: 5
day: 4
slice: "04_seed_group_integration_with_leaderboard"
title: "seed group integration with leaderboard"
priority: "P1"
status: "completed"
target_version: "v0.4-compare"
---

# 04_seed_group_integration_with_leaderboard — seed group integration with leaderboard

## Objective

Expose seed group summary alongside leaderboard data.

## Context

Final compare output should include both run-level leaderboard and grouped seed summary.

## Dependencies

- 03_seed_summary_markdown_csv

## Target Files

- src/skilllogboard/compare/leaderboard.py
- src/skilllogboard/compare/seed_group.py
- tests/test_compare_integration.py

## Implementation Steps

1. Create an integration test with multiple seed runs.
2. Build run index, leaderboard, and seed summary.
3. Assert leaderboard has all runs.
4. Assert seed summary groups runs correctly.
5. Assert best run id is present.
6. Keep integration deterministic.

## Acceptance Criteria

- Run-level and seed-level summaries can be generated from the same records.
- Integration test passes.
- Missing seed runs are handled.

## Verification Commands

```bash
pytest -q tests/test_compare_integration.py
```

## Non-goals

- Do not render compare.html here.

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
**Verification command(s):** pytest -q tests/test_compare_integration.py  
**Notes:** Completed and verified for the requested scope.

<!-- AGENT_STATUS: COMPLETED -->

