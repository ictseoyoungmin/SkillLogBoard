---
milestone: "v0.9"
phase: "Template Forge"
day: "3"
slice: "03_synthetic_example_scaffold"
title: "synthetic example scaffold"
priority: "P0"
status: "pending"
target_version: "v0.9-template-forge"
---

# 03_synthetic_example_scaffold — synthetic example scaffold

## Objective

Ensure generated example scaffold demonstrates a dependency-light synthetic run.

## Context

Every generated template must include an example that runs without external data.

## Dependencies

- 02_plugin_descriptor_scaffold

## Target Files

- src/skilllogboard/template_forge/harness/example_template.py.txt
- tests/test_template_forge_scaffold.py

## Implementation Steps

1. Update example scaffold to use `RunLogger`.
2. Include TODO synthetic data generation section.
3. Include metric logging using metrics from TemplateSpec.
4. Include dashboard/report generation placeholders.
5. Avoid torch/pandas/sklearn imports by default.
6. Add tests checking scaffold includes RunLogger and synthetic TODO markers.

## Acceptance Criteria

- Example scaffold is dependency-light.
- Example scaffold logs metrics through RunLogger.
- Example scaffold includes synthetic data placeholder.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_template_forge_scaffold.py
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

