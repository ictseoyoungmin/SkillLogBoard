---
milestone: "v0.8"
phase: "Agent Research Layer"
day: "2"
slice: "03_agent_init_cli"
title: "agent init CLI"
priority: "P0"
status: "pending"
target_version: "v0.8-agent-research"
---

# 03_agent_init_cli — agent init CLI

## Objective

Add `skilllog agent init` CLI command.

## Context

Users and agents need a single command to bootstrap the project-level `.skilllog/` control plane.

## Dependencies

- 02_default_rules_and_report_spec_generation

## Target Files

- src/skilllogboard/cli/main.py
- src/skilllogboard/agent/skills.py
- tests/test_cli_agent.py

## Implementation Steps

1. Add `agent` command group or equivalent argparse subcommand.
2. Add `skilllog agent init`.
3. Support `--root-dir` or operate on current directory by default.
4. Support `--template generic|ir-drop|trajectory` if straightforward; otherwise keep generic only and document planned template-specific init.
5. Support no-overwrite default behavior.
6. Print created/skipped files.
7. Add CLI tests.

## Acceptance Criteria

- `skilllog agent init` appears in help.
- Command creates `.skilllog/` files in a temp directory.
- Existing files are protected.
- CLI test passes.

## Verification Commands

```bash
pytest -q tests/test_cli_agent.py
skilllog --help
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

