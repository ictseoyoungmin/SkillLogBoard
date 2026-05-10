# Changelog

## 0.6.0-dev release hardening candidate

- Started Week 7 release hardening for packaging metadata, optional extras, build verification, CI, and release documentation.
- Normalized package version metadata for the v0.6 candidate.
- Added package-data and optional-dependency verification coverage.
- Added release checklist, release notes draft, smoke scripts, wheel install verification, and optional Docker test file.

## 0.5.0-dev research templates candidate

- Added dependency-free research template descriptors and registry.
- Added `skilllog templates` and `skilllog init --template` for implemented/planned templates.
- Added implemented `ir-drop` and `trajectory` templates with default configs and Skills.md rules.
- Added synthetic IR-drop, trajectory, and sklearn-style examples plus smoke tests.
- Added optional PyTorch and Lightning helper skeletons with lazy imports.

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
