# Run Summary

## Run

- Project: `mosquito-contest`
- Run: `pseudo_future_residual_cap006_noharm055`
- Run ID: `2026-05-17_21-50-23_pseudo_future_residual_cap006_noharm055`
- Status: `running`
- Created: `2026-05-17T21:50:24.209318+09:00`
- Updated: `2026-05-17T21:53:53.116685+09:00`

## Config


Full config: `config.yaml`

## Metrics

- Best metric: `val/r_hit@1cm` = `0.6504` at step `0` (max)

| Metric | Latest value | Step |
|---|---:|---:|
| `env/torch_cuda_available` | `1.0` | `0` |
| `model/median_best_epoch` | `6.0` | `0` |
| `model/pseudo_windows_per_sample` | `3.0` | `0` |
| `model/residual_cap` | `0.006` | `0` |
| `runtime/sec` | `225.2317219100005` | `0` |
| `val/fold_min_r_hit` | `0.64` | `0` |
| `val/mean_dist` | `0.012034072957892432` | `0` |
| `val/median_dist` | `0.007288121170517926` | `0` |
| `val/p90_dist` | `0.025097946630017142` | `0` |
| `val/p95_dist` | `0.04241079808294197` | `0` |
| `val/r_hit@1cm` | `0.6504` | `0` |

Metric files: `metrics.csv`, `events.jsonl`

## Artifacts

| Name | Type | Path | Mode |
|---|---|---|---|
| `oof_and_test_predictions` | `artifact` | `/mnt/f/NowWorking/SkillLogDashboard/alpha-test-project/mosquito/results/skilllog/mosquito-contest/2026-05-17_21-50-23_pseudo_future_residual_cap006_noharm055/predictions.npz` | `reference` |
| `fold_metrics` | `table` | `tables/fold_metrics.csv` | `copy` |
| `experiment_backlog` | `artifact` | `artifacts/20260517_215353_2026-05-17_21-50-23_pseudo_future_residual_cap006_noharm055_experiment.md` | `copy` |

## Files

- `manifest.yaml`
- `config.yaml`
- `metrics.csv`
- `events.jsonl`
- `artifact_index.json`
