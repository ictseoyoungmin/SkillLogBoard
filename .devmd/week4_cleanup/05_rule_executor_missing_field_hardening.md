---
week: 4-cleanup
day: cleanup
slice: "05_rule_executor_missing_field_hardening"
title: "rule executor missing-field hardening"
priority: "P0"
status: "completed"
target_version: "v0.3-cleanup"
---

# 05_rule_executor_missing_field_hardening — rule executor missing-field hardening

## Objective

Harden MVP rule executors so missing required fields produce RuleResult errors/warnings instead of uncaught Python exceptions.

## Context

Week 4 implemented rule executors. Before Week 5, rule execution should be robust against malformed or incomplete Skills.md blocks.

## Dependencies

- Week 4 completed

## Target Files

- src/skilllogboard/skills/rules.py
- tests/test_skills_rules.py
- tests/test_rule_engine.py

## Implementation Steps

1. Audit required_config, required_metric, metric_threshold, best_last_gap, artifact_required for missing required fields.
2. Normalize severity with `.lower()` or equivalent before comparing to `error`.
3. If required fields are missing, return a readable RuleResult with outcome warning/error based on severity.
4. Ensure invalid threshold values produce readable RuleResult instead of uncaught exception.
5. Add tests for missing `keys`, missing `metric`, missing `threshold`, invalid threshold, and uppercase severity such as `ERROR`.
6. Ensure planned/unknown rules still behave as designed.

## Acceptance Criteria

- Malformed MVP rule specs do not crash RuleEngine.
- Missing required fields produce structured RuleResult.
- Uppercase/mixed-case severity is handled consistently.
- All rule tests pass.

## Verification Commands

```bash
pytest -q tests/test_skills_rules.py tests/test_rule_engine.py
```

## Non-goals

- Do not add a schema validation dependency.

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
**Verification command(s):** pytest -q tests/test_skills_rules.py tests/test_rule_engine.py  
**Notes:** Completed and verified for the requested scope.

<!-- AGENT_STATUS: COMPLETED -->

