---
milestone: "v0.9"
phase: "Template Forge"
day: "3"
slice: "02_plugin_descriptor_scaffold"
title: "plugin descriptor scaffold"
priority: "P0"
status: "pending"
target_version: "v0.9-template-forge"
---

# 02_plugin_descriptor_scaffold — plugin descriptor scaffold

## Objective

Ensure generated plugin scaffold follows the existing plugin/template descriptor contract.

## Context

Scaffolded templates should integrate with SkillLogBoard's template registry after the agent fills TODOs.

## Dependencies

- 01_scaffold_generation_core

## Target Files

- src/skilllogboard/template_forge/harness/plugin_template.py.txt
- src/skilllogboard/template_forge/scaffold.py
- tests/test_template_forge_scaffold.py

## Implementation Steps

1. Inspect existing `plugins/base.py` and registry conventions.
2. Update plugin scaffold template to match `SkillLogTemplate` or existing descriptor contract.
3. Include TODO sections for default_config, default_skills, metric_names, recommended_tables, recommended_figures, docs_notes.
4. Keep scaffold import-safe with placeholders.
5. Add tests checking scaffold contains required descriptor field names.

## Acceptance Criteria

- Plugin scaffold matches current plugin descriptor convention.
- Scaffold includes required TODO sections.
- Scaffold does not register as implemented automatically.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_template_forge_scaffold.py tests/test_plugins.py
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

