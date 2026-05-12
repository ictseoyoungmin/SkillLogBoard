---
milestone: "v0.8"
phase: "Agent Research Layer"
day: "4"
slice: "02_agent_completion_checks"
title: "agent completion checks"
priority: "P0"
status: "pending"
target_version: "v0.8-agent-research"
---

# 02_agent_completion_checks — agent completion checks

## Objective

Implement core completion checks for run/report/handoff readiness.

## Context

A task should not be marked complete if core evidence or handoff files are missing.

## Dependencies

- 01_agent_check_result_schema

## Target Files

- src/skilllogboard/agent/checks.py
- tests/test_agent_checks.py

## Implementation Steps

1. Implement `check_agent_completion(run_dir, require_report=False)`.
2. Check for `manifest.yaml`.
3. Check for `config.yaml`.
4. Check for `metrics.csv`.
5. Check for `skill_trace.jsonl`.
6. Check no error-level rule failures if trace exists.
7. Check `agent/actions.jsonl`.
8. Check `agent/handoff.md`.
9. If `require_report=True`, check `report/report_manifest.yaml`.
10. Add tests for pass/warn/error cases.

## Acceptance Criteria

- Completion check detects missing manifest/config/metrics.
- Completion check detects missing action log and handoff.
- Completion check detects error-level rule failures.
- Report requirement can be toggled.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_agent_checks.py
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

