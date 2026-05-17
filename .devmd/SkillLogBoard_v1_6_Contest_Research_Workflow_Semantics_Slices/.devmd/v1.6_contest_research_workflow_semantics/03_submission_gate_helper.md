---
milestone: "v1.6"
phase: "Contest / Research Workflow Semantics"
slice: "03_submission_gate_helper"
title: "submission gate helper"
priority: "P1"
status: "pending"
---

# 03_submission_gate_helper — submission gate helper

## Objective

Add a lightweight helper to record contest submission threshold decisions even when no submission file is saved.

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
- src/skilllogboard/reports/report_manifest.py
- src/skilllogboard/live/readers.py
- tests/test_submission_gate.py
- tests/test_report_rendering.py
- docs/report_artifacts.md
- alpha-test-project/mosquito/contest_mosquito/runner.py

## Implementation Steps

1. Design `RunLogger.log_submission_gate(...)` API.
2. Suggested API: `log_submission_gate(metric, value, threshold, passed=None, mode="gte", path=None, role="submission_gate", metadata=None)`.
3. If `passed` is omitted, compute it from value/threshold/mode.
4. If path is provided and gate passed, register submission artifact with role `submission_candidate` or `submission_file`.
5. If path is absent or gate failed, still register a `submission_gate` evidence artifact/manifest entry.
6. Record gate result in manifest metadata and report manifest.
7. Expose gate result to report builder and Live Board reader.
8. Add tests for passed gate, failed gate, missing path, and unsupported mode.
9. Refactor mosquito runner to use helper in one experiment path if feasible.

## Acceptance Criteria

- Submission gate pass/fail is recorded even when no submission file exists.
- Report can display the gate decision.
- Manifest/report manifest include metric, value, threshold, mode, passed, and optional path.
- No submission file is copied on failed gate unless explicitly requested.
- Tests pass.

## Verification Commands

```bash
pytest -q tests/test_submission_gate.py tests/test_report_rendering.py
python alpha-test-project/mosquito/run_experiment.py --help || true
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

- This helper should not decide contest strategy; it only records the policy and result.
- Keep the helper generic enough for Kaggle/DACON/custom contests.

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

