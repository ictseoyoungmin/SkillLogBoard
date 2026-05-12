---
week: 6
day: 4
slice: "04_example_smoke_test_suite"
title: "example smoke test suite"
priority: "P0"
status: "completed"
target_version: "v0.5-research-templates"
---

# 04_example_smoke_test_suite — example smoke test suite

## Objective

Add smoke tests for lightweight examples.

## Context

Examples should not rot.

## Dependencies

- Previous slices in order

## Target Files

- tests/test_examples.py
- examples/basic_usage.py
- examples/ir_drop_example.py
- examples/trajectory_example.py

## Implementation Steps

1. Test basic_usage, ir_drop_example, trajectory_example.
2. Use temp output directories where practical.
3. Assert dashboard/report/skill_trace.
4. No internet or heavy deps.

## Acceptance Criteria

- Example smoke tests pass.
- No external data required.

## Verification Commands

```bash
pytest -q tests/test_examples.py
```

## Non-goals

- Do not implement unrelated future features.

## Handoff Notes

- Keep the slice small and focused.
- Preserve the public API already working after Week 5.
- Keep optional integrations optional; core install must not require heavy ML packages.
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
**Completed at:** 2026-05-10 19:51  
**Completed by:** coding agent  
**Verification command(s):** .venv/bin/pytest -q tests/test_optional_integrations.py tests/test_examples.py; .venv/bin/python examples/basic_usage.py; .venv/bin/python examples/sklearn_example.py  
**Notes:** Added lightweight example smoke tests for basic usage, IR-drop, trajectory, and sklearn-style logging.

<!-- AGENT_STATUS: COMPLETED -->
