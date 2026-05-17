---
milestone: "v1.6"
phase: "Contest / Research Workflow Semantics"
slice: "02_artifact_role_metadata"
title: "artifact role metadata"
priority: "P1"
status: "pending"
---

# 02_artifact_role_metadata — artifact role metadata

## Objective

Add first-class artifact role metadata so reports, Live Board, and agents can distinguish OOF predictions, test predictions, fold metrics, submission candidates, and gate results.

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

- src/skilllogboard/artifacts/
- src/skilllogboard/core/logger.py
- src/skilllogboard/live/readers.py
- src/skilllogboard/reports/report_manifest.py
- src/skilllogboard/reports/report_builder.py
- tests/test_artifact_roles.py
- tests/test_live_readers.py
- tests/test_report_manifest.py
- docs/report_artifacts.md
- docs/operational_rules.md

## Implementation Steps

1. Inspect current artifact index/manifest schema.
2. Add optional role metadata to artifact records. Suggested roles: `oof_prediction`, `test_prediction`, `fold_metrics`, `submission_candidate`, `submission_gate`, `model_checkpoint`, `report_table`, `report_figure`, `experiment_note`.
3. Add optional metadata fields: `split`, `array_key`, `safe_for_metric`, `source_metric`, `threshold`, `passed`, `project_rule`.
4. Update `RunLogger.log_artifact` or equivalent helper to accept `role` and `metadata` without breaking existing calls.
5. Update report manifest serialization to include artifact roles.
6. Update Live Board artifact reader to expose role metadata.
7. Add tests for backward compatibility with artifacts that do not have roles.
8. Document artifact role conventions.

## Acceptance Criteria

- Artifact records can include role metadata.
- Existing artifact calls without role still work.
- Report manifest preserves role metadata.
- Live Board artifact metadata includes roles.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_artifact_roles.py tests/test_live_readers.py tests/test_report_manifest.py
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

- Do not infer artifact roles from filenames only. Filename heuristics may be a fallback, not the canonical source.
- Keep role values documented and stable enough for report/agent usage.

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

