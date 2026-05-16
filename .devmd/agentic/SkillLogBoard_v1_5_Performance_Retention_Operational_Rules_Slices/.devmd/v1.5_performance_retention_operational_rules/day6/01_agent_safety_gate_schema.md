---
milestone: "v1.5"
phase: "Performance, Retention, and Operational Rules"
day: "day6"
slice: "01_agent_safety_gate_schema"
title: "agent safety gate schema"
priority: "P0"
status: "completed"
target_version: "v1.5"
---

# 01_agent_safety_gate_schema — agent safety gate schema

## Objective

Define agent safety gate schema.

## Context

v1.5 makes SkillLogBoard sustainable for real local research projects by adding performance guardrails, retention/pruning policy, JSONL rotation, compare scalability, and agent-safe operational rules.

## Dependencies

- v1.4 Portable Report Maturity completed or planned separately.
- v1.2/v1.3 Live Board app shell and commercial UI contracts are available.
- Agent Research Layer and Template Forge concepts are available.

## Target Files

- src/skilllogboard/agent/safety.py
- docs/agent_research_layer.md
- tests/test_agent_safety.py

## Implementation Steps

1. Define allowed paths, denied paths, allowed commands, denied commands, mutation scope.
2. Default deny core library mutation unless explicitly allowed.
3. Represent safety gate in YAML/JSON.
4. Add tests.

## Acceptance Criteria

- Safety gate schema exists.
- Core mutation is protected by default.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_agent_safety.py
```

## Non-goals

- Do not make destructive deletion the default behavior.
- Do not require a database for indexing/cache.
- Do not claim SkillLogBoard executes agents automatically.
- Do not implement TensorBoard/W&B import.
- Do not implement Prometheus/Grafana integration.
- Do not implement cloud sync.
- Do not implement multi-user auth.
- Do not add a database backend.
- Do not perform TestPyPI/PyPI publishing in this slice.
- Do not weaken local-first, inspectable-file behavior.

## Handoff Notes

- Keep the slice focused and reviewable.
- Prefer additive metadata/state fields over breaking existing artifact contracts.
- Preserve the separation between portable static evidence and local Live Board app behavior.
- If an item is deferred, document the reason in the Agent Completion Block.
- Update related docs/status/changelog when user-visible behavior changes.

---

## Agent Completion Block

- [x] Implementation completed
- [x] Acceptance criteria verified
- [x] Tests or smoke checks executed
- [x] No unrelated files changed
- [x] Notes added below if anything was skipped or deferred

**Status:** COMPLETED
**Completed at:** 2026-05-16
**Completed by:** Codex
**Verification command(s):**
- .venv/bin/python -m pytest tests/test_v15_index_query.py tests/test_v15_live_compare.py tests/test_v15_retention_agent.py tests/test_v15_artifact_storage.py -q
- .venv/bin/python -m pytest tests/test_live_project.py tests/test_live_server.py tests/test_cli.py tests/test_cli_live.py tests/test_cli_agent.py tests/test_agent_handoff.py tests/test_template_forge_validator.py tests/test_report_assets.py tests/test_report_manifest.py -q
- .venv/bin/python -m ruff check src/skilllogboard tests/test_v15_index_query.py tests/test_v15_live_compare.py tests/test_v15_retention_agent.py tests/test_v15_artifact_storage.py
**Completion evidence backlog:**
- B1: src/skilllogboard/agent/safety.py defines allowed/denied path and command gates.
- B2: Default policy denies core/package/manifest mutations.
- B3: tests/test_v15_retention_agent.py verifies path allow/deny behavior.
**Notes:** Implemented in the local v1.5 working tree; no destructive prune/delete action was executed.

<!-- AGENT_STATUS: COMPLETED -->
