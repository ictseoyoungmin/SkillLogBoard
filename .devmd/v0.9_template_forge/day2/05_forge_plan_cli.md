---
milestone: "v0.9"
phase: "Template Forge"
day: "2"
slice: "05_forge_plan_cli"
title: "forge plan CLI"
priority: "P0"
status: "pending"
target_version: "v0.9-template-forge"
---

# 05_forge_plan_cli — forge plan CLI

## Objective

Add CLI support for creating a draft TemplateSpec from ResearchBrief.

## Context

The plan step should produce a reviewable intermediate spec before scaffolding code files.

## Dependencies

- 04_init_brief_cli

## Target Files

- src/skilllogboard/cli/main.py
- src/skilllogboard/template_forge/template_spec.py
- tests/test_cli_template_forge.py

## Implementation Steps

1. Add `skilllog forge plan --brief ResearchBrief.md --name custom-task`.
2. Parse ResearchBrief.
3. Generate draft TemplateSpec.md using deterministic skeleton mapping.
4. Do not overwrite existing TemplateSpec.md by default.
5. Print created/skipped and TODO count if feasible.
6. Add CLI tests.

## Acceptance Criteria

- `skilllog forge plan` appears in help.
- Command creates TemplateSpec.md.
- Generated spec includes metrics and required outputs from brief.
- No LLM call is made.
- CLI tests pass.

## Verification Commands

```bash
pytest -q tests/test_cli_template_forge.py
```

## Non-goals

- Do not generate plugin code in this slice.

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

