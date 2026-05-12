---
milestone: "v0.8-cleanup"
phase: "Agent Research Layer Cleanup"
slice: "03_agent_check_strictness_and_exit_policy"
title: "agent check strictness and exit policy"
priority: "P0"
status: "completed"
target_version: "v0.8-cleanup"
---

# 03_agent_check_strictness_and_exit_policy — agent check strictness and exit policy

## Objective

Clarify or implement `skilllog agent check` behavior for soft vs strict completion checks.

## Context

v0.8 Agent Research Layer is functionally complete and CI is green. This cleanup phase resolves minor policy, documentation, CLI, and validation issues before starting v0.9 Template Forge.

## Dependencies

- v0.8 Agent Research Layer completed.
- Latest main CI is green.
- v0.7 Report Artifact Layer remains compatible.

## Target Files

- src/skilllogboard/agent/checks.py
- src/skilllogboard/cli/main.py
- tests/test_agent_checks.py
- tests/test_cli_agent.py
- docs/agent_research_layer.md

## Implementation Steps

1. Inspect current `check_agent_completion()` behavior and CLI exit-code policy.
2. Decide whether to implement `--strict` / `--soft` or document current behavior as intentionally strict.
3. Recommended behavior: default check reports warnings/errors clearly; `--strict` returns non-zero on warnings as well as errors; default returns non-zero only on error-level failures.
4. If changing behavior, add CLI tests for pass, warning, and error cases.
5. Ensure early/incomplete runs have readable output instead of confusing failure messages.
6. Update docs with examples for normal agent workflow and incomplete run behavior.

## Acceptance Criteria

- `skilllog agent check` behavior is predictable and documented.
- Exit code behavior is tested.
- Incomplete runs produce readable warnings/errors.
- Docs explain when failure is expected.

## Verification Commands

```bash
pytest -q tests/test_agent_checks.py tests/test_cli_agent.py
skilllog agent --help || skilllog --help
```

## Non-goals

- Do not begin v0.9 Template Forge implementation.
- Do not implement Live Board.
- Do not add built-in LLM inference, cloud calls, or automatic code generation.
- Do not change public RunLogger APIs.
- Do not add heavy dependencies to core.

## Handoff Notes

- Keep this cleanup focused.
- Preserve v0.8 behavior and all existing tests.
- If an item is intentionally deferred, update docs and record the reason in the Agent Completion Block.
- Core install must remain lightweight.

---

## Agent Completion Block

- [x] Implementation completed
- [x] Acceptance criteria verified
- [x] Tests or smoke checks executed
- [x] No unrelated files changed
- [x] Notes added below if anything was skipped or deferred

**Status:** COMPLETED  
**Completed at:** 2026-05-12  
**Completed by:** Codex  
**Verification command(s):** `.venv/bin/python -m pytest -q tests/test_agent_checks.py tests/test_cli_agent.py`; `.venv/bin/skilllog --help`; `.venv/bin/python -m ruff check .`  
**Notes:** Default `skilllog agent check` fails on errors; `--strict` also fails on warnings.

<!-- AGENT_STATUS: COMPLETED -->
