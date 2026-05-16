---
milestone: "v1.5"
phase: "Performance, Retention, and Operational Rules"
day: "day2"
slice: "01_lazy_series_api_contract"
title: "lazy series API contract"
priority: "P0"
status: "completed"
target_version: "v1.5"
---

# 01_lazy_series_api_contract — lazy series API contract

## Objective

Make full metric series loading explicit and bounded.

## Context

v1.5 makes SkillLogBoard sustainable for real local research projects by adding performance guardrails, retention/pruning policy, JSONL rotation, compare scalability, and agent-safe operational rules.

## Dependencies

- v1.4 Portable Report Maturity completed or planned separately.
- v1.2/v1.3 Live Board app shell and commercial UI contracts are available.
- Agent Research Layer and Template Forge concepts are available.

## Target Files

- src/skilllogboard/live/server.py
- src/skilllogboard/live/project.py
- tests/test_live_server.py

## Implementation Steps

1. Define API for selected series only: run_id(s), metric, max_points, align, normalize.
2. Clamp max_points/max_runs.
3. Return downsampling/truncation metadata.
4. Add tests for invalid inputs and bounds.

## Acceptance Criteria

- Full series loading is explicit.
- Payload is bounded.
- Invalid input is safe.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_live_server.py tests/test_live_project.py
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
- B1: src/skilllogboard/live/server.py adds /api/series and filter-aware /api/compare.
- B2: src/skilllogboard/live/project.py clamps max_runs/max_points and returns downsampling metadata.
- B3: tests/test_v15_live_compare.py verifies bounded selected series.
**Notes:** Implemented in the local v1.5 working tree; no destructive prune/delete action was executed.

<!-- AGENT_STATUS: COMPLETED -->
