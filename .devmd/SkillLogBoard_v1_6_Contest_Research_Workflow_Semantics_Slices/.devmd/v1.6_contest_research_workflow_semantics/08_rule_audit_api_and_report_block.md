---
milestone: "v1.6"
phase: "Contest / Research Workflow Semantics"
slice: "08_rule_audit_api_and_report_block"
title: "rule audit API and report block"
priority: "P1"
status: "pending"
---

# 08_rule_audit_api_and_report_block — rule audit API and report block

## Objective

Add a lightweight rule audit API for project/contest policies such as test data policy, submission threshold, fold count, and main metric mode.

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
- src/skilllogboard/rules/
- src/skilllogboard/reports/report_builder.py
- src/skilllogboard/live/readers.py
- tests/test_rule_audit.py
- tests/test_report_rendering.py
- docs/operational_rules.md
- docs/agent_research_layer.md

## Implementation Steps

1. Design `RunLogger.log_rule_audit(name, status, expected=None, actual=None, severity="info", metadata=None)`.
2. Support statuses: `pass`, `warning`, `fail`, `skipped`.
3. Persist rule audit to `rules/audit.json` and optionally `rules/audit.md`.
4. Add manifest summary fields such as pass/warning/fail counts.
5. Render Rule Audit block in report.
6. Expose audit metadata to Live Board readers.
7. Add tests for pass/fail/warning/skipped rules.
8. Document contest examples: `test_data_policy`, `submission_threshold`, `fold_count`, `main_metric_mode`.

## Acceptance Criteria

- Rule audit entries can be logged.
- Report displays rule audit summary and details.
- Manifest includes rule audit summary.
- Agents can read structured audit JSON.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_rule_audit.py tests/test_report_rendering.py
python examples/live_demo.py --multi-run --runs 5 --rich
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

- Rule audit records evidence; it should not become a full policy engine in v1.6.
- Use clear status/severity values so agents can parse them.

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

