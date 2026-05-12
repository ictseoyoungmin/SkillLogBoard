---
milestone: "v0.8"
phase: "Agent Research Layer"
day: "4"
slice: "04_agent_check_cli"
title: "agent check CLI"
priority: "P0"
status: "pending"
target_version: "v0.8-agent-research"
---

# 04_agent_check_cli — agent check CLI

## Objective

Add `skilllog agent check` CLI command.

## Context

Human users and coding agents need a simple completion gate command.

## Dependencies

- 03_agent_rules

## Target Files

- src/skilllogboard/cli/main.py
- src/skilllogboard/agent/checks.py
- tests/test_cli_agent.py

## Implementation Steps

1. Add `skilllog agent check RUN_DIR`.
2. Support `--require-report`.
3. Support `--json` for machine-readable output if feasible.
4. Print pass/warn/error summary.
5. Return non-zero exit code when error-level checks fail.
6. Add CLI tests.

## Acceptance Criteria

- `skilllog agent check` appears in help.
- Command prints readable results.
- Command returns non-zero on error-level failure.
- JSON output works or is clearly deferred.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_cli_agent.py tests/test_agent_checks.py
```

## Non-goals

- Do not implement unrelated future features.

## Handoff Notes

- Keep this slice focused and small.
- Preserve existing v0.7/v0.6 public APIs and run folder compatibility.
- Do not introduce built-in LLM inference, cloud calls, or automatic code generation.
- Core install must remain lightweight. Do not add torch, lightning, sklearn, pandas, matplotlib, LLM SDKs, or domain packages to core dependencies.
- Agent files must be local, inspectable Markdown/JSONL/YAML-compatible artifacts.
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
**Completed at:** 2026-05-12
**Completed by:** Codex
**Verification command(s):** .venv/bin/ruff check .; .venv/bin/pytest -q; .venv/bin/pytest -q tests/test_agent_action_log.py tests/test_agent_init.py tests/test_agent_handoff.py tests/test_agent_checks.py tests/test_agent_rules.py tests/test_cli_agent.py; .venv/bin/python examples/basic_usage.py; .venv/bin/python examples/ir_drop_example.py; .venv/bin/python examples/trajectory_example.py; .venv/bin/python -m build --no-isolation; .venv/bin/skilllog --version
**Notes:** Implemented v0.8 Agent Research Layer as a local-first file workflow with no built-in LLM, cloud sync, or automatic code generation. Template-specific agent init uses existing template metadata for implemented templates.

<!-- AGENT_STATUS: COMPLETED -->

