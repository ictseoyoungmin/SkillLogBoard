# SkillLogBoard v0.6 Release-Hardening Candidate

This is a release-hardening candidate, not a published PyPI release.

## Implemented Capabilities

- `RunLogger` records local experiment evidence with manifest, config, metrics, events, artifacts,
  summary reports, and static dashboards.
- Static single-run `dashboard.html` rendering includes run summary, metrics, config, artifacts,
  files, and rule audit output.
- Skills.md MVP rule engine supports required config, required metric, metric threshold,
  best-last gap, and artifact-required checks.
- Multi-run compare generates leaderboard, config diff, ablation axes, seed summary, and static
  `compare.csv`, `compare.md`, and `compare.html` outputs.
- Research templates include implemented lightweight `ir-drop` and `trajectory` starters.
- Optional integrations for PyTorch and Lightning are lazy/guarded; core install remains
  dependency-light.

## CLI Commands

```text
skilllog init
skilllog templates
skilllog inspect RUN_DIR
skilllog dashboard RUN_DIR
skilllog report RUN_DIR
skilllog compare RUNS_DIR --metric METRIC
skilllog export-table RUNS_DIR --metric METRIC --format csv|md|latex --output PATH
```

## Examples

```bash
python examples/basic_usage.py
python examples/ir_drop_example.py
python examples/trajectory_example.py
python examples/sklearn_example.py
```

## Known Limitations

- Planned templates `classification`, `segmentation`, and `finance-dashboard` are not implemented.
- Planned rule metadata such as `dashboard_panel` and `domain_breakdown` is parsed but not executed
  as MVP rule logic.
- No online dashboard, database backend, W&B/TensorBoard import, or real-time server is included.
- PyTorch, Lightning, pandas/table workflows, and domain-specific tooling remain optional and
  user-provided.
- Isolated package builds should pass in CI or Docker before publishing.

## Release Verification

Use `docs/release_checklist.md` for the release candidate checklist. Do not publish to PyPI or
create a GitHub release until the release decision record is complete.
