---
milestone: "v0.9"
phase: "Template Forge"
day: "5"
slice: "03_template_forge_cli_regression"
title: "template forge CLI regression"
priority: "P0"
status: "pending"
target_version: "v0.9-template-forge"
---

# 03_template_forge_cli_regression — template forge CLI regression

## Objective

Run and harden CLI tests for all v0.9 forge commands.

## Context

Forge commands are the main user interface for v0.9.

## Dependencies

- 02_status_matrix_and_changelog_v09

## Target Files

- tests/test_cli_template_forge.py
- src/skilllogboard/cli/main.py

## Implementation Steps

1. Run CLI template forge tests.
2. Ensure `skilllog forge init-brief` works.
3. Ensure `skilllog forge plan` works.
4. Ensure `skilllog forge scaffold` works.
5. Ensure `skilllog forge validate` works.
6. Fix only CLI regressions or missing error handling.

## Acceptance Criteria

- All CLI template forge tests pass.
- Forge commands appear in help.
- Commands produce readable outputs.
- Error cases are handled clearly.

## Verification Commands

```bash
pytest -q tests/test_cli_template_forge.py
skilllog --help
```

## Non-goals

- Do not add new forge commands beyond v0.9 scope.

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

