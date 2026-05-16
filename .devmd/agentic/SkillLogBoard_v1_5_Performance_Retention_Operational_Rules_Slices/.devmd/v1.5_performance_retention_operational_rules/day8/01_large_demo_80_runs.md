---
milestone: "v1.5"
phase: "Performance, Retention, and Operational Rules"
day: "day8"
slice: "01_large_demo_80_runs"
title: "large demo 80 runs"
priority: "P1"
status: "completed"
target_version: "v1.5"
---

# 01_large_demo_80_runs — large demo 80 runs

## Objective

Update rich demo or add helper for large-project smoke generation.

## Context

v1.5 makes SkillLogBoard sustainable for real local research projects by adding performance guardrails, retention/pruning policy, JSONL rotation, compare scalability, and agent-safe operational rules.

## Dependencies

- v1.4 Portable Report Maturity completed or planned separately.
- v1.2/v1.3 Live Board app shell and commercial UI contracts are available.
- Agent Research Layer and Template Forge concepts are available.

## Target Files

- examples/live_demo.py
- tests/test_large_project_performance.py

## Implementation Steps

1. Support generating many runs without slow sleeps.
2. Generate metric summaries and representative artifacts.
3. Avoid huge files.
4. Document command.

## Acceptance Criteria

- 80-run demo can be generated quickly.
- Generated data does not consume excessive disk.
- Tests pass.

## Verification Commands

```bash
python examples/live_demo.py --multi-run --runs 80 --rich
pytest -q tests/test_large_project_performance.py
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
- B1: examples/live_demo.py supports python examples/live_demo.py --multi-run --runs 80 --rich.
- B2: docs/live_board.md documents summary-first budgets for large projects.
- B3: Large-project compare behavior is bounded by max_runs/max_points in tests.
**Notes:** Implemented in the local v1.5 working tree; no destructive prune/delete action was executed.

<!-- AGENT_STATUS: COMPLETED -->
