---
milestone: "v0.9"
phase: "Template Forge"
day: "1"
slice: "04_template_spec_template_and_parser"
title: "template spec template and parser"
priority: "P0"
status: "completed"
target_version: "v0.9-template-forge"
---

# 04_template_spec_template_and_parser — template spec template and parser

## Objective

Provide a default `TemplateSpec.md` template and parser.

## Context

External agents should fill a predictable TemplateSpec before generating plugin/template files.

## Dependencies

- 03_template_spec_contract

## Target Files

- src/skilllogboard/template_forge/template_spec.py
- src/skilllogboard/template_forge/harness/template_spec_template.md
- tests/test_template_forge_spec.py

## Implementation Steps

1. Add `template_spec_template.md` under harness files.
2. Implement `parse_template_spec_text(text)`.
3. Implement `parse_template_spec(path)`.
4. Support Markdown/YAML-like blocks for default config, metrics, rules, tables, figures, synthetic example plan.
5. Add tests for parsing generated spec examples.

## Acceptance Criteria

- Default template spec template exists.
- Parser handles a filled TemplateSpec.md.
- List and dict-style sections parse into structured data.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_template_forge_spec.py
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
