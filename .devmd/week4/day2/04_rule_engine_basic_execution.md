---
week: 4
day: 2
slice: "04_rule_engine_basic_execution"
title: "basic rule engine execution"
priority: "P0"
status: "completed"
target_version: "v0.3-rule-engine"
---

# 04_rule_engine_basic_execution — basic rule engine execution

## Objective

Implement RuleEngine that parses Skills.md and executes MVP rules against a run directory.

## Context

This connects parser and rule executors.

## Dependencies

- Previous slices in order

## Target Files

- src/skilllogboard/skills/rule_engine.py
- src/skilllogboard/skills/rules.py
- tests/test_rule_engine.py

## Implementation Steps

1. Implement `RuleEngine` constructor/from_file.
2. Implement `run(run_dir)` or `evaluate(context)`.
3. Load manifest/config/metrics/artifact index as needed.
4. Execute only MVP supported rules by default.
5. Return RuleResult objects/dicts.
6. Test with temporary run and Skills.md.

## Acceptance Criteria

- RuleEngine executes required_config and required_metric.
- RuleEngine returns structured results.
- Missing Skills.md or empty rules produce readable state.

## Verification Commands

```bash
pytest -q tests/test_rule_engine.py
```

## Non-goals

- Do not connect dashboard yet.

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
**Verification command(s):** pytest -q tests/test_rule_engine.py  
**Notes:** Completed and verified for Week 4 v0.3 rule engine scope.

<!-- AGENT_STATUS: COMPLETED -->

