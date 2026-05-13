---
milestone: "v0.9-cleanup"
phase: "Template Forge Cleanup"
slice: "03_forge_cli_help_ux"
title: "Forge CLI help UX"
priority: "P0"
status: "completed"
target_version: "v0.9-cleanup"
---

# 03_forge_cli_help_ux — Forge CLI help UX

## Objective

Improve `skilllog forge` help messages and validation/error output without changing the core workflow.

## Context

v0.9 Template Forge is functionally complete and CI is green. This cleanup phase polishes docs, CLI UX, validator depth, and CI maintenance before v1.0 Live Board.

## Target Files

- src/skilllogboard/cli/main.py
- tests/test_cli_template_forge.py
- docs/template_forge.md

## Implementation Steps

1. Run `skilllog forge --help` and inspect current usability.
2. Ensure subcommands have descriptive help text.
3. Ensure init-brief, plan, scaffold, and validate show required/optional arguments clearly.
4. Improve missing-file and existing-file error messages if confusing.
5. Add tests for help output and one readable error path.
6. Update docs if CLI options changed.

## Acceptance Criteria

- `skilllog forge --help` is readable.
- Each forge subcommand has useful help text.
- Missing brief/spec/template errors are actionable.
- CLI tests pass.

## Verification Commands

```bash
pytest -q tests/test_cli_template_forge.py
skilllog forge --help || skilllog --help
```

## Non-goals

- Do not begin v1.0 Live Board implementation.
- Do not add built-in LLM inference, cloud calls, or automatic code generation.
- Do not implement new domain templates directly.
- Do not change public RunLogger APIs.
- Do not add heavy dependencies to core.

## Handoff Notes

- Keep this cleanup focused.
- Preserve v0.9 behavior and all existing tests.
- If an item is deferred, update docs and record the reason below.

---

## Agent Completion Block

- [x] Implementation completed
- [x] Acceptance criteria verified
- [x] Tests or smoke checks executed
- [x] No unrelated files changed
- [x] Notes added below if anything was skipped or deferred

**Status:** COMPLETED  
**Completed at:** 2026-05-13  
**Completed by:** Codex  
**Verification command(s):** `.venv/bin/python -m pytest -q tests/test_cli_template_forge.py`; `.venv/bin/skilllog --help`; `.venv/bin/skilllog forge --help`  
**Notes:** Forge top-level help lists commands and examples; subcommand help and missing-brief errors are covered by tests.

<!-- AGENT_STATUS: COMPLETED -->
