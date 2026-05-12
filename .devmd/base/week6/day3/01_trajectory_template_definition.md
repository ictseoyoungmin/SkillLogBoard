---
week: 6
day: 3
slice: "01_trajectory_template_definition"
title: "trajectory template definition"
priority: "P0"
status: "completed"
target_version: "v0.5-research-templates"
---

# 01_trajectory_template_definition — trajectory template definition

## Objective

Define `trajectory` template.

## Context

Trajectory/JEPA is a key research logging use case.

## Dependencies

- Previous slices in order

## Target Files

- src/skilllogboard/plugins/trajectory.py
- src/skilllogboard/plugins/registry.py
- tests/test_trajectory_template.py

## Implementation Steps

1. Create trajectory descriptor.
2. Define metrics train/loss,val/loss,val/pb_score,val/endpoint_error.
3. Define default Skills.md rules.
4. Define config fields model, dataset, seed, encoder, horizon, lr, batch_size.
5. Register template.
6. Test descriptor.

## Acceptance Criteria

- trajectory registered.
- Default skills parse.
- PB score metric convention present.

## Verification Commands

```bash
pytest -q tests/test_trajectory_template.py tests/test_skills_parser.py
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
**Verification command(s):** .venv/bin/pytest -q tests/test_trajectory_template.py tests/test_ir_drop_template.py tests/test_skills_parser.py tests/test_plugins.py tests/test_cli_templates.py  
**Notes:** Added registered trajectory descriptor, config fields, default skills, and PB score metric convention.

<!-- AGENT_STATUS: COMPLETED -->
