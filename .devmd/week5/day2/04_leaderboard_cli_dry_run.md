---
week: 5
day: 2
slice: "04_leaderboard_cli_dry_run"
title: "leaderboard CLI dry run"
priority: "P1"
status: "pending"
target_version: "v0.4-compare"
---

# 04_leaderboard_cli_dry_run — leaderboard CLI dry run

## Objective

Add a minimal CLI path to inspect leaderboard output without full compare dashboard.

## Context

Before final compare CLI, a dry-run table helps validate ranking from terminal.

## Dependencies

- 03_leaderboard_csv_markdown_export

## Target Files

- src/skilllogboard/cli/main.py
- src/skilllogboard/compare/leaderboard.py
- tests/test_cli_compare.py

## Implementation Steps

1. Update `skilllog compare RUNS_DIR --metric METRIC --mode max|min` to build run index and leaderboard.
2. Print a small text/Markdown table to stdout.
3. Keep compare.html generation for later slices.
4. Add tests for CLI compare using temporary run folders.

## Acceptance Criteria

- `skilllog compare <runs_dir> --metric val/acc --mode max` exits 0.
- Output contains run ids and metric values.
- Missing metrics produce a readable message.
- Week 5 placeholder text is replaced for this basic path.

## Verification Commands

```bash
pytest -q tests/test_cli_compare.py
```

## Non-goals

- Do not implement config diff in this slice.

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

