---
milestone: "v0.9"
phase: "Template Forge"
day: "4"
slice: "01_template_validator_contract"
title: "template validator contract"
priority: "P0"
status: "pending"
target_version: "v0.9-template-forge"
---

# 01_template_validator_contract — template validator contract

## Objective

Define validation result schema and validation categories for scaffolded templates.

## Context

Validation is the gate that prevents agent-generated templates from being marked complete prematurely.

## Dependencies

- day3 scaffold CLI completed.

## Target Files

- src/skilllogboard/template_forge/validator.py
- tests/test_template_forge_validator.py

## Implementation Steps

1. Create `validator.py`.
2. Define `TemplateValidationResult` schema.
3. Fields: `check_id`, `name`, `outcome`, `severity`, `message`, `details`.
4. Define validation categories: files, plugin, skills, example, tests, docs, dependencies, status.
5. Add serialization helper.
6. Add tests for result construction.

## Acceptance Criteria

- Validation result schema exists.
- Outcomes are consistent: passed/warning/error/skipped.
- Result is JSON-serializable.
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

