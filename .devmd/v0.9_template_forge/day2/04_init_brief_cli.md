---
milestone: "v0.9"
phase: "Template Forge"
day: "2"
slice: "04_init_brief_cli"
title: "init brief CLI"
priority: "P0"
status: "completed"
target_version: "v0.9-template-forge"
---

# 04_init_brief_cli — init brief CLI

## Objective

Add CLI support for creating a ResearchBrief template.

## Context

Users need a simple entry point before asking an agent to generate a research template.

## Dependencies

- 03_template_name_slug_and_paths

## Target Files

- src/skilllogboard/cli/main.py
- src/skilllogboard/template_forge/research_brief.py
- tests/test_cli_template_forge.py

## Implementation Steps

1. Add `skilllog forge init-brief` command or equivalent.
2. Default output should be `ResearchBrief.md` in the current directory unless `--output` is provided.
3. Do not overwrite existing file by default.
4. Print created/skipped status.
5. Add CLI tests.

## Acceptance Criteria

- `skilllog forge init-brief` appears in help.
- Command creates `ResearchBrief.md`.
- Existing file is not overwritten by default.
- CLI tests pass.

## Verification Commands

```bash
pytest -q tests/test_cli_template_forge.py
skilllog --help
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
