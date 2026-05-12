---
milestone: "v0.9"
phase: "Template Forge"
day: "4"
slice: "02_file_presence_validation"
title: "file presence validation"
priority: "P0"
status: "pending"
target_version: "v0.9-template-forge"
---

# 02_file_presence_validation — file presence validation

## Objective

Validate that scaffolded template files exist.

## Context

The first validation layer checks that the expected files were created and not deleted.

## Dependencies

- 01_template_validator_contract

## Target Files

- src/skilllogboard/template_forge/validator.py
- tests/test_template_forge_validator.py

## Implementation Steps

1. Implement `validate_template_files(template_name, root_dir='.')`.
2. Check plugin file exists.
3. Check example file exists.
4. Check test file exists.
5. Check docs file exists.
6. Check `.skilllog/template_spec.md` and `.skilllog/template_harness.md` exist if expected.
7. Add tests for pass and missing-file cases.

## Acceptance Criteria

- Missing plugin/example/test/docs are detected.
- Existing scaffold passes file presence checks.
- Results are structured.
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

