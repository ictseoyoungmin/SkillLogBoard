---
milestone: "v0.9"
phase: "Template Forge"
day: "4"
slice: "04_example_tests_docs_dependency_validation"
title: "example tests docs dependency validation"
priority: "P0"
status: "pending"
target_version: "v0.9-template-forge"
---

# 04_example_tests_docs_dependency_validation — example tests docs dependency validation

## Objective

Validate synthetic example requirements, test existence, docs existence, and dependency policy.

## Context

Template Forge's main safety policy is that generated templates must be testable, documented, and dependency-light.

## Dependencies

- 03_plugin_and_skills_validation

## Target Files

- src/skilllogboard/template_forge/validator.py
- tests/test_template_forge_validator.py

## Implementation Steps

1. Check example scaffold/file exists and does not require external data by default.
2. Check test file exists.
3. Check docs file exists.
4. Inspect pyproject core dependencies to ensure no heavy dependency was added.
5. Flag torch/lightning/sklearn/pandas/matplotlib/LLM SDKs in core dependencies as errors.
6. Add tests for dependency violation detection using fake pyproject content if feasible.

## Acceptance Criteria

- Synthetic example presence is checked.
- Tests/docs presence are checked.
- Heavy core dependency additions are detected.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_template_forge_validator.py
```

## Non-goals

- Do not implement unrelated future features.

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

