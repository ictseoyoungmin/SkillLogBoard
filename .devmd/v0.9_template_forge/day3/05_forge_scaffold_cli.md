---
milestone: "v0.9"
phase: "Template Forge"
day: "3"
slice: "05_forge_scaffold_cli"
title: "forge scaffold CLI"
priority: "P0"
status: "pending"
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

