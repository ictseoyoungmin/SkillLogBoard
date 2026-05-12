---
milestone: "v0.9"
phase: "Template Forge"
day: "5"
slice: "04_backward_compatibility_regression"
title: "backward compatibility regression"
priority: "P0"
status: "pending"
target_version: "v0.9-template-forge"
---

# 04_backward_compatibility_regression — backward compatibility regression

## Objective

Ensure v0.9 did not break existing v0.8/v0.7/v0.6 functionality.

## Context

Template Forge must be additive and must not affect logging/report/dashboard/compare/template/agent behavior.

## Dependencies

- 03_template_forge_cli_regression

## Target Files

- tests/
- examples/
- .devmd/v0.9_template_forge/day5/04_backward_compatibility_regression.md

## Implementation Steps

1. Run full test suite.
2. Run basic example.
3. Run IR-drop and trajectory examples.
4. Run report artifact tests if v0.7 exists.
5. Run agent tests if v0.8 exists.
6. Run compare/dashboard tests.
7. Fix only regressions caused by v0.9 changes.
8. Record results in the completion block.

## Acceptance Criteria

- `pytest -q` passes.
- `python examples/basic_usage.py` passes.
- `python examples/ir_drop_example.py` passes.
- `python examples/trajectory_example.py` passes.
- Existing report/agent/dashboard/compare behavior remains intact.

## Verification Commands

```bash
pytest -q
python examples/basic_usage.py
python examples/ir_drop_example.py
python examples/trajectory_example.py
```

## Non-goals

- Do not add new features in this regression slice.

## Handoff Notes

- Keep this slice focused and small.
- Preserve existing v0.8/v0.7/v0.6 public APIs and run folder compatibility.
- Template Forge is a scaffold/harness/validation system. It must not embed LLM inference or call cloud APIs.
- Generated template code must be local, inspectable, dependency-light, and testable with synthetic examples.
- Core install must remain lightweight. Do not add torch, lightning, sklearn, pandas, matplotlib, LLM SDKs, or domain packages to core dependencies.
- If a blocker appears, document it in the Agent Completion Block instead of expanding scope.

---

## Agent Completion Block

> The agent must update this block after finishing the slice.

- [ ] Implementation completed
- [ ] Acceptance criteria verified
- [ ] Tests or smoke checks executed
- [ ] No unrelated files changed
- [ ] Notes added below if anything was skipped or deferred

**Status:** PENDING  
**Completed at:**  
**Completed by:**  
**Verification command(s):**  
**Notes:**  

<!-- AGENT_STATUS: PENDING -->

