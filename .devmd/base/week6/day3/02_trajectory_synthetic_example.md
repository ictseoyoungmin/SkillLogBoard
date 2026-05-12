---
week: 6
day: 3
slice: "02_trajectory_synthetic_example"
title: "trajectory synthetic example"
priority: "P0"
status: "completed"
target_version: "v0.5-research-templates"
---

# 02_trajectory_synthetic_example — trajectory synthetic example

## Objective

Add lightweight trajectory example.

## Context

Example should track trajectory experiments without model training.

## Dependencies

- Previous slices in order

## Target Files

- examples/trajectory_example.py
- tests/test_trajectory_template.py
- README.md

## Implementation Steps

1. Create/update example.
2. Log trajectory metrics over steps.
3. Log small table/artifact.
4. Run skill checks.
5. Finish dashboard/report.
6. Print run dir.

## Acceptance Criteria

- Example runs without external data.
- Generated run has metrics, dashboard, summary, skill_trace.

## Verification Commands

```bash
python examples/trajectory_example.py
pytest -q tests/test_trajectory_template.py
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
**Completed at:** 2026-05-10 19:49  
**Completed by:** coding agent  
**Verification command(s):** .venv/bin/python examples/trajectory_example.py; .venv/bin/pytest -q tests/test_trajectory_template.py tests/test_ir_drop_template.py tests/test_skills_parser.py tests/test_plugins.py tests/test_cli_templates.py  
**Notes:** Added synthetic trajectory example that logs metrics, table/artifact, skill trace, summary, and dashboard without external data.

<!-- AGENT_STATUS: COMPLETED -->
