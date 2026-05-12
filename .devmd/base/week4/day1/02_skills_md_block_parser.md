---
week: 4
day: 1
slice: "02_skills_md_block_parser"
title: "Skills.md block parser"
priority: "P0"
status: "completed"
target_version: "v0.3-rule-engine"
---

# 02_skills_md_block_parser — Skills.md block parser

## Objective

Implement parser support for RULE-* Markdown blocks.

## Context

D16 requires Skills.md block parser design and implementation.

## Dependencies

- Previous slices in order

## Target Files

- src/skilllogboard/skills/parser.py
- tests/test_skills_parser.py

## Implementation Steps

1. Create `RuleSpec` dataclass or dictionary schema.
2. Implement `parse_skills_text(text)`.
3. Implement `parse_skills(path)`.
4. Extract `rule_id` from headings.
5. Parse YAML-like bullet metadata.
6. Convert `[a, b, c]` fields to lists.
7. Preserve message strings.
8. Add tests for multiple blocks.

## Acceptance Criteria

- Parser returns ordered rule specs.
- Each spec includes rule_id, type, severity, status, message, params.
- Unknown non-rule sections are ignored safely.

## Verification Commands

```bash
pytest -q tests/test_skills_parser.py
```

## Non-goals

- Do not execute rules yet.

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

