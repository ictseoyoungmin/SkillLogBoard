---
milestone: "v1.6"
phase: "Contest / Research Workflow Semantics"
slice: "04_fold_metrics_and_prediction_bundle_helpers"
title: "fold metrics and prediction bundle helpers"
priority: "P1"
status: "pending"
---

# 04_fold_metrics_and_prediction_bundle_helpers — fold metrics and prediction bundle helpers

## Objective

Add lightweight helpers for CV fold metrics and OOF/test prediction bundles to reduce repeated contest boilerplate.

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
- src/skilllogboard/artifacts/
- src/skilllogboard/reports/report_builder.py
- tests/test_fold_metrics_helper.py
- tests/test_prediction_bundle_helper.py
- docs/report_artifacts.md
- examples/
- alpha-test-project/mosquito/contest_mosquito/runner.py

## Implementation Steps

1. Design `RunLogger.log_fold_metrics(rows, main_metric=None, mode=None, path=None, role="fold_metrics")`.
2. Persist fold metrics as a table artifact and register role `fold_metrics`.
3. Design `RunLogger.log_predictions(...)` or `log_prediction_bundle(...)` for OOF/test arrays and IDs.
4. Suggested fields: `oof_pred`, `test_pred`, `train_ids`, `test_ids`, `path=None`, `role="cv_predictions"`, `metadata=None`.
5. Store prediction bundle in a transparent format such as `.npz` plus artifact role metadata.
6. Record array key metadata so agents can understand `oof_pred`, `test_pred`, `train_ids`, and `test_ids` without reading runner code.
7. Add report metadata block for prediction bundle and fold metrics.
8. Add tests for minimal fold metrics, prediction bundle, missing optional test predictions, and metadata serialization.
9. Update mosquito runner to use helpers where low risk.

## Acceptance Criteria

- Fold metrics can be logged with one helper call.
- Prediction bundles can be logged with explicit OOF/test roles.
- Artifact index/report manifest include role and array-key metadata.
- Report can list fold metrics and prediction bundle metadata.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_fold_metrics_helper.py tests/test_prediction_bundle_helper.py tests/test_report_manifest.py
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

- Do not force scikit-learn, PyTorch, or numpy-heavy dependencies into core unless already present or optional.
- If numpy is optional, support metadata-only registration or keep helper behind an extra.

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

