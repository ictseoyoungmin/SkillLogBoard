# SkillLogBoard ReportSpec: Offline Package

## REPORT-MAIN
- title: Offline Evidence Package
- render_mode: package
- output: report.md

## TABLE-ABLATION
- type: ablation-summary
- metric: val/acc
- mode: max
- output: tables/ablation-summary.md

## TABLE-RULE-AUDIT
- type: rule-audit
- output: tables/rule-audit.md
