---
milestone: "v1.6"
phase: "Contest / Research Workflow Semantics"
slice: "01_status_consistency_fix"
title: "status consistency fix"
priority: "P0"
status: "pending"
---

# 01_status_consistency_fix — status consistency fix

## Objective

Ensure final run status is consistent across manifest.yaml, summary.md, dashboard.html, report outputs, and Live Board summaries.

## Context

v1.6 is motivated by the mosquito alpha-test feedback. The core finding is that SkillLogBoard can already collect experiment evidence, but contest/research workflow semantics are still encoded as user conventions.

This milestone should promote repeated contest/research patterns into first-class SkillLogBoard concepts:

```text
submission gate
OOF/test prediction roles
fold metrics
artifact role metadata
negative tag filtering
compact/quiet agent-friendly CLI
auto findings draft
rule audit
structured feedback backlog
```

## Dependencies

- v1.5 Performance, Retention, and Operational Rules cleanup completed.
- alpha-test-project/mosquito feedback exists and is used as product evidence.
- Static report package and Live Board remain separate product surfaces.

## Target Files

- src/skilllogboard/core/logger.py
- src/skilllogboard/summary.py
- src/skilllogboard/dashboard/
- src/skilllogboard/reports/
- src/skilllogboard/live/readers.py
- tests/test_status_consistency.py
- tests/test_run_logger.py
- tests/test_report_rendering.py
- alpha-test-project/mosquito/results/backlog/skilllog_feature_feedback.md

## Implementation Steps

1. Reproduce the alpha-test bug: manifest status is `completed` while summary.md shows `running`.
2. Identify whether summary/dashboard/report are generated before `logger.finish()` writes final status.
3. Refactor finish order so final status is written before summary/dashboard/report generation, or force those builders to reload the final manifest.
4. Ensure failed runs also regenerate summary/report with `failed` status.
5. Add a test for completed status consistency.
6. Add a test for failed status consistency.
7. Update alpha-test feedback/backlog with the resolved bug reference.

## Acceptance Criteria

- A completed run shows `completed` in manifest.yaml and summary.md.
- A failed run shows `failed` in manifest.yaml and summary.md.
- Dashboard/report status blocks do not show stale `running` after finish.
- Live Board summary uses the final manifest status.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_status_consistency.py tests/test_run_logger.py tests/test_report_rendering.py
python examples/basic_usage.py
```

## Non-goals

- Do not implement TensorBoard/W&B import.
- Do not implement Prometheus/Grafana integration.
- Do not implement cloud sync.
- Do not implement multi-user auth.
- Do not add a database backend.
- Do not publish to TestPyPI/PyPI in this milestone.
- Do not make static reports depend on the Live Board server.
- Do not require external CDN/network access for portable reports.
- Do not weaken local-first file-backed behavior.

## Additional Notes

- This is a trust/evidence bug. Complete before adding new contest helpers.
- Do not hide inconsistencies with UI-only formatting; fix generation/read order.

## Handoff Notes

- Keep changes focused on contest/research semantics, not generic MLOps sprawl.
- Preserve backward compatibility for existing runs and report packages.
- Prefer explicit artifact roles and manifest metadata over filename-only conventions.
- Keep helpers lightweight: they should reduce boilerplate, not impose a full contest framework.
- If an item is deferred, record the reason in the Agent Completion Block.
- Update docs, examples, and alpha-test feedback/backlog when user-visible behavior changes.

---

## Agent Completion Block

- [ ] Implementation completed
- [ ] Acceptance criteria verified
- [ ] Tests or smoke checks executed
- [ ] No unrelated files changed
- [ ] Notes added below if anything was skipped or deferred

**Status:** PENDING  
**Completed at:**  
**Completed by:**  
**Verification command(s):**  
**Notes:**  

<!-- AGENT_STATUS: PENDING -->

