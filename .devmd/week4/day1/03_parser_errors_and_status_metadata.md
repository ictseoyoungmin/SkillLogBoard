---
week: 4
day: 1
slice: "03_parser_errors_and_status_metadata"
title: "parser errors and status metadata"
priority: "P0"
status: "completed"
target_version: "v0.3-rule-engine"
---

# 03_parser_errors_and_status_metadata — parser errors and status metadata

## Objective

Make parser failures readable and preserve MVP/Planned/Experimental metadata.

## Context

Docs/Implementation sync requires planned rule types not to be treated as implemented.

## Dependencies

- Previous slices in order

## Target Files

- src/skilllogboard/skills/parser.py
- tests/test_skills_parser.py

## Implementation Steps

1. Define `SkillsParseError` or structured parse errors.
2. Validate each RULE block has at least `type`.
3. Default severity to `warning` if missing.
4. Preserve Planned/Experimental status values.
5. Add malformed block tests.

## Acceptance Criteria

- Malformed blocks produce readable errors/warnings.
- Status metadata is preserved.
- Planned rules are parseable but not executable by default.

## Verification Commands

```bash
pytest -q tests/test_skills_parser.py
```

## Non-goals

- Do not add a complex validation library.

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

