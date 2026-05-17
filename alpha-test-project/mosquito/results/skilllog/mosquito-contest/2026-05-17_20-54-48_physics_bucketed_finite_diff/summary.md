# Run Summary

## Run

- Project: `mosquito-contest`
- Run: `physics_bucketed_finite_diff`
- Run ID: `2026-05-17_20-54-48_physics_bucketed_finite_diff`
- Status: `running`
- Created: `2026-05-17T20:54:48.969033+09:00`
- Updated: `2026-05-17T20:55:30.658481+09:00`

## Config


Full config: `config.yaml`

## Metrics

- Best metric: `val/r_hit@1cm` = `0.6011` at step `0` (max)

| Metric | Latest value | Step |
|---|---:|---:|
| `runtime/sec` | `46.182042163000006` | `0` |
| `val/fold_min_r_hit` | `0.5865` | `0` |
| `val/mean_dist` | `0.01285362155367234` | `0` |
| `val/median_dist` | `0.008098233438510766` | `0` |
| `val/p90_dist` | `0.026941575888534856` | `0` |
| `val/p95_dist` | `0.04431739161915137` | `0` |
| `val/r_hit@1cm` | `0.6011` | `0` |

Metric files: `metrics.csv`, `events.jsonl`

## Artifacts

| Name | Type | Path | Mode |
|---|---|---|---|
| `oof_and_test_predictions` | `artifact` | `/mnt/f/NowWorking/SkillLogDashboard/alpha-test-project/mosquito/results/skilllog/mosquito-contest/2026-05-17_20-54-48_physics_bucketed_finite_diff/predictions.npz` | `reference` |
| `fold_metrics` | `table` | `tables/fold_metrics.csv` | `copy` |
| `experiment_backlog` | `artifact` | `artifacts/20260517_205531_2026-05-17_20-54-48_physics_bucketed_finite_diff_experiment.md` | `copy` |

## Files

- `manifest.yaml`
- `config.yaml`
- `metrics.csv`
- `events.jsonl`
- `artifact_index.json`
