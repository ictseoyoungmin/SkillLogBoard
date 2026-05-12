---
milestone: "v0.9"
phase: "Template Forge"
day: "2"
slice: "01_template_harness_documents"
title: "template harness documents"
priority: "P0"
status: "pending"
target_version: "v0.9-template-forge"
---

# 01_template_harness_documents — template harness documents

## Objective

Add package-accessible harness documents that instruct external agents how to create SkillLogBoard-compatible templates.

## Context

The harness is the core safety rail for external coding agents.

## Dependencies

- day1 brief/spec completed.

## Target Files

- src/skilllogboard/template_forge/harness/template_harness.md
- src/skilllogboard/template_forge/harness/agent_template_creation_guide.md
- tests/test_template_forge_harness.py

## Implementation Steps

1. Create `template_harness.md` with required files, constraints, validation gates, and non-goals.
2. Create `agent_template_creation_guide.md` with step-by-step agent workflow.
3. Explicitly state: no core heavy dependencies, no external data requirement, synthetic example required, tests required, docs required.
4. Mention that implemented status is allowed only after validation passes.
5. Add tests that harness files are package-accessible.

## Acceptance Criteria

- Harness Markdown files exist.
- Harness files are package-accessible.
- Harness states no built-in LLM/codegen/cloud.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_template_forge_harness.py
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

