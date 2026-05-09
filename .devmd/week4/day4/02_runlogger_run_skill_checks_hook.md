---
week: 4
day: 4
slice: "02_runlogger_run_skill_checks_hook"
title: "RunLogger run_skill_checks hook"
priority: "P0"
status: "completed"
target_version: "v0.3-rule-engine"
---

# 02_runlogger_run_skill_checks_hook — RunLogger run_skill_checks hook

## Objective

Expose rule execution through RunLogger with a simple API.

## Context

Docs mention `logger.run_skill_checks(stage)`; Week 4 should provide this hook.

## Dependencies

- Previous slices in order

## Target Files

- src/skilllogboard/core/logger.py
- src/skilllogboard/skills/rule_engine.py
- tests/test_rule_engine.py

## Implementation Steps

1. Add `RunLogger.run_skill_checks(skills_path='Skills.md', stage=None)`.
2. Run RuleEngine against current run directory.
3. Write skill_trace.jsonl.
4. Update manifest.files with skill_trace.
5. Return list of results.
6. Test with temporary Skills.md.

## Acceptance Criteria

- run_skill_checks returns results.
- skill_trace.jsonl is written.
- Manifest includes skill_trace path.
- Missing Skills.md is safe/readable.

## Verification Commands

```bash
pytest -q tests/test_rule_engine.py tests/test_logger_lifecycle.py
```

## Non-goals

- Do not run checks on every metric log.

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
**Verification command(s):** pytest -q tests/test_rule_engine.py tests/test_logger_lifecycle.py  
**Notes:** Completed and verified for Week 4 v0.3 rule engine scope.

<!-- AGENT_STATUS: COMPLETED -->

