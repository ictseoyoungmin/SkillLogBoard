# physics_bucketed_finite_diff / 2026-05-17_20-54-48_physics_bucketed_finite_diff

## 가설
- `physics:bucketed_finite_diff` can improve +80ms position prediction under R-Hit@1cm.

## 설계
- 5-fold random validation, train-only fitting, test used only for final inference.

## 결과
- `runtime/sec`: 46.182042
- `val/fold_min_r_hit`: 0.586500
- `val/mean_dist`: 0.012854
- `val/median_dist`: 0.008098
- `val/p90_dist`: 0.026942
- `val/p95_dist`: 0.044317
- `val/r_hit@1cm`: 0.601100

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
