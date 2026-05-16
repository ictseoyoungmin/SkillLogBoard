# physics_finite_diff_hit_tuned / 2026-05-17_02-01-33_physics_finite_diff_hit_tuned

## 가설
- `physics:finite_diff` can improve +80ms position prediction under R-Hit@1cm.

## 설계
- 5-fold random validation, train-only fitting, test used only for final inference.

## 결과
- `runtime/sec`: 0.909116
- `val/mean_dist`: 0.012933
- `val/median_dist`: 0.008168
- `val/p90_dist`: 0.027080
- `val/p95_dist`: 0.045006
- `val/r_hit@1cm`: 0.602600

## artifact 인사이트
- Inspect `predictions.npz`, fold metric tables, and distance quantiles before next run.

## 다음 실험
- Tune residual capacity, then enable ensemble only after a strong single model appears.

## SkillLog 좋았던 점
- TBD

## 불편한 점
- TBD

## 개선점
- TBD
