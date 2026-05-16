---
milestone: "v1.5"
phase: "Performance, Retention, and Operational Rules"
day: "day7"
slice: "01_operational_rules_doc"
title: "operational rules document"
priority: "P0"
status: "completed"
target_version: "v1.5"
---

# 01_operational_rules_doc — operational rules document

## Objective

Create comprehensive operational rules documentation.

## Context

v1.5 makes SkillLogBoard sustainable for real local research projects by adding performance guardrails, retention/pruning policy, JSONL rotation, compare scalability, and agent-safe operational rules.

## Dependencies

- v1.4 Portable Report Maturity completed or planned separately.
- v1.2/v1.3 Live Board app shell and commercial UI contracts are available.
- Agent Research Layer and Template Forge concepts are available.

## Target Files

- docs/operational_rules.md
- README.md
- docs/status_matrix.md

## Implementation Steps

1. Document performance model.
2. Document retention/pruning safety.
3. Document JSONL rotation.
4. Document artifact storage modes.
5. Document agent safety gate and handoff.
6. Document compare filters and baseline policy.

## Acceptance Criteria

- Operational rules doc exists.
- Docs cover all v1.5 workstreams.
- Status matrix updated.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
text = Path('docs/operational_rules.md').read_text(encoding='utf-8').lower()
for word in ['retention','prune','agent','baseline','rotation']:
    assert word in text
print('operational rules docs check passed')
PY
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
- B1: docs/operational_rules.md added with performance, retention, rotation, artifact, and agent rules.
- B2: README.md and docs/live_board.md link the v1.5 operational behavior.
- B3: docs/status_matrix.md includes v1.5 implementation rows.
**Notes:** Implemented in the local v1.5 working tree; no destructive prune/delete action was executed.

<!-- AGENT_STATUS: COMPLETED -->
