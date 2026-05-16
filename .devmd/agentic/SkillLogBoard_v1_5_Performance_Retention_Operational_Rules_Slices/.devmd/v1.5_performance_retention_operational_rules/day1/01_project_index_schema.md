---
milestone: "v1.5"
phase: "Performance, Retention, and Operational Rules"
day: "day1"
slice: "01_project_index_schema"
title: "project index schema"
priority: "P0"
status: "completed"
target_version: "v1.5"
---

# 01_project_index_schema — project index schema

## Objective

Define a project-level run index schema for scalable project summaries.

## Context

v1.5 makes SkillLogBoard sustainable for real local research projects by adding performance guardrails, retention/pruning policy, JSONL rotation, compare scalability, and agent-safe operational rules.

## Dependencies

- v1.4 Portable Report Maturity completed or planned separately.
- v1.2/v1.3 Live Board app shell and commercial UI contracts are available.
- Agent Research Layer and Template Forge concepts are available.

## Target Files

- src/skilllogboard/index/
- src/skilllogboard/live/project.py
- tests/test_project_index.py
- docs/operational_rules.md

## Implementation Steps

1. Define index fields: run_id, path, status, started_at, updated_at, duration, key_metrics, tags, group, baseline flag, artifact count, warning count.
2. Choose index file location such as `.skilllogboard/index.json` or project-local cache.
3. Document cache as derived and rebuildable.
4. Add tests for schema serialization.

## Acceptance Criteria

- Project index schema exists.
- Index is explicitly rebuildable/derived.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_project_index.py
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
- B1: src/skilllogboard/index/schema.py defines ProjectIndex/ProjectIndexRun and DEFAULT_INDEX_PATH.
- B2: docs/operational_rules.md documents the index as derived and rebuildable.
- B3: tests/test_v15_index_query.py verifies schema fields, tags, baseline, and summaries.
**Notes:** Implemented in the local v1.5 working tree; no destructive prune/delete action was executed.

<!-- AGENT_STATUS: COMPLETED -->
