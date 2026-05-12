---
milestone: "v0.8"
phase: "Agent Research Layer"
day: "4"
slice: "03_agent_rules"
title: "agent-specific rules"
priority: "P0"
status: "pending"
target_version: "v0.8-agent-research"
---

# 03_agent_rules — agent-specific rules

## Objective

Add agent-specific rule executors for handoff/action/completion requirements.

## Context

Agent checks should integrate with the existing rule philosophy when feasible.

## Dependencies

- 02_agent_completion_checks

## Target Files

- src/skilllogboard/skills/agent_rules.py
- src/skilllogboard/skills/rules.py
- tests/test_agent_rules.py
- tests/test_skills_rules.py

## Implementation Steps

1. Create `agent_rules.py` or extend the registry cleanly.
2. Implement `agent_handoff_required`.
3. Implement `agent_actions_required`.
4. Implement `agent_no_error_rules`.
5. Optional: implement `agent_required_commands` if command matching is simple.
6. Return existing RuleResult format if available.
7. Add tests.

## Acceptance Criteria

- `agent_handoff_required` works.
- `agent_actions_required` works.
- `agent_no_error_rules` works.
- Rules do not crash when agent folder is missing.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_agent_rules.py tests/test_skills_rules.py
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

