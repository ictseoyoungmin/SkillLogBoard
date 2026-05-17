# SkillLogBoard Alpha Test Feedback Guide

## Purpose

이 문서는 SkillLogBoard를 실제 연구/대회/에이전트 워크플로우에 적용한 뒤, 제품 개선에 직접 연결될 수 있는 피드백을 수집하기 위한 표준 양식입니다.

단순히 “좋았다 / 불편했다”를 기록하는 것이 아니라, 다음 질문에 답할 수 있도록 피드백을 구조화합니다.

```text
1. 어떤 workflow에서 SkillLogBoard가 실제로 도움이 되었는가?
2. 어떤 부분은 사용자가 반복 구현해야 했는가?
3. 어떤 정보가 dashboard / report / artifact / agent handoff에 부족했는가?
4. 어떤 기능이 template, helper, CLI, report, Live Board로 승격되어야 하는가?
5. 다음 개발 backlog로 바로 옮길 수 있는 개선 항목은 무엇인가?
```

---

## Feedback Principles

좋은 피드백은 다음 조건을 만족해야 합니다.

```text
- 재현 가능해야 한다.
- 어떤 run / command / config에서 발생했는지 알 수 있어야 한다.
- 단순 감상이 아니라 개선 방향으로 변환 가능해야 한다.
- 기능 요청과 버그를 구분해야 한다.
- 사람과 agent가 모두 읽을 수 있어야 한다.
```

피해야 할 피드백:

```text
- “UI가 별로다”
- “뭔가 불편하다”
- “자동화가 더 필요하다”
- “좋다”
```

좋은 피드백:

```text
- “submission threshold 미달로 파일이 저장되지 않았는데, dashboard/report에서 gate 결과가 명확히 보이지 않았다.”
- “CV 기반 contest 실험마다 OOF prediction, test prediction, fold_metrics artifact를 수동으로 같은 convention으로 저장했다.”
- “manifest.yaml은 completed인데 summary.md에는 running으로 남아 evidence 신뢰성이 떨어졌다.”
```

---

# 1. Quick Feedback Summary

## Test Context

| Field | Value |
|---|---|
| Project name |  |
| Test folder |  |
| Date / time |  |
| Tester | human / agent / mixed |
| SkillLogBoard version |  |
| Python version |  |
| OS / environment |  |
| Test type | example / contest / research / agent workflow / report workflow / live board |
| Dataset or task |  |

## Overall Verdict

| Category | Rating | Notes |
|---|---:|---|
| Setup / install | 1-5 |  |
| Logging API usability | 1-5 |  |
| Metric tracking | 1-5 |  |
| Artifact tracking | 1-5 |  |
| Report generation | 1-5 |  |
| Live Board usability | 1-5 |  |
| Agent handoff usefulness | 1-5 |  |
| Template/helper coverage | 1-5 |  |
| Documentation clarity | 1-5 |  |

## One-line Summary

```text
예: Core logging은 실제 contest workflow에 잘 붙었지만, submission gate / OOF artifact / fold-aware template은 사용자가 반복 구현해야 했다.
```

---

# 2. Run-level Feedback

하나의 실험 run마다 아래 항목을 작성합니다.

## Run Metadata

| Field | Value |
|---|---|
| Run ID |  |
| Run name |  |
| Config path |  |
| Command |  |
| Status | completed / failed / running / skipped |
| Main metric |  |
| Best metric value |  |
| Runtime |  |
| Tags |  |

## What Worked Well

```text
예:
- RunLogger로 config, metrics, artifacts, report를 한 run folder에 묶을 수 있었다.
- main_metric mode=max를 manifest에 남길 수 있어 나중에 best run 비교가 쉬웠다.
- fold_metrics.csv를 table artifact로 남길 수 있었다.
```

## What Was Painful

```text
예:
- contest submission threshold gate를 직접 구현해야 했다.
- OOF/test prediction artifact naming convention을 직접 정해야 했다.
- report에서 submission gate 통과/실패 여부가 바로 보이지 않았다.
```

## Missing Evidence

이 run을 나중에 다시 봤을 때 부족했던 evidence를 적습니다.

| Missing item | Why it matters | Suggested location |
|---|---|---|
|  |  | manifest / summary / report / dashboard / artifact / agent handoff |

예:

| Missing item | Why it matters | Suggested location |
|---|---|---|
| submission_gate_result | submission 파일이 왜 없는지 바로 알기 어려움 | report + manifest metadata |
| oof_artifact_role | prediction artifact가 OOF인지 test인지 convention이 불명확 | artifact_index metadata |
| validation_split_policy | CV 방식이 report에서 바로 보이지 않음 | report manifest / config table |

## Bug Candidates

| Symptom | Expected | Actual | Severity | Evidence path |
|---|---|---|---|---|
|  |  |  | P0/P1/P2 |  |

예:

| Symptom | Expected | Actual | Severity | Evidence path |
|---|---|---|---|---|
| summary status mismatch | summary.md status should match manifest.yaml | manifest completed, summary running | P0 | run_dir/summary.md |

## Improvement Candidate

| Proposed improvement | Type | Priority | Product area |
|---|---|---:|---|
|  | bug / helper / template / CLI / UI / report / agent | P0/P1/P2 | core / report / live / template / agent |

---

# 3. Workflow-level Feedback

개별 run이 아니라 전체 workflow 관점에서 작성합니다.

## Workflow Description

```text
예:
Mosquito trajectory contest에서 train.csv 기반 5-fold validation을 수행하고,
OOF prediction과 test prediction을 artifact로 저장한 뒤,
validation score가 threshold 이상일 때만 submission.csv를 생성한다.
```

## Repeated User Code

SkillLogBoard가 아직 제공하지 않아 사용자가 반복 구현한 코드를 기록합니다.

| Repeated code or convention | Frequency | Should become |
|---|---:|---|
| submission threshold gate | every contest run | helper / template |
| OOF/test prediction artifact convention | every CV run | artifact convention helper |
| fold_metrics table logging | every CV run | fold-aware template |
| experiment backlog markdown | every run | report/agent template |

## Workflow Friction

| Friction | Impact | Current workaround | Suggested SkillLogBoard feature |
|---|---|---|---|
|  |  |  |  |

예:

| Friction | Impact | Current workaround | Suggested SkillLogBoard feature |
|---|---|---|---|
| Submission not saved when score < threshold, but report does not highlight why | Reviewer may think submission failed | logger.log_note manually | submission gate artifact/report block |
| CV fold metrics need manual table construction | Repeated boilerplate | logger.log_table manually | fold-aware experiment template |

## Workflow-specific Helper Candidates

| Helper | Minimal API sketch | Priority |
|---|---|---:|
| threshold-gated submission writer | `logger.log_submission(path, score, threshold, role="contest")` | P1 |
| OOF/test prediction artifact helper | `logger.log_predictions(oof=..., test=..., ids=..., role="cv")` | P1 |
| fold metrics helper | `logger.log_fold_metrics(rows, main_metric="val/r_hit@1cm")` | P1 |
| contest report block | `ReportSpec(include_submission_gate=True)` | P2 |

---

# 4. Dashboard / Live Board Feedback

Live Board를 실제로 실행해 본 뒤 작성합니다.

## Live Board Command

```bash
skilllog watch <project_or_run_dir> --project
```

## First Impression

| Question | Answer |
|---|---|
| Project/run mode가 명확했는가? | yes / no |
| Overview에서 현재 상태를 이해할 수 있었는가? | yes / no |
| Compare에 들어가기 전 어떤 run이 best인지 알 수 있었는가? | yes / no |
| Artifacts/Reports/Agent 탭이 실제 workflow와 연결되어 보였는가? | yes / no |
| UI가 외부 사용자에게 보여줄 만했는가? | yes / no |

## Screen-level Feedback

| Screen | What worked | What was missing | Priority |
|---|---|---|---|
| Overview |  |  |  |
| Runs |  |  |  |
| Compare |  |  |  |
| Metric Lab |  |  |  |
| Artifacts |  |  |  |
| Reports |  |  |  |
| Agent |  |  |  |
| Settings |  |  |  |

## UI Evidence Gaps

| Evidence needed | Current visibility | Suggested UI location |
|---|---|---|
| submission gate pass/fail | hidden / note-only / visible | Overview / Run detail / Report |
| best metric trend | visible / not visible | Overview / Compare |
| artifact role | ambiguous / clear | Artifacts |
| agent next action | missing / visible | Agent |
| run status consistency | mismatch / consistent | Overview / Summary |

---

# 5. Report Artifact Feedback

정적 report/dashboard 산출물에 대한 피드백입니다.

## Report Outputs Checked

| File | Exists? | Rendered offline? | Notes |
|---|---|---|---|
| dashboard.html | yes / no | yes / no |  |
| report/report.html | yes / no | yes / no |  |
| report/report.md | yes / no | n/a |  |
| report/report_manifest.yaml | yes / no | n/a |  |
| report/tables/* | yes / no | n/a |  |
| report/figures/* | yes / no | n/a |  |
| report/chart_specs/* | yes / no | n/a |  |

## Report Quality

| Question | Answer |
|---|---|
| Report alone explains the run? | yes / no |
| Config is readable? | yes / no |
| Main metric is clear? | yes / no |
| Best metric mode is clear? | yes / no |
| Artifact provenance is clear? | yes / no |
| Tables/Figures are useful? | yes / no |
| Report can be shared without server? | yes / no |

## Report Improvement Requests

| Request | Reason | Priority |
|---|---|---:|
|  |  | P0/P1/P2 |

Examples:

| Request | Reason | Priority |
|---|---|---:|
| Add submission gate block | Explains why submission.csv is missing | P1 |
| Add CV summary block | Contest/research workflows rely on fold metrics | P1 |
| Add artifact role labels | OOF/test/submission artifacts need clear semantics | P1 |

---

# 6. Agent Workflow Feedback

agent가 SkillLogBoard를 사용해 연구를 수행하거나 이어받았을 때 작성합니다.

## Agent Context

| Field | Value |
|---|---|
| Agent tool | Codex / Claude / Cursor / other |
| Task |  |
| Input instruction |  |
| Files read |  |
| Files changed |  |
| Verification commands |  |

## Agent Handoff Quality

| Question | Answer |
|---|---|
| Agent could identify current best run? | yes / no |
| Agent could identify next experiments? | yes / no |
| Agent could parse metrics and artifacts? | yes / no |
| Agent could understand failed/skipped runs? | yes / no |
| Agent had enough safety rules? | yes / no |
| Agent handoff was machine-readable? | yes / no |

## Missing Agent Evidence

| Missing evidence | Why it matters | Suggested file |
|---|---|---|
| next_actions JSON | agent continuation | agent/handoff.json |
| verification command list | reproducibility | agent/handoff.json |
| blocked reason | avoid repeated failure | agent/blockers.md |
| safety scope | prevent risky edits | agent/safety_gate.yaml |

## Agent Backlog

| Backlog | Type | Priority |
|---|---|---:|
|  | agent / template / report / CLI / safety | P0/P1/P2 |

---

# 7. Template / Helper Backlog

이 섹션은 피드백을 곧바로 개발 backlog로 변환하기 위한 영역입니다.

## Template Candidates

| Template | Target user | Required features | Priority |
|---|---|---|---:|
| contest_cv | Kaggle/DACON/competition users | CV split, OOF artifact, fold metrics, gated submission | P1 |
| classification_basic | ML beginners/researchers | train/val metrics, confusion matrix, prediction artifact | P2 |
| segmentation_basic | vision researchers | mIoU, pixel metrics, mask figures | P2 |
| agent_research_loop | coding agents | handoff.json, verification commands, backlog update | P1 |

## Helper Candidates

| Helper | API sketch | Product area | Priority |
|---|---|---|---:|
| submission gate | `logger.log_submission(path, score, threshold)` | core/report | P1 |
| prediction bundle | `logger.log_predictions(oof, test, ids, role)` | core/artifact | P1 |
| fold-aware metrics | `logger.log_cv_results(fold_rows, main_metric)` | core/report | P1 |
| backlog writer | `logger.log_backlog(sections={...})` | agent/report | P2 |
| contest report block | `ReportSpec(blocks=["submission_gate", "cv_summary"])` | report | P2 |

---

# 8. Feedback-to-Backlog Conversion

피드백을 제품 backlog로 옮길 때 아래 기준을 사용합니다.

## Priority Rule

| Priority | Definition |
|---|---|
| P0 | evidence 신뢰성, 데이터 손실, 상태 불일치, 실행 실패 |
| P1 | 반복 구현이 많고 실제 workflow 생산성을 크게 올리는 기능 |
| P2 | 사용성/표현력 개선, 특정 workflow convenience |
| P3 | nice-to-have, polish, long-term idea |

## Type Rule

| Type | Examples |
|---|---|
| bug | status mismatch, broken link, missing artifact, wrong metric mode |
| helper | submission gate, prediction bundle, fold metrics |
| template | contest_cv, segmentation_basic, agent_research_loop |
| report | new report block, provenance display, table/figure layout |
| live | overview card, compare UI, artifact browser |
| agent | handoff.json, safety gate, validation feedback |
| docs | quickstart, examples, troubleshooting |

## Backlog Item Format

```markdown
## [P1][template] contest_cv template

### Problem
Contest-style experiments repeatedly require CV split, OOF prediction artifact, fold metrics, and threshold-gated submission handling.

### Evidence
- alpha-test-project/mosquito
- repeated manual implementation in contest_mosquito.runner
- feedback: “contest 전용 submission gate와 OOF artifact convention은 사용자가 직접 구현해야 함.”

### Proposed Solution
Add a `contest_cv` template or helper scaffold that includes:
- fold-aware metric logging
- OOF/test prediction artifact convention
- threshold-gated submission writer
- report block for submission gate result

### Acceptance Criteria
- A synthetic contest example can run end-to-end.
- No submission file is written below threshold.
- Report shows submission gate result.
- OOF/test predictions are registered as typed artifacts.
```

---

# 9. Machine-readable Feedback Block

사람이 작성한 Markdown과 별도로, agent가 파싱하기 쉬운 JSON block을 남깁니다.

```json
{
  "feedback_schema_version": "1.0",
  "project": "",
  "run_id": "",
  "tester_type": "human|agent|mixed",
  "overall_rating": 0,
  "main_metric": {
    "name": "",
    "value": null,
    "mode": "max|min"
  },
  "worked_well": [],
  "pain_points": [],
  "bugs": [
    {
      "title": "",
      "severity": "P0|P1|P2|P3",
      "expected": "",
      "actual": "",
      "evidence_path": ""
    }
  ],
  "feature_requests": [
    {
      "title": "",
      "type": "helper|template|report|live|agent|docs",
      "priority": "P0|P1|P2|P3",
      "evidence": "",
      "suggested_solution": ""
    }
  ],
  "next_actions": []
}
```

---

# 10. Mosquito Alpha-test Example Feedback

아래는 mosquito alpha-test에서 이미 드러난 피드백을 제품 backlog 형태로 정리한 예시입니다.

## [P0][bug] summary status should match manifest status

### Problem

A completed run can have `manifest.yaml` status as `completed` while `summary.md` still displays `running`.

### Why it matters

Static evidence must be trustworthy. If summary and manifest disagree, reviewers and agents cannot rely on the generated report package.

### Proposed Solution

Ensure summary/dashboard/report generation happens after final manifest status update, or regenerate summary after `logger.finish()` marks the run completed.

### Acceptance Criteria

- Completed runs show `completed` in manifest and summary.
- Failed runs show `failed` in manifest and summary.
- Test covers status consistency.

---

## [P1][template/helper] contest CV template

### Problem

Contest-style workflows repeatedly need CV split, OOF predictions, test predictions, fold metrics, and gated submission handling.

### Evidence

The mosquito alpha-test implemented these manually in the project runner.

### Proposed Solution

Add a `contest_cv` template or helper set.

### Acceptance Criteria

- Synthetic contest example runs end-to-end.
- OOF/test predictions are logged as typed artifacts.
- Fold metrics are logged as report-ready tables.
- Submission gate result is recorded even when no submission file is saved.

---

## [P1][helper] threshold-gated submission writer

### Problem

Submission files should only be saved when validation passes a threshold, but users currently implement this manually.

### Proposed API Sketch

```python
logger.log_submission(
    path=submission_path,
    score=score,
    threshold=0.70,
    mode="gte",
    role="contest_submission",
)
```

### Acceptance Criteria

- Below threshold: no submission artifact is copied, but gate result is recorded.
- Above threshold: submission artifact is saved and indexed.
- Report shows pass/fail gate status.

---

## [P1][artifact convention] OOF/test prediction bundle

### Problem

OOF and test predictions are core contest artifacts, but there is no standard artifact role convention.

### Proposed API Sketch

```python
logger.log_prediction_bundle(
    oof_pred=oof_pred,
    test_pred=test_pred,
    train_ids=train_ids,
    test_ids=test_ids,
    role="cv_predictions",
)
```

### Acceptance Criteria

- Artifact index records roles: `oof_prediction`, `test_prediction`, `train_ids`, `test_ids`.
- Report can display prediction bundle metadata.
- Agent can identify which artifact is safe for validation and which is final inference.

---

## [P1][feedback] richer alpha feedback schema

### Problem

Current alpha feedback can become repetitive boilerplate.

### Proposed Solution

Replace generic feedback lines with structured categories:

```text
API ergonomics
artifact convention gap
report evidence gap
dashboard evidence gap
agent handoff gap
template/helper candidate
```

### Acceptance Criteria

- Each run feedback includes at least one actionable backlog candidate.
- Feedback can be converted into JSON.
- Repeated boilerplate is reduced.

---

# 11. Recommended File Locations

For a test project:

```text
alpha-test-project/<project_name>/
  Feedback.md
  results/
    backlog/
      skilllog_alpha_feedback.md
      product_backlog.md
      agent_feedback.jsonl
```

For a run folder:

```text
run_dir/
  feedback.md
  agent/
    handoff.md
    handoff.json
```

Recommended usage:

```text
- Use `Feedback.md` as the global template.
- Use `results/backlog/skilllog_alpha_feedback.md` for chronological run feedback.
- Use `results/backlog/product_backlog.md` for deduplicated product backlog.
- Use `agent_feedback.jsonl` for machine-readable agent feedback events.
```
