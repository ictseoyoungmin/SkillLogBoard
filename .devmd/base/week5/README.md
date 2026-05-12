# Week 5 — Multi-run Compare and Ablation Export

Week 5 implements v0.4 multi-run comparison.

## Target Outputs

- `compare.csv`
- `compare.md`
- `compare.html`
- leaderboard table
- config diff table
- ablation axis summary
- seed group summary

## CLI Targets

- `skilllog compare RUNS_DIR --metric <metric>`
- `skilllog export-table RUNS_DIR --metric <metric> --format csv|md|latex`

## Scope Boundary

Allowed:
- run discovery
- manifest/metrics/config aggregation
- leaderboard
- config diff
- ablation grouping
- seed mean/std
- static compare dashboard
- CSV/Markdown/LaTeX-like table export

Not allowed:
- online dashboards
- database backend
- W&B import
- IR-drop/trajectory plugins
