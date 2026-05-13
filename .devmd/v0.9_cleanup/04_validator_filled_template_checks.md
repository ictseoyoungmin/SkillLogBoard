---
milestone: "v0.9-cleanup"
phase: "Template Forge Cleanup"
slice: "04_validator_filled_template_checks"
title: "filled-template validator checks"
priority: "P0"
status: "completed"
target_version: "v0.9-cleanup"
---

# 04_validator_filled_template_checks — filled-template validator checks

## Objective

Strengthen Template Forge validation for templates that have moved beyond scaffold TODOs into filled implementation.

## Context

v0.9 Template Forge is functionally complete and CI is green. This cleanup phase polishes docs, CLI UX, validator depth, and CI maintenance before v1.0 Live Board.

## Target Files

- src/skilllogboard/template_forge/validator.py
- tests/test_template_forge_validator.py
- tests/test_cli_template_forge.py
- docs/template_forge.md

## Implementation Steps

1. Inspect current validator checks for scaffold/file/marker/dependency policy.
2. Add or refine checks for filled templates: import safety, descriptor field presence, default_config presence, metric_names presence, and docs/test/example presence.
3. Keep scaffolded Draft templates as warnings, not false failures, unless required files are missing.
4. Do not execute arbitrary heavy example training code during validation.
5. If import validation is risky, gate it behind a safe flag or document limitation.
6. Add tests for a minimal filled fake template and a scaffolded TODO template.

## Acceptance Criteria

- Validator distinguishes scaffolded TODO templates from filled templates.
- A minimal filled fake template can pass validation.
- Heavy core dependencies are still detected.
- Validator does not execute unsafe long-running code.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_template_forge_validator.py tests/test_cli_template_forge.py
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
**Verification command(s):** `.venv/bin/python -m pytest -q tests/test_template_forge_validator.py tests/test_cli_template_forge.py`; `.venv/bin/python -m ruff check .`  
**Notes:** Validator now statically checks filled-template descriptor values and default skills without importing template modules or running example training code.

<!-- AGENT_STATUS: COMPLETED -->
