# SkillLogBoard Feature Feedback From Mosquito Alpha Test

## RunLogger

- 좋았던 점: config, metrics, artifacts, dashboard, summary가 한 run 폴더에 모여서 실험 증거 패키지를 만들기 쉽다.
- 불편한 점: fold별 OOF prediction, submission gate, leaderboard threshold 같은 contest 규칙은 사용자가 직접 convention을 만들어야 한다.
- 개선점: `RunLogger`에 `log_fold_metrics`, `log_predictions`, `log_gated_submission` 같은 경량 helper가 있으면 contest alpha-test가 빨라진다.

## Project Index

- 좋았던 점: `index rebuild`가 run_count와 metric summary를 빠르게 재구성해서 Live Board/검색 기반이 된다.
- 불편한 점: `--json` 출력이 매우 길어서 터미널에서는 핵심 best metric을 찾기 어렵다.
- 개선점: `--compact` 또는 `--metric val/r_hit@1cm` 옵션으로 run_id, status, key metric만 출력하면 좋다.

## Runs List

- 좋았던 점: `status:completed` 필터로 완료 run만 빠르게 확인할 수 있다.
- 불편한 점: tree 계열을 pass하려고 할 때 tag exclude 필터가 명확하지 않아 이미 생성된 tree run까지 함께 보인다.
- 개선점: `--filter "not tag:extra-trees not tag:lightgbm"` 같은 negative tag filter가 있으면 후속 실험 관리가 편하다.

## Compare

- 좋았던 점: `compare`가 같은 metric 기준으로 `csv/md/html`을 한 번에 만들고 leaderboard를 즉시 확인할 수 있다.
- 불편한 점: output에 전체 leaderboard가 먼저 크게 출력되어 자동화 로그가 길어진다.
- 개선점: `--quiet`, `--top-k`, `--filter` 옵션을 compare에도 직접 제공하면 좋다.

## Export Table

- 좋았던 점: leaderboard/config-diff를 md로 바로 뽑아 backlog에 붙이기 좋다.
- 불편한 점: contest 관점의 best-only 요약, submission gate 상태, model family group이 기본 테이블에는 없다.
- 개선점: `--columns` 또는 contest preset table을 제공하면 재설계 문서 작성이 쉬워진다.

## Report Build And Validate

- 좋았던 점: `report build --render-mode package`와 `report validate --json`으로 오프라인 HTML, 표, figure 존재 여부를 검증할 수 있다.
- 불편한 점: matplotlib cache dir 권한 경고가 나왔고, 실험 환경 진단 정보가 report에 자동 포함되지는 않는다.
- 개선점: `skilllog doctor` 결과와 GPU/패키지 smoke artifact를 report manifest에 자동 포함하는 옵션이 있으면 좋다.

## Live Board Follow-Up

- 좋았던 점: 이번 산출물 구조는 Live Board project mode로 바로 열 수 있다.
- 불편한 점: 많은 run에서 tree/pass 같은 실험 중단 의도를 UI 필터로 바로 표현하기 어렵다.
- 개선점: tag include/exclude, submission-ready gate, best non-tree view 같은 contest workflow filter가 필요하다.

## Reference-Guided Research Sweep 2026-05-17

- 사용 기능: `RunLogger`, artifact logging, table logging, `index rebuild`, `runs list`, `compare`, `export-table`, `report build`, `report validate`, `inspect`.
- 좋았던 점: pseudo-future residual 4개 실험을 같은 convention으로 기록하니 `compare.md`, `leaderboard.md`, `report.html`이 곧바로 연구 회의 자료가 되었다.
- 좋았던 점: fold table artifact가 있어 cap sweep 결과를 단일 점수뿐 아니라 fold-3 약점, base-anchor hit, best epoch까지 같이 볼 수 있었다.
- 좋았던 점: `report validate --json`이 오프라인 HTML/표/figure 존재를 기계적으로 확인해 주어 산출물 누락 여부를 빠르게 판단했다.
- 불편한 점: `index rebuild --json`과 `runs list --json` 출력이 너무 길어 agent loop에서 best run만 확인하기 어렵다.
- 불편한 점: `summary.md`가 일시적으로 `running` 상태를 보여 주었고 `manifest.yaml`은 `completed`여서, final evidence를 볼 때 어떤 파일을 신뢰해야 하는지 혼란이 생겼다.
- 불편한 점: submission gate 미통과가 report/leaderboard에서 명시되지 않아, submission 폴더가 비어 있는 것이 정상인지 실패인지 바로 알 수 없다.
- 불편한 점: `predictions.npz` 내부의 `oof_pred`, `test_pred`, `train_ids`, `test_ids` 역할은 코드 convention을 알아야 이해된다.
- 불편한 점: report의 `Key Findings`가 TODO로 남아 있어, 이미 있는 leaderboard delta를 사람이 다시 요약해야 한다.
- 불편한 점: `report build`에서 matplotlib cache dir 권한 경고가 반복되어, WSL/sandbox 환경에서는 기본 cache 경로를 자동 우회하면 좋겠다.
- 개선점: `RunLogger.log_submission_gate(metric, threshold, passed, path=None)` helper를 추가하면 contest workflow가 훨씬 명확해진다.
- 개선점: artifact role metadata에 `role=oof_prediction`, `role=test_prediction`, `role=fold_metrics`, `role=submission_candidate` 같은 값을 넣을 수 있으면 Live Board/Report에서 해석이 쉬워진다.
- 개선점: `skilllog compare --top-k 5 --include-tags torch,pseudo-future --exclude-tags lightgbm,extra-trees` 같은 필터가 필요하다.
- 개선점: report generator가 best run, second-best, delta, warning, submission gate를 자동 findings draft로 만들어 주면 agent handoff 품질이 올라간다.
- 개선점: rule audit에 `test_data_policy`, `submission_threshold`, `fold_count`, `main_metric_mode` 같은 프로젝트 규칙을 등록하고 pass/fail을 채우는 API가 필요하다.
