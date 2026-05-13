---
milestone: "v0.9"
phase: "Template Forge"
day: "1"
slice: "05_brief_to_spec_skeleton"
title: "brief to spec skeleton"
priority: "P0"
status: "completed"
target_version: "v0.9-template-forge"
---

# 05_brief_to_spec_skeleton — brief to spec skeleton

## Objective

Implement a deterministic helper that creates a draft TemplateSpec skeleton from a ResearchBrief.

## Context

SkillLogBoard should not use an LLM, but it can map a brief into a structured draft spec with placeholders.

## Dependencies

- 04_template_spec_template_and_parser

## Target Files

- src/skilllogboard/template_forge/template_spec.py
- src/skilllogboard/template_forge/research_brief.py
- tests/test_template_forge_spec.py

## Implementation Steps

1. Implement `draft_template_spec_from_brief(brief, template_name=None)`.
2. Infer template name from task/topic if not provided, using safe slugification.
3. Copy main metric, secondary metrics, required outputs, and axes from brief.
4. Fill unsupported or ambiguous fields with TODO placeholders.
5. Do not invent domain-specific model code.
6. Add tests using IR-drop-like and trajectory-like brief examples.

## Acceptance Criteria

- Draft spec can be generated from a brief.
- Generated spec preserves metrics and required outputs.
- Ambiguous parts are marked TODO instead of fabricated.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_template_forge_brief.py tests/test_template_forge_spec.py
```

## Non-goals

- Do not use LLMs.
- Do not generate final research code.

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
