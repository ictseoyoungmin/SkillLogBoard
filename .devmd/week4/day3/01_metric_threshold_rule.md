---
week: 4
day: 3
slice: "01_metric_threshold_rule"
title: "metric_threshold rule"
priority: "P0"
status: "completed"
target_version: "v0.3-rule-engine"
---

# 01_metric_threshold_rule — metric_threshold rule

## Objective

Implement the MVP `metric_threshold` rule.

## Context

This checks whether a metric reaches/stays within a threshold.

## Dependencies

- Previous slices in order

## Target Files

- src/skilllogboard/skills/rules.py
- tests/test_skills_rules.py

## Implementation Steps

1. Support fields: metric, threshold, mode.
2. Support `min` and `max` semantics.
3. Use latest metric value unless rule specifies otherwise.
4. Return observed value and threshold in details.
5. Test max pass/fail and min pass/fail.

## Acceptance Criteria

- Works for max and min modes.
- Missing metric produces readable result.
- Details include metric, observed value, threshold, mode.

## Verification Commands

```bash
pytest -q tests/test_skills_rules.py
```

## Non-goals

- Do not implement formulas.

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

