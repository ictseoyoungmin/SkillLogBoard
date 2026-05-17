# Run Summary

## Run

- Project: `mosquito-contest`
- Run: `residual_knn_cv_last1`
- Run ID: `2026-05-17_20-28-06_residual_knn_cv_last1`
- Status: `running`
- Created: `2026-05-17T20:28:07.096385+09:00`
- Updated: `2026-05-17T20:28:14.212956+09:00`

## Config


Full config: `config.yaml`

## Metrics

- Best metric: `val/r_hit@1cm` = `0.5984` at step `0` (max)

| Metric | Latest value | Step |
|---|---:|---:|
| `runtime/sec` | `6.30415882699981` | `0` |
| `val/fold_min_r_hit` | `0.582` | `0` |
| `val/mean_dist` | `0.012615169050485013` | `0` |
| `val/median_dist` | `0.008224404961898732` | `0` |
| `val/p90_dist` | `0.02570881552931789` | `0` |
| `val/p95_dist` | `0.04242897290275999` | `0` |
| `val/r_hit@1cm` | `0.5984` | `0` |

Metric files: `metrics.csv`, `events.jsonl`

## Artifacts

| Name | Type | Path | Mode |
|---|---|---|---|
| `oof_and_test_predictions` | `artifact` | `/mnt/f/NowWorking/SkillLogDashboard/alpha-test-project/mosquito/results/skilllog/mosquito-contest/2026-05-17_20-28-06_residual_knn_cv_last1/predictions.npz` | `reference` |
| `fold_metrics` | `table` | `tables/fold_metrics.csv` | `copy` |
| `experiment_backlog` | `artifact` | `artifacts/20260517_202814_2026-05-17_20-28-06_residual_knn_cv_last1_experiment.md` | `copy` |

## Files

- `manifest.yaml`
- `config.yaml`
- `metrics.csv`
- `events.jsonl`
- `artifact_index.json`
