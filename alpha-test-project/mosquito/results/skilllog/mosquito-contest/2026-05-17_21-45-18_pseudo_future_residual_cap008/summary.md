# Run Summary

## Run

- Project: `mosquito-contest`
- Run: `pseudo_future_residual_cap008`
- Run ID: `2026-05-17_21-45-18_pseudo_future_residual_cap008`
- Status: `running`
- Created: `2026-05-17T21:45:19.259709+09:00`
- Updated: `2026-05-17T21:48:58.626242+09:00`

## Config


Full config: `config.yaml`

## Metrics

- Best metric: `val/r_hit@1cm` = `0.6497` at step `0` (max)

| Metric | Latest value | Step |
|---|---:|---:|
| `env/torch_cuda_available` | `1.0` | `0` |
| `model/median_best_epoch` | `6.0` | `0` |
| `model/pseudo_windows_per_sample` | `3.0` | `0` |
| `model/residual_cap` | `0.008` | `0` |
| `runtime/sec` | `238.01321836499847` | `0` |
| `val/fold_min_r_hit` | `0.637` | `0` |
| `val/mean_dist` | `0.011963674172288174` | `0` |
| `val/median_dist` | `0.007300985055070302` | `0` |
| `val/p90_dist` | `0.024686447973499868` | `0` |
| `val/p95_dist` | `0.04223158926078131` | `0` |
| `val/r_hit@1cm` | `0.6497` | `0` |

Metric files: `metrics.csv`, `events.jsonl`

## Artifacts

| Name | Type | Path | Mode |
|---|---|---|---|
| `oof_and_test_predictions` | `artifact` | `/mnt/f/NowWorking/SkillLogDashboard/alpha-test-project/mosquito/results/skilllog/mosquito-contest/2026-05-17_21-45-18_pseudo_future_residual_cap008/predictions.npz` | `reference` |
| `fold_metrics` | `table` | `tables/fold_metrics.csv` | `copy` |
| `experiment_backlog` | `artifact` | `artifacts/20260517_214859_2026-05-17_21-45-18_pseudo_future_residual_cap008_experiment.md` | `copy` |

## Files

- `manifest.yaml`
- `config.yaml`
- `metrics.csv`
- `events.jsonl`
- `artifact_index.json`
