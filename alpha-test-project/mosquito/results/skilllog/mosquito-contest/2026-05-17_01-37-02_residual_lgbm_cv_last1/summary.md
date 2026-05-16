# Run Summary

## Run

- Project: `mosquito-contest`
- Run: `residual_lgbm_cv_last1`
- Run ID: `2026-05-17_01-37-02_residual_lgbm_cv_last1`
- Status: `running`
- Created: `2026-05-17T01:37:02.374685+09:00`
- Updated: `2026-05-17T01:39:41.382711+09:00`

## Config


Full config: `config.yaml`

## Metrics

- Best metric: `val/r_hit@1cm` = `0.5814` at step `0` (max)

| Metric | Latest value | Step |
|---|---:|---:|
| `runtime/sec` | `172.71166187600102` | `0` |
| `val/fold_min_r_hit` | `0.566` | `0` |
| `val/mean_dist` | `0.012724523589157955` | `0` |
| `val/median_dist` | `0.008392567179344368` | `0` |
| `val/p90_dist` | `0.02656780751733983` | `0` |
| `val/p95_dist` | `0.039847839273924116` | `0` |
| `val/r_hit@1cm` | `0.5814` | `0` |

Metric files: `metrics.csv`, `events.jsonl`

## Artifacts

| Name | Type | Path | Mode |
|---|---|---|---|
| `oof_and_test_predictions` | `artifact` | `/mnt/f/NowWorking/SkillLogDashboard/alpha-test-project/mosquito/results/skilllog/mosquito-contest/2026-05-17_01-37-02_residual_lgbm_cv_last1/predictions.npz` | `reference` |
| `fold_metrics` | `table` | `tables/fold_metrics.csv` | `copy` |
| `experiment_backlog` | `artifact` | `artifacts/20260517_013942_2026-05-17_01-37-02_residual_lgbm_cv_last1_experiment.md` | `copy` |

## Files

- `manifest.yaml`
- `config.yaml`
- `metrics.csv`
- `events.jsonl`
- `artifact_index.json`
