# Run Summary

## Run

- Project: `mosquito-contest`
- Run: `jepa_torch_residual`
- Run ID: `2026-05-17_20-22-05_jepa_torch_residual`
- Status: `running`
- Created: `2026-05-17T20:22:05.950928+09:00`
- Updated: `2026-05-17T20:25:49.048359+09:00`

## Config


Full config: `config.yaml`

## Metrics

- Best metric: `val/r_hit@1cm` = `0.4847` at step `0` (max)

| Metric | Latest value | Step |
|---|---:|---:|
| `env/torch_cuda_available` | `1.0` | `0` |
| `runtime/sec` | `243.87209815699998` | `0` |
| `val/fold_min_r_hit` | `0.4335` | `0` |
| `val/mean_dist` | `0.014607698356557368` | `0` |
| `val/median_dist` | `0.010226068052170027` | `0` |
| `val/p90_dist` | `0.026347744038846207` | `0` |
| `val/p95_dist` | `0.04350335686429072` | `0` |
| `val/r_hit@1cm` | `0.4847` | `0` |

Metric files: `metrics.csv`, `events.jsonl`

## Artifacts

| Name | Type | Path | Mode |
|---|---|---|---|
| `oof_and_test_predictions` | `artifact` | `/mnt/f/NowWorking/SkillLogDashboard/alpha-test-project/mosquito/results/skilllog/mosquito-contest/2026-05-17_20-22-05_jepa_torch_residual/predictions.npz` | `reference` |
| `fold_metrics` | `table` | `tables/fold_metrics.csv` | `copy` |
| `experiment_backlog` | `artifact` | `artifacts/20260517_202549_2026-05-17_20-22-05_jepa_torch_residual_experiment.md` | `copy` |

## Files

- `manifest.yaml`
- `config.yaml`
- `metrics.csv`
- `events.jsonl`
- `artifact_index.json`
