---
week: 4
day: 2
slice: "03_required_metric_rule"
title: "required_metric rule"
priority: "P0"
status: "completed"
target_version: "v0.3-rule-engine"
---

# 03_required_metric_rule — required_metric rule

## Objective

Implement the MVP `required_metric` rule.

## Context

It checks whether required metric names appear in metrics.csv/run context.

## Dependencies

- Previous slices in order

## Target Files

- src/skilllogboard/skills/rules.py
- tests/test_skills_rules.py

## Implementation Steps

1. Implement `required_metric` executor.
2. Read required metric names from `keys`.
3. Check names against available metric records.
4. Return passed/warning/error.
5. Add tests for present, missing, and empty metrics.

## Acceptance Criteria

- Passes when metrics exist.
- Reports missing metric names.
- Empty metrics are handled clearly.

## Verification Commands

```bash
pytest -q tests/test_skills_rules.py
```

## Non-goals

- Do not validate metric quality here.

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
**Verification command(s):** pytest -q tests/test_skills_rules.py  
**Notes:** Completed and verified for Week 4 v0.3 rule engine scope.

<!-- AGENT_STATUS: COMPLETED -->

