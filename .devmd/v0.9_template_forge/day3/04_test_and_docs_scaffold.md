---
milestone: "v0.9"
phase: "Template Forge"
day: "3"
slice: "04_test_and_docs_scaffold"
title: "test and docs scaffold"
priority: "P0"
status: "completed"
target_version: "v0.9-template-forge"
---

# 04_test_and_docs_scaffold — test and docs scaffold

## Objective

Ensure generated tests and docs scaffolds enforce validation and documentation standards.

## Context

Agent-generated templates should not be considered complete unless tests and docs exist.

## Dependencies

- 03_synthetic_example_scaffold

## Target Files

- src/skilllogboard/template_forge/harness/test_template.py.txt
- src/skilllogboard/template_forge/harness/docs_template.md
- tests/test_template_forge_scaffold.py

## Implementation Steps

1. Update test scaffold with checks for registration, default skills parseability, synthetic example existence, and docs existence.
2. Update docs scaffold with sections: overview, metrics, config, rules, tables, figures, example usage, limitations.
3. Ensure generated docs mark template status as Draft/Scaffolded until validation passes.
4. Add tests checking scaffold content.

## Acceptance Criteria

- Test scaffold contains required test placeholders.
- Docs scaffold contains required sections.
- Status is not marked Implemented by default.
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
