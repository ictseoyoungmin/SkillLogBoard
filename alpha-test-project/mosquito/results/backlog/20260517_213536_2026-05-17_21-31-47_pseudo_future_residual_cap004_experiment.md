# pseudo_future_residual_cap004 / 2026-05-17_21-31-47_pseudo_future_residual_cap004

## 가설
- `pseudo_future_residual:ca_last_beta_0.25:cap0.004:device=NVIDIA GeForce GTX 1660` can improve +80ms position prediction under R-Hit@1cm.

## 설계
- 5-fold random validation, train-only fitting, test used only for final inference.

## 결과
- `env/torch_cuda_available`: 1.000000
- `model/median_best_epoch`: 7.000000
- `model/pseudo_windows_per_sample`: 3.000000
- `model/residual_cap`: 0.004000
- `runtime/sec`: 246.852464
- `val/fold_min_r_hit`: 0.635000
- `val/mean_dist`: 0.012148
- `val/median_dist`: 0.007326
- `val/p90_dist`: 0.025527
- `val/p95_dist`: 0.042799
- `val/r_hit@1cm`: 0.650600

## artifact 인사이트
- Inspect `predictions.npz`, fold metric tables, and distance quantiles before next run.

## 다음 실험
- Tune residual capacity, then enable ensemble only after a strong single model appears.

## SkillLog 좋았던 점
- Fold metrics table, predictions artifact, config snapshot, and manifest were enough to reproduce the reference-style evidence package inside the local SkillLog framework.

## 불편한 점
- Submission gate failure is only visible through notes and the empty submissions folder; the report/leaderboard does not show `submission_ready=false`.

## 개선점
- Add first-class submission gate metadata and prediction artifact role metadata to avoid contest-specific conventions living only in runner code.
