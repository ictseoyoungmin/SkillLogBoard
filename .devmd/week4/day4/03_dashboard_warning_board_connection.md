---
week: 4
day: 4
slice: "03_dashboard_warning_board_connection"
title: "dashboard warning board connection"
priority: "P0"
status: "completed"
target_version: "v0.3-rule-engine"
---

# 03_dashboard_warning_board_connection — dashboard warning board connection

## Objective

Display skill trace warnings/errors in the static dashboard.

## Context

D19 connects skill_trace to dashboard warning board.

## Dependencies

- Previous slices in order

## Target Files

- src/skilllogboard/dashboards/components.py
- src/skilllogboard/dashboards/templates/run.html.j2
- tests/test_dashboard_rule_trace.py

## Implementation Steps

1. Load skill_trace.jsonl in dashboard context.
2. Summarize counts by outcome.
3. Add Rule Audit/Warning Board section.
4. List warning/error rule_id and message.
5. Show empty state when absent.
6. Test fixture skill_trace rendering.

## Acceptance Criteria

- Dashboard includes Rule Audit/Warning Board.
- Warnings/errors visible.
- Absent skill_trace does not crash.
- Tests verify rendering.

## Verification Commands

```bash
pytest -q tests/test_dashboard_rule_trace.py
```

## Non-goals

- Do not implement interactive filtering.

## Handoff Notes

- Keep the slice small and focused.
- Preserve the public API already working after Week 3.
- Do not implement Week 5+ features unless this file explicitly asks for a placeholder.
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
**Completed at:** 2026-05-09 23:49  
**Completed by:** coding agent  
**Verification command(s):** pytest -q tests/test_dashboard_rule_trace.py  
**Notes:** Completed and verified for Week 4 v0.3 rule engine scope.

<!-- AGENT_STATUS: COMPLETED -->

