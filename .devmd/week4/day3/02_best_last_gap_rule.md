---
week: 4
day: 3
slice: "02_best_last_gap_rule"
title: "best_last_gap rule"
priority: "P0"
status: "completed"
target_version: "v0.3-rule-engine"
---

# 02_best_last_gap_rule — best_last_gap rule

## Objective

Implement the MVP `best_last_gap` rule.

## Context

Warn about possible overfitting or instability when best and last values diverge.

## Dependencies

- Previous slices in order

## Target Files

- src/skilllogboard/skills/rules.py
- tests/test_skills_rules.py

## Implementation Steps

1. Support fields: metric, threshold, mode.
2. Compute best and last values from metric series.
3. For max: gap = best - last. For min: gap = last - best.
4. Warn/error when gap exceeds threshold.
5. Test no gap, large gap, min mode, missing metric.

## Acceptance Criteria

- Computes best/last correctly.
- Passes when gap within threshold.
- Warns/errors when gap exceeds threshold.
- Missing/single-value metric handled clearly.

## Verification Commands

```bash
pytest -q tests/test_skills_rules.py
```

## Non-goals

- Do not implement significance tests.

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

