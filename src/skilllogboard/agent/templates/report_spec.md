# ReportSpec

## TABLE-LEADERBOARD
- type: leaderboard
- metric: val/acc
- mode: max
- output: report/tables/leaderboard.md

## TABLE-RULE-AUDIT
- type: rule-audit
- output: report/tables/rule_audit.md

## FIG-METRIC-CURVE
- type: metric-curve-overlay
- metric: val/acc
- output: report/figures/metric_curve_overlay.png
