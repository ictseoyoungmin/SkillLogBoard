---
milestone: "v0.9"
phase: "Template Forge"
day: "1"
slice: "03_template_spec_contract"
title: "template spec contract"
priority: "P0"
status: "completed"
target_version: "v0.9-template-forge"
---

# 03_template_spec_contract — template spec contract

## Objective

Define the `TemplateSpec.md` contract generated from or based on ResearchBrief.

## Context

TemplateSpec is the intermediate design artifact that should be reviewed before scaffolding code files.

## Dependencies

- 02_research_brief_template_and_parser

## Target Files

- src/skilllogboard/template_forge/template_spec.py
- tests/test_template_forge_spec.py
- docs/template_forge.md

## Implementation Steps

1. Create `template_spec.py`.
2. Define `TemplateSpec` schema.
3. Fields should include: `template_name`, `category`, `description`, `default_config`, `metric_names`, `required_rules`, `recommended_tables`, `recommended_figures`, `synthetic_example_plan`, `dependency_policy`, `status`.
4. Define allowed initial statuses such as `Draft`, `Scaffolded`, `Implemented`, `Planned` if useful.
5. Add tests for minimal and complete spec records.

## Acceptance Criteria

- `TemplateSpec` or equivalent schema exists.
- Spec includes metrics, rules, tables, figures, and synthetic example plan.
- Spec is JSON/YAML serializable.
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
