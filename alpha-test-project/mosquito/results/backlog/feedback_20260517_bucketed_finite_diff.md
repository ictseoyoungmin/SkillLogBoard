# Mosquito Alpha-test Structured Feedback: Bucketed Finite Difference

## 1. Quick Feedback Summary

## Test Context

| Field | Value |
|---|---|
| Project name | mosquito-contest |
| Test folder | `alpha-test-project/mosquito` |
| Date / time | 2026-05-17 20:54 KST |
| Tester | agent |
| SkillLogBoard version | 1.5.0.dev0 |
| Python version | 3.10.12 |
| OS / environment | WSL2, GTX 1660, torch cu128 installed |
| Test type | contest / research / agent workflow / report workflow |
| Dataset or task | DACON mosquito +80ms 3D trajectory prediction |

## Overall Verdict

| Category | Rating | Notes |
|---|---:|---|
| Setup / install | 4 | GPU torch smoke passed, but CUDA wheel install on `/mnt/f` venv was slow. |
| Logging API usability | 4 | RunLogger captured config, metrics, artifacts, dashboard, summary. |
| Metric tracking | 4 | Main metric was clear, but submission gate status is note-only. |
| Artifact tracking | 3 | Prediction bundle exists, but artifact roles are convention-based. |
| Report generation | 4 | Package report and validate worked. |
| Live Board usability | 3 | Project index works, but family filtering needs negative tags. |
| Agent handoff usefulness | 3 | Markdown backlog helps, but no machine-readable handoff file exists. |
| Template/helper coverage | 2 | Contest CV/gated submission workflow required custom code. |
| Documentation clarity | 4 | Feedback guide made product feedback structure clearer. |

## One-line Summary

```text
Bucketed finite-difference provided useful non-tree evidence but did not beat the global hit-tuned finite-difference baseline; SkillLog captured the run, while contest-specific gate/prediction/fold conventions remain custom code.
```

# 2. Run-level Feedback

## Run Metadata

| Field | Value |
|---|---|
| Run ID | `2026-05-17_20-54-48_physics_bucketed_finite_diff` |
| Run name | `physics_bucketed_finite_diff` |
| Config path | `alpha-test-project/mosquito/configs/physics_bucketed_finite_diff.yaml` |
| Command | `PYTHONPATH=alpha-test-project/mosquito .venv/bin/python -m contest_mosquito.runner --config alpha-test-project/mosquito/configs/physics_bucketed_finite_diff.yaml` |
| Status | completed |
| Main metric | `val/r_hit@1cm` |
| Best metric value | `0.6011` |
| Runtime | see run `metrics.csv` |
| Tags | `physics`, `finite-difference`, `bucketed`, `non-tree` |

## What Worked Well

- RunLogger created a complete local evidence package with config, metric CSV, prediction artifact, summary, and dashboard.
- The config clearly separates model family and bucket parameters, so the run is reproducible.
- The below-threshold submission gate correctly produced no `submission.csv`.

## What Was Painful

- Submission gate result is not a structured manifest/report field; absence of a file still needs interpretation.
- Bucket coefficients are not stored as typed model artifacts, only implicit in code/config and predictions.
- Fold-level optimization details are hard to inspect from the generic report.

## Missing Evidence

| Missing item | Why it matters | Suggested location |
|---|---|---|
| `submission_gate_result` | Explains why no submission file exists despite completed run | manifest + report |
| `bucket_coefficients` | Needed to audit the learned physics policy | artifact + report table |
| `validation_split_policy` | Confirms random 5-fold policy and seed | report manifest |
| `model_family=non-tree` | Needed to filter away tree/LGBM runs in dashboard/compare | manifest metadata |

## Bug Candidates

| Symptom | Expected | Actual | Severity | Evidence path |
|---|---|---|---|---|
| Submission gate hidden in report | Report should show gate fail/pass | No submission file and no report block | P1 | `alpha-test-project/mosquito/results/report/report.html` |

## Improvement Candidate

| Proposed improvement | Type | Priority | Product area |
|---|---|---:|---|
| Add threshold-gated submission helper | helper | P1 | core/report |
| Add typed prediction bundle helper | helper | P1 | core/artifact |
| Add contest CV template | template | P1 | template/report |
| Add negative tag filters | CLI/UI | P2 | index/live/compare |
| Add coefficient/table artifact convention | helper | P2 | artifact/report |

# 3. Workflow-level Feedback

## Workflow Description

```text
Mosquito trajectory contest workflow runs train-only 5-fold validation, logs OOF/test prediction artifacts, and saves submission files only when validation R-Hit@1cm exceeds 0.7000.
```

## Repeated User Code

| Repeated code or convention | Frequency | Should become |
|---|---:|---|
| submission threshold gate | every contest run | helper / report block |
| OOF/test prediction artifact convention | every CV run | artifact helper |
| fold_metrics table logging | every CV run | fold-aware template |
| experiment backlog markdown | every run | agent/report template |
| non-tree/tree family tagging | every model family | manifest metadata helper |

## Workflow Friction

| Friction | Impact | Current workaround | Suggested SkillLogBoard feature |
|---|---|---|---|
| No submission gate block | Reviewer cannot tell if no file is expected | `logger.log_note` and backlog docs | submission gate artifact/report block |
| Prediction roles are ambiguous | Agents may confuse OOF and test predictions | `predictions.npz` convention | typed prediction bundle |
| Family filtering is manual | Tree-pass instruction is awkward in compare/report | custom tags and markdown note | negative filters and family metadata |

## Workflow-specific Helper Candidates

| Helper | Minimal API sketch | Priority |
|---|---|---:|
| threshold-gated submission writer | `logger.log_submission(path, score, threshold, role="contest")` | P1 |
| prediction bundle helper | `logger.log_predictions(oof=..., test=..., ids=..., role="cv")` | P1 |
| fold metrics helper | `logger.log_fold_metrics(rows, main_metric="val/r_hit@1cm")` | P1 |
| family metadata helper | `logger.log_model_family("non-tree")` | P2 |

# 4. Dashboard / Live Board Feedback

## Live Board Command

```bash
.venv/bin/python -m skilllogboard.cli.main watch alpha-test-project/mosquito/results/skilllog/mosquito-contest --project --no-open
```

## First Impression

| Question | Answer |
|---|---|
| Project/run mode가 명확했는가? | yes |
| Overview에서 현재 상태를 이해할 수 있었는가? | yes |
| Compare에 들어가기 전 어떤 run이 best인지 알 수 있었는가? | partially |
| Artifacts/Reports/Agent 탭이 실제 workflow와 연결되어 보였는가? | partially |
| UI가 외부 사용자에게 보여줄 만했는가? | yes, with contest gate additions |

## UI Evidence Gaps

| Evidence needed | Current visibility | Suggested UI location |
|---|---|---|
| submission gate pass/fail | hidden / note-only | Overview + Run detail + Report |
| best non-tree run | not directly visible | Compare filter / Overview card |
| artifact role | ambiguous | Artifacts |
| agent next action | markdown-only | Agent |

# 5. Report Artifact Feedback

## Report Outputs Checked

| File | Exists? | Rendered offline? | Notes |
|---|---|---|---|
| `dashboard.html` | yes | yes | Run-level dashboard exists. |
| `report/report.html` | yes | yes | `report validate --json` returned `ok=true`. |
| `report/report.md` | yes | n/a | Useful for handoff. |
| `report/report_manifest.yaml` | yes | n/a | Valid schema. |
| `report/tables/*` | yes | n/a | Leaderboard useful. |
| `report/figures/*` | yes | n/a | Figure exists. |

## Report Improvement Requests

| Request | Reason | Priority |
|---|---|---:|
| Add submission gate block | Explains why no submission.csv exists | P1 |
| Add CV summary block | Contest workflows rely on fold metrics | P1 |
| Add artifact role labels | OOF/test/submission artifacts need clear semantics | P1 |
| Add model-family filtering | User asked to pass tree models but report still ranks them | P2 |

# 6. Agent Workflow Feedback

## Agent Context

| Field | Value |
|---|---|
| Agent tool | Codex |
| Task | Continue mosquito contest experiments after reading `docs/Feedback.md` |
| Input instruction | Run next experiment and record feedback |
| Files read | `docs/Feedback.md`, `next_non_tree_experiments.md`, run metrics |
| Files changed | bucketed finite-diff model/config, structured feedback docs |
| Verification commands | pytest, ruff, SkillLog report validate |

## Agent Handoff Quality

| Question | Answer |
|---|---|
| Agent could identify current best run? | yes |
| Agent could identify next experiments? | yes |
| Agent could parse metrics and artifacts? | yes |
| Agent could understand failed/skipped runs? | partially |
| Agent had enough safety rules? | yes |
| Agent handoff was machine-readable? | partially |

# 9. Machine-readable Feedback Block

```json
{
  "feedback_schema_version": "1.0",
  "project": "mosquito-contest",
  "run_id": "2026-05-17_20-54-48_physics_bucketed_finite_diff",
  "tester_type": "agent",
  "overall_rating": 3,
  "main_metric": {
    "name": "val/r_hit@1cm",
    "value": 0.6011,
    "mode": "max"
  },
  "worked_well": [
    "RunLogger produced config, metrics, artifacts, dashboard, and summary for the run.",
    "Threshold gate correctly avoided writing a submission below 0.7000.",
    "Feedback guide made run/workflow/report/agent feedback more actionable."
  ],
  "pain_points": [
    "Submission gate result is not structured in manifest/report.",
    "OOF/test prediction roles are convention-based.",
    "Tree-pass workflow needs negative filters or family metadata."
  ],
  "bugs": [
    {
      "title": "Submission gate result hidden from report",
      "severity": "P1",
      "expected": "Report shows submission gate pass/fail and threshold.",
      "actual": "No submission file exists, but report has no explicit gate block.",
      "evidence_path": "alpha-test-project/mosquito/results/report/report.html"
    }
  ],
  "feature_requests": [
    {
      "title": "contest_cv template",
      "type": "template",
      "priority": "P1",
      "evidence": "contest_mosquito.runner repeats CV, OOF, fold metrics, and submission gate code.",
      "suggested_solution": "Add a template with fold-aware metrics, prediction bundle artifacts, and gated submission report block."
    },
    {
      "title": "typed prediction bundle",
      "type": "helper",
      "priority": "P1",
      "evidence": "predictions.npz stores both OOF and test predictions without typed artifact roles.",
      "suggested_solution": "Add logger.log_prediction_bundle(oof, test, ids, role='cv_predictions')."
    },
    {
      "title": "negative tag filters",
      "type": "CLI",
      "priority": "P2",
      "evidence": "User requested tree models be passed, but leaderboard/report still include previous tree runs.",
      "suggested_solution": "Support not tag:tree or --exclude-tag in runs, compare, report, and Live Board."
    }
  ],
  "next_actions": [
    "Try differentiable coefficient model that predicts finite-difference weights.",
    "Record submission gate result as structured artifact metadata.",
    "Keep ensemble disabled until a non-tree single model reaches 0.6800."
  ]
}
```
