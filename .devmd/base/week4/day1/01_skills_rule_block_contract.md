---
week: 4
day: 1
slice: "01_skills_rule_block_contract"
title: "Skills.md rule block contract"
priority: "P0"
status: "completed"
target_version: "v0.3-rule-engine"
---

# 01_skills_rule_block_contract — Skills.md rule block contract

## Objective

Define the MVP Skills.md rule block contract before implementing the parser.

## Context

The parser must support a limited YAML-like Markdown block format and avoid open-ended DSL complexity.

## Dependencies

- Previous slices in order

## Target Files

- docs/skills.md
- src/skilllogboard/skills/parser.py
- tests/test_skills_parser.py

## Implementation Steps

1. Document headings like `## RULE-CONFIG-001` as rule delimiters.
2. Support metadata lines such as `- type: required_config`.
3. Support list syntax such as `- keys: [model_name, dataset_name, seed]`.
4. Support fields: type, keys, metric, threshold, mode, severity, status, message.
5. Define status labels: MVP, Planned, Experimental.
6. Add parser contract tests.

## Acceptance Criteria

- Supported Skills.md syntax is explicit.
- Unsupported arbitrary content is ignored or rejected safely.
- At least one complete RULE block test exists.
- No arbitrary Python execution is possible.

## Verification Commands

```bash
pytest -q tests/test_skills_parser.py
```

## Non-goals

- Do not implement all rule types here.

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
**Verification command(s):** pytest -q tests/test_skills_parser.py  
**Notes:** Completed and verified for Week 4 v0.3 rule engine scope.

<!-- AGENT_STATUS: COMPLETED -->

