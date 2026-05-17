---
milestone: "v1.6"
phase: "Contest / Research Workflow Semantics"
slice: "10_mosquito_alpha_test_integration_and_rc"
title: "mosquito alpha-test integration and release candidate"
priority: "P0"
status: "pending"
---

# 10_mosquito_alpha_test_integration_and_rc — mosquito alpha-test integration and release candidate

## Objective

Use the mosquito alpha-test to verify v1.6 semantics and close the milestone with evidence.

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

- alpha-test-project/mosquito/contest_mosquito/runner.py
- alpha-test-project/mosquito/results/backlog/skilllog_feature_feedback.md
- alpha-test-project/mosquito/results/backlog/skilllog_product_backlog.md
- docs/v1_6_release_candidate_note.md
- CHANGELOG.md
- docs/status_matrix.md
- tests/

## Implementation Steps

1. Select one mosquito experiment path to use new v1.6 helpers.
2. Log artifact roles for OOF/test predictions and fold metrics.
3. Log submission gate result.
4. Log at least one rule audit entry.
5. Generate report and validate that auto findings and submission gate block appear.
6. Run compare with top-k/quiet/filter options against mosquito runs.
7. Compile feedback backlog if feedback compiler exists.
8. Update `skilllog_feature_feedback.md` with before/after notes.
9. Write `docs/v1_6_release_candidate_note.md` with verification commands and known limitations.
10. Update changelog and status matrix.

## Acceptance Criteria

- At least one mosquito alpha-test run uses v1.6 semantic helpers.
- Report shows auto findings and submission gate block.
- Artifact roles are visible in generated metadata.
- Rule audit evidence is generated.
- Compare compact/top-k/quiet workflow is demonstrated.
- v1.6 RC note records commands and outcomes.
- Tests pass.

## Verification Commands

```bash
pip install -e ".[dev,dashboard,report,live]"
ruff check .
pytest -q
python alpha-test-project/mosquito/run_experiment.py --help || true
python -m skilllogboard.cli.main compare alpha-test-project/mosquito/results/skilllog/mosquito-contest --metric val/r_hit@1cm --top-k 5 --quiet || true
python -m build --no-isolation
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

- If mosquito data or dependencies are not available in the current environment, document the limitation and run synthetic equivalent tests.
- Do not let contest score optimization block SkillLogBoard product verification.

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

