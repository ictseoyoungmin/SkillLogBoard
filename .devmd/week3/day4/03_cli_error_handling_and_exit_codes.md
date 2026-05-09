---
week: 3
day: 4
slice: "03_cli_error_handling_and_exit_codes"
title: "CLI error handling and exit codes"
priority: "P0"
status: "completed"
target_version: "v0.2-dashboard"
---

# 03_cli_error_handling_and_exit_codes — CLI error handling and exit codes

## Objective

Standardize CLI errors and exit codes for missing or invalid run directories.

## Context

A tool used by agents must fail clearly. Bad paths should not produce stack traces for normal user mistakes.

## Dependencies

- 01_cli_dashboard_report_inspect_refinement

## Target Files

- src/skilllogboard/cli/main.py
- tests/test_cli_errors.py

## Implementation Steps

1. Add helper validation for run directory existence.
2. Return non-zero exit code for missing run directory.
3. Return non-zero exit code for missing required manifest where applicable.
4. Print clear error messages to stderr or stdout consistently.
5. Add tests for missing path and invalid run directory.

## Acceptance Criteria

- CLI missing-path tests pass.
- Error messages mention the invalid path.
- Exit codes are non-zero for invalid input.
- Valid commands still return zero.

## Verification Commands

```bash
pytest -q tests/test_cli_errors.py
```

## Non-goals

- Do not implement rich terminal UI.

## Handoff Notes

- Keep the slice small and focused.
- Preserve the public API already working after Week 2.
- Do not implement Week 4+ features unless this file explicitly asks for a placeholder.
- Prefer deterministic, file-based output over complex runtime behavior.
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
**Completed at:** 2026-05-09 22:53  
**Completed by:** coding agent  
**Verification command(s):** pytest -q tests/test_cli_errors.py  
**Notes:** Completed for Week 3 v0.2 dashboard scope.  

<!-- AGENT_STATUS: COMPLETED -->
