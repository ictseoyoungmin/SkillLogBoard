---
milestone: "v0.9"
phase: "Template Forge"
day: "3"
slice: "05_forge_scaffold_cli"
title: "forge scaffold CLI"
priority: "P0"
status: "completed"
target_version: "v0.9-template-forge"
---

# 05_forge_scaffold_cli — forge scaffold CLI

## Objective

Add CLI support for generating a full template scaffold.

## Context

This is the main user-facing command that creates files for an external coding agent to fill.

## Dependencies

- 04_test_and_docs_scaffold

## Target Files

- src/skilllogboard/cli/main.py
- src/skilllogboard/template_forge/scaffold.py
- tests/test_cli_template_forge.py

## Implementation Steps

1. Add `skilllog forge scaffold --spec TemplateSpec.md`.
2. Support `--name` and `--brief` convenience path if feasible.
3. Support `--root-dir`.
4. Do not overwrite files by default.
5. Print created/skipped files.
6. Add CLI tests with a temp directory.

## Acceptance Criteria

- `skilllog forge scaffold` appears in help.
- Command creates plugin/example/test/docs scaffold files.
- Existing files are protected.
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
