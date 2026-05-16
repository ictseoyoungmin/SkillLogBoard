# Run Summary

## Run

- Project: `mosquito-contest`
- Run: `physics_finite_diff_hit_tuned`
- Run ID: `2026-05-17_02-01-33_physics_finite_diff_hit_tuned`
- Status: `running`
- Created: `2026-05-17T02:01:33.736028+09:00`
- Updated: `2026-05-17T02:01:34.721945+09:00`

## Config


Full config: `config.yaml`

## Metrics

- Best metric: `val/r_hit@1cm` = `0.6026` at step `0` (max)

| Metric | Latest value | Step |
|---|---:|---:|
| `runtime/sec` | `0.9091158039991569` | `0` |
| `val/mean_dist` | `0.0129333321525475` | `0` |
| `val/median_dist` | `0.008168408483851534` | `0` |
| `val/p90_dist` | `0.02708003854735572` | `0` |
| `val/p95_dist` | `0.04500615333735512` | `0` |
| `val/r_hit@1cm` | `0.6026` | `0` |

Metric files: `metrics.csv`, `events.jsonl`

## Artifacts

| Name | Type | Path | Mode |
|---|---|---|---|
| `oof_and_test_predictions` | `artifact` | `/mnt/f/NowWorking/SkillLogDashboard/alpha-test-project/mosquito/results/skilllog/mosquito-contest/2026-05-17_02-01-33_physics_finite_diff_hit_tuned/predictions.npz` | `reference` |
| `fold_metrics` | `table` | `tables/fold_metrics.csv` | `copy` |
| `experiment_backlog` | `artifact` | `artifacts/20260517_020135_2026-05-17_02-01-33_physics_finite_diff_hit_tuned_experiment.md` | `copy` |

## Files

- `manifest.yaml`
- `config.yaml`
- `metrics.csv`
- `events.jsonl`
- `artifact_index.json`
