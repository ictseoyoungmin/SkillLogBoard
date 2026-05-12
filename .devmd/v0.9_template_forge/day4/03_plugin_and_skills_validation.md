---
milestone: "v0.9"
phase: "Template Forge"
day: "4"
slice: "03_plugin_and_skills_validation"
title: "plugin and skills validation"
priority: "P0"
status: "pending"
target_version: "v0.9-template-forge"
---

# 03_plugin_and_skills_validation — plugin and skills validation

## Objective

Validate plugin descriptor compatibility and default skills parseability where possible.

## Context

Generated templates should follow SkillLogBoard plugin conventions and rule syntax.

## Dependencies

- 02_file_presence_validation

## Target Files

- src/skilllogboard/template_forge/validator.py
- tests/test_template_forge_validator.py
- tests/test_plugins.py

## Implementation Steps

1. Validate that plugin scaffold contains or exposes expected descriptor fields.
2. If the template is registered, validate registry lookup.
3. If default skills content exists, parse it using existing skills parser.
4. Do not require scaffolded Draft templates to be fully importable if TODOs remain; report scaffold/draft status clearly.
5. Add tests for draft scaffold and filled minimal fake template if feasible.

## Acceptance Criteria

- Plugin descriptor checks run.
- Default skills parse checks run when available.
- Draft templates with TODOs produce warnings, not false implemented status.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_template_forge_validator.py tests/test_plugins.py tests/test_skills_parser.py
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

