---
week: 4
day: 2
slice: "01_rule_result_and_registry_schema"
title: "rule result and registry schema"
priority: "P0"
status: "completed"
target_version: "v0.3-rule-engine"
---

# 01_rule_result_and_registry_schema — rule result and registry schema

## Objective

Create the rule execution result schema and built-in rule registry.

## Context

Rules should return structured results for skill_trace.jsonl and dashboard warning board.

## Dependencies

- Previous slices in order

## Target Files

- src/skilllogboard/skills/rules.py
- src/skilllogboard/skills/rule_engine.py
- tests/test_skills_rules.py

## Implementation Steps

1. Define `RuleResult` dataclass or JSON-serializable dict.
2. Include rule_id, rule_type, severity, status, outcome, message, details, timestamp.
3. Define outcomes: passed, warning, error, skipped, planned.
4. Create built-in registry mapping rule type to executor.
5. Ensure Planned rules return planned/skipped.

## Acceptance Criteria

- Rule results are JSON-serializable.
- Registry finds MVP rule executors.
- Unknown types produce readable skipped/error results.
- Planned status is explicit.

## Verification Commands

```bash
pytest -q tests/test_skills_rules.py
```

## Non-goals

- Do not write skill_trace.jsonl yet.

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

