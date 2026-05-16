# Run Summary

## Run

- Project: `mosquito-contest`
- Run: `residual_extra_trees_cv_last1`
- Run ID: `2026-05-17_02-02-01_residual_extra_trees_cv_last1`
- Status: `running`
- Created: `2026-05-17T02:02:01.911672+09:00`
- Updated: `2026-05-17T02:03:11.397280+09:00`

## Config


Full config: `config.yaml`

## Metrics

- Best metric: `val/r_hit@1cm` = `0.6075` at step `0` (max)

| Metric | Latest value | Step |
|---|---:|---:|
| `runtime/sec` | `74.32569527099986` | `0` |
| `val/fold_min_r_hit` | `0.5965` | `0` |
| `val/mean_dist` | `0.012241444451748629` | `0` |
| `val/median_dist` | `0.007952689682417805` | `0` |
| `val/p90_dist` | `0.02517136540598614` | `0` |
| `val/p95_dist` | `0.040022209436527574` | `0` |
| `val/r_hit@1cm` | `0.6075` | `0` |

Metric files: `metrics.csv`, `events.jsonl`

## Artifacts

| Name | Type | Path | Mode |
|---|---|---|---|
| `oof_and_test_predictions` | `artifact` | `/mnt/f/NowWorking/SkillLogDashboard/alpha-test-project/mosquito/results/skilllog/mosquito-contest/2026-05-17_02-02-01_residual_extra_trees_cv_last1/predictions.npz` | `reference` |
| `fold_metrics` | `table` | `tables/fold_metrics.csv` | `copy` |
| `experiment_backlog` | `artifact` | `artifacts/20260517_020312_2026-05-17_02-02-01_residual_extra_trees_cv_last1_experiment.md` | `copy` |

## Files

- `manifest.yaml`
- `config.yaml`
- `metrics.csv`
- `events.jsonl`
- `artifact_index.json`
