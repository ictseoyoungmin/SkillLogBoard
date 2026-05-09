# Changelog

## 0.4.0-dev compare candidate

- Added Week 5 multi-run run discovery and manifest/config/metric indexing.
- Added compare leaderboard, config diff, ablation axis extraction, and seed summary helpers.
- Added static `compare.csv`, `compare.md`, and `compare.html` report generation.
- Added working `skilllog compare` and `skilllog export-table` commands.

## 0.3.0-dev rule engine candidate

- Added Week 4 Skills.md RULE block parser and RuleSpec/RuleResult schema.
- Added MVP rules: required_config, required_metric, metric_threshold, best_last_gap, artifact_required.
- Added RuleEngine execution, `skill_trace.jsonl` logging, `RunLogger.run_skill_checks`, and dashboard Rule Audit.

## v0.2 dashboard candidate

- Added Week 3 static single-run dashboard, dashboard data loaders, CLI refinements, packaging checks, and dashboard smoke tests.

## v0.1 MVP

- Initial Week 1 project skeleton.
- Added package layout, CLI placeholder, manifest/event/writer placeholders.
- Added Week 2 v0.1 MVP RunLogger lifecycle, metric/config logging, artifact/image/table logging, summary generation, and integration tests.
