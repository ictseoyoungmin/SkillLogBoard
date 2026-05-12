---
milestone: "v0.9"
phase: "Template Forge"
day: "4"
slice: "05_forge_validate_cli"
title: "forge validate CLI"
priority: "P0"
status: "pending"
target_version: "v0.9-template-forge"
---

# 05_forge_validate_cli — forge validate CLI

## Objective

Add CLI support for validating a scaffolded or implemented template.

## Context

External agents should run this command before marking a generated template complete.

## Dependencies

- 04_example_tests_docs_dependency_validation

## Target Files

- src/skilllogboard/cli/main.py
- src/skilllogboard/template_forge/validator.py
- tests/test_cli_template_forge.py

## Implementation Steps

1. Add `skilllog forge validate TEMPLATE_NAME`.
2. Support `--root-dir`.
3. Support `--json` if simple.
4. Print pass/warn/error summary.
5. Return non-zero exit code on error-level validation failure.
6. Add CLI tests.

## Acceptance Criteria

- `skilllog forge validate` appears in help.
- Command validates scaffolded files.
- Command returns non-zero on error.
- CLI tests pass.

## Verification Commands

```bash
pytest -q tests/test_cli_template_forge.py tests/test_template_forge_validator.py
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

