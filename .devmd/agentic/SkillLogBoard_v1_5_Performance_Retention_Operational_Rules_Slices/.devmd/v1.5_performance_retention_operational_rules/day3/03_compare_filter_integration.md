---
milestone: "v1.5"
phase: "Performance, Retention, and Operational Rules"
day: "day3"
slice: "03_compare_filter_integration"
title: "compare filter integration"
priority: "P0"
status: "completed"
target_version: "v1.5"
---

# 03_compare_filter_integration — compare filter integration

## Objective

Integrate tags/groups/baseline with Compare selection.

## Context

v1.5 makes SkillLogBoard sustainable for real local research projects by adding performance guardrails, retention/pruning policy, JSONL rotation, compare scalability, and agent-safe operational rules.

## Dependencies

- v1.4 Portable Report Maturity completed or planned separately.
- v1.2/v1.3 Live Board app shell and commercial UI contracts are available.
- Agent Research Layer and Template Forge concepts are available.

## Target Files

- src/skilllogboard/live/project.py
- src/skilllogboard/live/server.py
- tests/test_live_project.py
- tests/test_live_server.py

## Implementation Steps

1. Allow compare candidates to be filtered by tag/group/status.
2. Surface baseline/reference run.
3. Return delta vs baseline where available.
4. Add tests.

## Acceptance Criteria

- Compare supports filtered candidates.
- Baseline is represented.
- Delta fields are available.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_live_project.py tests/test_live_server.py
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
- B1: build_compare_state accepts filters and applies them before candidate selection.
- B2: Compare public runs include tags/group/baseline and series include delta_from_baseline.
- B3: tests/test_v15_live_compare.py verifies tag-filtered compare and baseline deltas.
**Notes:** Implemented in the local v1.5 working tree; no destructive prune/delete action was executed.

<!-- AGENT_STATUS: COMPLETED -->
