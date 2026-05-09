# SkillLogBoard Default Skills

These are starter rule definitions for Skills.md validation. MVP rules execute
in v0.3; Planned rules parse but are reported as planned/skipped.

## RULE-CONFIG-001
- type: required_config
- keys: [model_name, dataset_name, seed, optimizer, lr, batch_size]
- severity: warning
- status: MVP
- message: Core reproducibility config should be logged.

## RULE-METRIC-001
- type: required_metric
- keys: [train/loss, val/acc]
- severity: warning
- status: MVP
- message: Core training and validation metrics should be logged.

## RULE-METRIC-THRESHOLD-001
- type: metric_threshold
- metric: val/acc
- threshold: 0.0
- mode: max
- severity: warning
- status: MVP
- message: Validation accuracy should be logged as a numeric metric.

## RULE-BEST-LAST-001
- type: best_last_gap
- metric: val/acc
- threshold: 0.25
- mode: max
- severity: warning
- status: MVP
- message: Best and last validation accuracy should stay reasonably close.

## RULE-ARTIFACT-001
- type: artifact_required
- artifacts: [example_artifact]
- severity: warning
- status: MVP
- message: Example artifact should be present when using the default demo.

## RULE-DASHBOARD-PANEL-001
- type: dashboard_panel
- keys: [loss_curve, metric_curve, config_table, artifact_links]
- severity: info
- status: Planned
- message: Dashboard panel rules are planned for a later release.

## RULE-DOMAIN-001
- type: domain_breakdown
- keys: [train, val, test]
- severity: info
- status: Planned
- message: Domain breakdown rules are planned for research templates.
