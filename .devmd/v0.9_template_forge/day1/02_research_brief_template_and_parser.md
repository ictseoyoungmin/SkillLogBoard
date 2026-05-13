---
milestone: "v0.9"
phase: "Template Forge"
day: "1"
slice: "02_research_brief_template_and_parser"
title: "research brief template and parser"
priority: "P0"
status: "completed"
target_version: "v0.9-template-forge"
---

# 02_research_brief_template_and_parser — research brief template and parser

## Objective

Provide a default `ResearchBrief.md` template and parser.

## Context

Users need a starting file that they can fill in before asking an external agent to create a template.

## Dependencies

- 01_research_brief_contract

## Target Files

- src/skilllogboard/template_forge/research_brief.py
- src/skilllogboard/template_forge/harness/research_brief_template.md
- tests/test_template_forge_brief.py

## Implementation Steps

1. Add `research_brief_template.md` under package harness files.
2. Implement `parse_research_brief_text(text)`.
3. Implement `parse_research_brief(path)`.
4. Support section-based Markdown parsing for topic, task type, data, target, metrics, axes, outputs, constraints.
5. Handle missing optional sections gracefully.
6. Add tests for parsing the default template and a filled example.

## Acceptance Criteria

- Default research brief template exists.
- Template is package-accessible.
- Parser can parse a filled ResearchBrief.md.
- Missing optional sections do not crash parser.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_template_forge_brief.py
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
