# pseudo_future_residual_cap006_noharm055 / 2026-05-17_21-50-23_pseudo_future_residual_cap006_noharm055

## 가설
- `pseudo_future_residual:ca_last_beta_0.25:cap0.006:device=NVIDIA GeForce GTX 1660` can improve +80ms position prediction under R-Hit@1cm.

## 설계
- 5-fold random validation, train-only fitting, test used only for final inference.

## 결과
- `env/torch_cuda_available`: 1.000000
- `model/median_best_epoch`: 6.000000
- `model/pseudo_windows_per_sample`: 3.000000
- `model/residual_cap`: 0.006000
- `runtime/sec`: 225.231722
- `val/fold_min_r_hit`: 0.640000
- `val/mean_dist`: 0.012034
- `val/median_dist`: 0.007288
- `val/p90_dist`: 0.025098
- `val/p95_dist`: 0.042411
- `val/r_hit@1cm`: 0.650400

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
