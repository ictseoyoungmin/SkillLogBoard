---
week: 4
day: 1
slice: "04_parser_default_skills_alignment"
title: "parser and default skills alignment"
priority: "P1"
status: "completed"
target_version: "v0.3-rule-engine"
---

# 04_parser_default_skills_alignment — parser and default skills alignment

## Objective

Ensure package default_skills.md parses and separates MVP/Planned rules.

## Context

The default skills file is documentation and a test fixture.

## Dependencies

- Previous slices in order

## Target Files

- src/skilllogboard/skills/default_skills.md
- tests/test_skills_parser.py
- docs/skills.md

## Implementation Steps

1. Update default_skills.md to supported syntax.
2. Include MVP examples for required_config and required_metric.
3. Optionally include Planned dashboard_panel/domain_breakdown examples marked Planned.
4. Add a test parsing package default_skills.md.

## Acceptance Criteria

- default_skills.md parses successfully.
- MVP and Planned rules are clearly separated.
- No unsupported syntax remains.

## Verification Commands

```bash
pytest -q tests/test_skills_parser.py
```

## Non-goals

- Do not execute Planned rules.

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

