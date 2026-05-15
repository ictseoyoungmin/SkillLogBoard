# SkillLogBoard ReportSpec: Baseline Delta

## TABLE-LEADERBOARD
- type: leaderboard
- metric: val/acc
- mode: max
- baseline_run_id: baseline
- reference_run_id: candidate
- delta_mode: absolute
- output: tables/leaderboard.md

## TABLE-SEED-SUMMARY
- type: seed-summary
- metric: val/acc
- mode: max
- group_by: [model]
- output: tables/seed-summary.md

## FIG-CURVE
- type: metric-curve-overlay
- metric: val/acc
- output: figures/val-acc-overlay.png
