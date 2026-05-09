---
week: 4
day: 2
slice: "02_required_config_rule"
title: "required_config rule"
priority: "P0"
status: "completed"
target_version: "v0.3-rule-engine"
---

# 02_required_config_rule — required_config rule

## Objective

Implement the MVP `required_config` rule.

## Context

It checks whether required config keys exist in config.yaml/run context.

## Dependencies

- Previous slices in order

## Target Files

- src/skilllogboard/skills/rules.py
- tests/test_skills_rules.py

## Implementation Steps

1. Implement `required_config` executor.
2. Read required keys from rule spec `keys`.
3. Check against loaded config dict.
4. Return passed if all exist.
5. Return warning/error if missing based on severity.
6. Include missing keys in result details.

## Acceptance Criteria

- Passes when all keys exist.
- Reports missing keys.
- Severity affects outcome consistently.
- Details include missing keys.

## Verification Commands

```bash
pytest -q tests/test_skills_rules.py
```

## Non-goals

- Do not validate config value types.

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

