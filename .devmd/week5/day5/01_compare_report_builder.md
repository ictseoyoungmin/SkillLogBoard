---
week: 5
day: 5
slice: "01_compare_report_builder"
title: "compare report builder"
priority: "P0"
status: "pending"
target_version: "v0.4-compare"
---

# 01_compare_report_builder — compare report builder

## Objective

Build compare report outputs from leaderboard, config diff, ablation axes, and seed summary.

## Context

D25 requires compare.html/csv/md export. This slice creates the report builder contract.

## Dependencies

- day1-day4 compare components

## Target Files

- src/skilllogboard/dashboards/compare_builder.py
- src/skilllogboard/compare/run_index.py
- tests/test_compare_report.py

## Implementation Steps

1. Implement `build_compare_report(runs_dir, metric, mode, output_dir=None)` or equivalent.
2. Build run index, leaderboard, config diff, ablation axes, and seed summary.
3. Write `compare.csv` for leaderboard.
4. Write `compare.md` with sections: Leaderboard, Config Diff, Ablation Axes, Seed Summary.
5. Return output paths.
6. Add tests using temporary run folders.

## Acceptance Criteria

- compare.md and compare.csv are generated.
- compare.md includes all expected sections.
- compare.csv contains leaderboard rows.
- Builder returns output paths.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_compare_report.py
```

## Non-goals

- Do not polish HTML dashboard yet.

## Handoff Notes

- Keep the slice small and focused.
- Preserve the public API already working after Week 4.
- Do not implement Week 6+ research plugins unless this slice explicitly asks for a placeholder.
- Do not hide unsupported or planned features in docs; label them clearly.
- If a blocker appears, document it in the Agent Completion Block instead of expanding scope.

---

## Agent Completion Block

> The agent must update this block after finishing the slice.

- [ ] Implementation completed
- [ ] Acceptance criteria verified
- [ ] Tests or smoke checks executed
- [ ] No unrelated files changed
- [ ] Notes added below if anything was skipped or deferred

**Status:** PENDING  
**Completed at:**  
**Completed by:**  
**Verification command(s):**  
**Notes:**  

<!-- AGENT_STATUS: PENDING -->

