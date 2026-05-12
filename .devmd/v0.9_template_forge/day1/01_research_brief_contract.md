---
milestone: "v0.9"
phase: "Template Forge"
day: "1"
slice: "01_research_brief_contract"
title: "research brief contract"
priority: "P0"
status: "pending"
target_version: "v0.9-template-forge"
---

# 01_research_brief_contract — research brief contract

## Objective

Define the `ResearchBrief.md` contract for describing a user's research topic, data, metrics, experiment axes, and required outputs.

## Context

Template Forge starts from a user-authored research description. The format must be simple, local, Markdown-based, and readable by humans and agents.

## Dependencies

- v0.8 Agent Research Layer completed or available.

## Target Files

- src/skilllogboard/template_forge/__init__.py
- src/skilllogboard/template_forge/research_brief.py
- tests/test_template_forge_brief.py
- docs/template_forge.md

## Implementation Steps

1. Create `src/skilllogboard/template_forge/` package if missing.
2. Define a `ResearchBrief` dataclass or JSON-serializable dict schema.
3. Fields should include: `research_topic`, `task_type`, `input_data`, `target`, `main_metric`, `secondary_metrics`, `experiment_axes`, `required_outputs`, `constraints`.
4. Use Python 3.9-compatible typing.
5. Document the Markdown block sections expected in `ResearchBrief.md`.
6. Add tests for minimal and complete research brief records.

## Acceptance Criteria

- `ResearchBrief` or equivalent schema exists.
- Schema is JSON-serializable.
- Contract is documented.
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

