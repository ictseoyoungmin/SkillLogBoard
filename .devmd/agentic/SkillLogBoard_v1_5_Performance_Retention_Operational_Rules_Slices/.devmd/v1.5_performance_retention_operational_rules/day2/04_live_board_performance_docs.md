---
milestone: "v1.5"
phase: "Performance, Retention, and Operational Rules"
day: "day2"
slice: "04_live_board_performance_docs"
title: "Live Board performance docs"
priority: "P0"
status: "completed"
target_version: "v1.5"
---

# 04_live_board_performance_docs — Live Board performance docs

## Objective

Document performance model and payload budgets.

## Context

v1.5 makes SkillLogBoard sustainable for real local research projects by adding performance guardrails, retention/pruning policy, JSONL rotation, compare scalability, and agent-safe operational rules.

## Dependencies

- v1.4 Portable Report Maturity completed or planned separately.
- v1.2/v1.3 Live Board app shell and commercial UI contracts are available.
- Agent Research Layer and Template Forge concepts are available.

## Target Files

- docs/live_board.md
- docs/operational_rules.md
- README.md

## Implementation Steps

1. Explain summary-first model.
2. Explain full-series lazy loading.
3. Explain max run/max point limits.
4. Explain index rebuild command.
5. Document expected large project behavior.

## Acceptance Criteria

- Performance docs exist.
- Payload budgets are documented.
- Index rebuild is documented.

## Verification Commands

```bash
python - <<'PY'
from pathlib import Path
text = Path('docs/operational_rules.md').read_text(encoding='utf-8').lower()
assert 'summary' in text and 'lazy' in text and 'index' in text
print('performance docs check passed')
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
- B1: docs/live_board.md documents summary-first payloads, /api/series, clamp bounds, filters, and index rebuild.
- B2: docs/operational_rules.md captures performance budgets and lazy-series policy.
- B3: README.md references v1.5 operational features.
**Notes:** Implemented in the local v1.5 working tree; no destructive prune/delete action was executed.

<!-- AGENT_STATUS: COMPLETED -->
