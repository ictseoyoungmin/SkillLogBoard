---
week: 4-cleanup
day: cleanup
slice: "05_rule_executor_missing_field_hardening"
title: "rule executor missing-field hardening"
priority: "P0"
status: "pending"
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

