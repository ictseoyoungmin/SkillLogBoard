---
milestone: "v0.9"
phase: "Template Forge"
day: "2"
slice: "02_scaffold_file_templates"
title: "scaffold file templates"
priority: "P0"
status: "completed"
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

- [x] Implementation completed
- [x] Acceptance criteria verified
- [x] Tests or smoke checks executed
- [x] No unrelated files changed
- [x] Notes added below if anything was skipped or deferred

**Status:** COMPLETED  
**Completed at:** 2026-05-13  
**Completed by:** Codex  
**Verification command(s):** ruff check; Template Forge tests; full pytest; examples; build no-isolation; forge CLI e2e smoke check  
**Notes:** v0.9 Template Forge implemented as a local scaffold/harness/validation layer. No built-in LLM, cloud API, automatic domain-code generation, or heavy core dependency was added.  

<!-- AGENT_STATUS: COMPLETED -->
