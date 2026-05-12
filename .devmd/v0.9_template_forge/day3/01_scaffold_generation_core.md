---
milestone: "v0.9"
phase: "Template Forge"
day: "3"
slice: "01_scaffold_generation_core"
title: "scaffold generation core"
priority: "P0"
status: "pending"
target_version: "v0.9-template-forge"
---

# 01_scaffold_generation_core — scaffold generation core

## Objective

Implement core scaffold generation from TemplateSpec.

## Context

Scaffold generation creates placeholder files for an external agent to fill.

## Dependencies

- day2 CLI planning completed.

## Target Files

- src/skilllogboard/template_forge/scaffold.py
- tests/test_template_forge_scaffold.py

## Implementation Steps

1. Implement `scaffold_template_from_spec(spec, root_dir='.', force=False)`.
2. Create plugin scaffold file under `src/skilllogboard/plugins/{module_name}.py`.
3. Create example scaffold under `examples/{module_name}_example.py`.
4. Create test scaffold under `tests/test_{module_name}_template.py`.
5. Create docs scaffold under `docs/templates/{module_name}.md`.
6. Create or copy `.skilllog/template_harness.md` and `.skilllog/template_spec.md`.
7. Do not overwrite existing files by default.
8. Return structured result listing created/skipped files.

## Acceptance Criteria

- Scaffold generator creates expected files.
- Existing files are not overwritten by default.
- Created files contain TODO markers.
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

