---
week: 3
day: 4
slice: "04_compare_command_placeholder_message"
title: "compare command placeholder message"
priority: "P1"
status: "completed"
target_version: "v0.2-dashboard"
---

# 04_compare_command_placeholder_message — compare command placeholder message

## Objective

Keep compare/export-table visible but clearly marked as planned for Week 5.

## Context

The CLI may already expose `compare` and `export-table`. Before Week 5, these commands should not silently fail or pretend to be implemented.

## Dependencies

- 03_cli_error_handling_and_exit_codes

## Target Files

- src/skilllogboard/cli/main.py
- tests/test_cli.py
- docs/status_matrix.md

## Implementation Steps

1. Implement `skilllog compare` as a planned-feature placeholder if it is exposed.
2. Implement `skilllog export-table` as a planned-feature placeholder if it is exposed.
3. Return a clear non-zero or documented placeholder exit code.
4. Mention that implementation is targeted for Week 5/v0.4.
5. Update docs/status_matrix.md if necessary.
6. Add tests for placeholder messaging.

## Acceptance Criteria

- `skilllog compare --help` or `skilllog compare` does not crash.
- Output clearly says the feature is planned for Week 5/v0.4.
- Docs do not mark compare as implemented in v0.2.

## Verification Commands

```bash
pytest -q tests/test_cli.py
skilllog compare || true
skilllog export-table || true
```

## Non-goals

- Do not implement multi-run compare logic.

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
**Verification command(s):** pytest -q tests/test_cli.py; skilllog compare || true; skilllog export-table || true  
**Notes:** Completed with clear Week 5/v0.4 placeholder messaging.  

<!-- AGENT_STATUS: COMPLETED -->
