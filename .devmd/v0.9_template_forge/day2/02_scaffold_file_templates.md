---
milestone: "v0.9"
phase: "Template Forge"
day: "2"
slice: "02_scaffold_file_templates"
title: "scaffold file templates"
priority: "P0"
status: "pending"
target_version: "v0.9-template-forge"
---

# 02_scaffold_file_templates — scaffold file templates

## Objective

Add placeholder templates for plugin, example, tests, and docs scaffolds.

## Context

Template Forge should create structured files that an external agent fills, not final code.

## Dependencies

- 01_template_harness_documents

## Target Files

- src/skilllogboard/template_forge/harness/plugin_template.py.txt
- src/skilllogboard/template_forge/harness/example_template.py.txt
- src/skilllogboard/template_forge/harness/test_template.py.txt
- src/skilllogboard/template_forge/harness/docs_template.md
- tests/test_template_forge_harness.py

## Implementation Steps

1. Create plugin scaffold template with TODO markers.
2. Create synthetic example scaffold template with TODO markers.
3. Create test scaffold template with TODO markers.
4. Create docs scaffold template.
5. Use simple placeholder formatting compatible with `str.format` or custom safe replacement.
6. Add tests that all scaffold templates are package-accessible.

## Acceptance Criteria

- Plugin/example/test/docs scaffold templates exist.
- Templates include TODO markers.
- Templates do not include heavy dependency imports by default.
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

