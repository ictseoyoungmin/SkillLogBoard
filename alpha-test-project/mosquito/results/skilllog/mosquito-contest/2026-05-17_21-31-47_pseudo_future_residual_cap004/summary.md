# Run Summary

## Run

- Project: `mosquito-contest`
- Run: `pseudo_future_residual_cap004`
- Run ID: `2026-05-17_21-31-47_pseudo_future_residual_cap004`
- Status: `running`
- Created: `2026-05-17T21:31:47.474878+09:00`
- Updated: `2026-05-17T21:35:35.871323+09:00`

## Config


Full config: `config.yaml`

## Metrics

- Best metric: `val/r_hit@1cm` = `0.6506` at step `0` (max)

| Metric | Latest value | Step |
|---|---:|---:|
| `env/torch_cuda_available` | `1.0` | `0` |
| `model/median_best_epoch` | `7.0` | `0` |
| `model/pseudo_windows_per_sample` | `3.0` | `0` |
| `model/residual_cap` | `0.004` | `0` |
| `runtime/sec` | `246.85246445700068` | `0` |
| `val/fold_min_r_hit` | `0.635` | `0` |
| `val/mean_dist` | `0.012147714458219851` | `0` |
| `val/median_dist` | `0.00732597893678622` | `0` |
| `val/p90_dist` | `0.025526836587893814` | `0` |
| `val/p95_dist` | `0.042799383518918065` | `0` |
| `val/r_hit@1cm` | `0.6506` | `0` |

Metric files: `metrics.csv`, `events.jsonl`

## Artifacts

| Name | Type | Path | Mode |
|---|---|---|---|
| `oof_and_test_predictions` | `artifact` | `/mnt/f/NowWorking/SkillLogDashboard/alpha-test-project/mosquito/results/skilllog/mosquito-contest/2026-05-17_21-31-47_pseudo_future_residual_cap004/predictions.npz` | `reference` |
| `fold_metrics` | `table` | `tables/fold_metrics.csv` | `copy` |
| `experiment_backlog` | `artifact` | `artifacts/20260517_213536_2026-05-17_21-31-47_pseudo_future_residual_cap004_experiment.md` | `copy` |

## Files

- `manifest.yaml`
- `config.yaml`
- `metrics.csv`
- `events.jsonl`
- `artifact_index.json`
