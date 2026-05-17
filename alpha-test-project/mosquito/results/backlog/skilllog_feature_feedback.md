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
