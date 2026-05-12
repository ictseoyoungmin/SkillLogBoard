---
week: 4
day: 3
slice: "03_artifact_required_rule"
title: "artifact_required rule"
priority: "P0"
status: "completed"
target_version: "v0.3-rule-engine"
---

# 03_artifact_required_rule — artifact_required rule

## Objective

Implement the MVP `artifact_required` rule.

## Context

Verify required artifacts were recorded in artifact_index.json.

## Dependencies

- Previous slices in order

## Target Files

- src/skilllogboard/skills/rules.py
- tests/test_skills_rules.py

## Implementation Steps

1. Support fields: keys or artifacts.
2. Check names against artifact_index.json records.
3. Optionally match by artifact type if already present.
4. Return missing artifact names in details.
5. Test pass, missing artifact, missing index.

## Acceptance Criteria

- Passes when artifacts exist.
- Missing index produces readable warning/error.
- Missing artifacts listed in details.

## Verification Commands

```bash
pytest -q tests/test_skills_rules.py
```

## Non-goals

- Do not inspect artifact contents.

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

