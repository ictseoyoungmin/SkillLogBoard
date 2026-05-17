# Run Summary

## Run

- Project: `mosquito-contest`
- Run: `pseudo_future_residual_cap006`
- Run ID: `2026-05-17_21-39-34_pseudo_future_residual_cap006`
- Status: `running`
- Created: `2026-05-17T21:39:35.167991+09:00`
- Updated: `2026-05-17T21:43:19.372770+09:00`

## Config


Full config: `config.yaml`

## Metrics

- Best metric: `val/r_hit@1cm` = `0.6513` at step `0` (max)

| Metric | Latest value | Step |
|---|---:|---:|
| `env/torch_cuda_available` | `1.0` | `0` |
| `model/median_best_epoch` | `6.0` | `0` |
| `model/pseudo_windows_per_sample` | `3.0` | `0` |
| `model/residual_cap` | `0.006` | `0` |
| `runtime/sec` | `242.80143643299925` | `0` |
| `val/fold_min_r_hit` | `0.6395` | `0` |
| `val/mean_dist` | `0.012028083370537505` | `0` |
| `val/median_dist` | `0.007285416506733127` | `0` |
| `val/p90_dist` | `0.025086911908026796` | `0` |
| `val/p95_dist` | `0.04215941375909202` | `0` |
| `val/r_hit@1cm` | `0.6513` | `0` |

Metric files: `metrics.csv`, `events.jsonl`

## Artifacts

| Name | Type | Path | Mode |
|---|---|---|---|
| `oof_and_test_predictions` | `artifact` | `/mnt/f/NowWorking/SkillLogDashboard/alpha-test-project/mosquito/results/skilllog/mosquito-contest/2026-05-17_21-39-34_pseudo_future_residual_cap006/predictions.npz` | `reference` |
| `fold_metrics` | `table` | `tables/fold_metrics.csv` | `copy` |
| `experiment_backlog` | `artifact` | `artifacts/20260517_214321_2026-05-17_21-39-34_pseudo_future_residual_cap006_experiment.md` | `copy` |

## Files

- `manifest.yaml`
- `config.yaml`
- `metrics.csv`
- `events.jsonl`
- `artifact_index.json`
