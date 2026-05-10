# SkillLogBoard

Portable experiment logging and dashboard package for local-first ML research.

## Current MVP

SkillLogBoard creates local experiment evidence packages, static dashboards, rule audit traces,
and multi-run comparison reports:

- installable `src/skilllogboard` package
- `RunLogger` lifecycle: running, completed, failed
- metrics CSV and event JSONL logging
- config/system/git snapshots
- artifact, image-path, and table logging
- `summary.md` and single-run `dashboard.html`
- Skills.md v0.3 MVP rule checks with `skill_trace.jsonl`
- v0.4 multi-run compare outputs: `compare.csv`, `compare.md`, and `compare.html`
- CLI `init`, `inspect`, `report`, and `dashboard`
- CLI `compare` and `export-table`

## Install

```bash
pip install -e ".[dev,dashboard]"
```

## CLI

```bash
skilllog --help
skilllog init
skilllog inspect runs/demo/<run_id>
skilllog compare runs/demo --metric val/acc --mode max --output-dir runs/demo/compare
skilllog export-table runs/demo --metric val/acc --format md --output runs/demo/compare.md
```

## Smoke Test

```bash
python examples/basic_usage.py
```

The example writes a run folder under `runs/demo/<run_id>/`, where `<run_id>` is generated from
the run name and timestamp:

```text
manifest.yaml
config.yaml
system.json
git.json
metrics.csv
events.jsonl
artifact_index.json
summary.md
dashboard.html
skill_trace.jsonl
artifacts/
```

Open the generated dashboard directly from the run folder:

```bash
# Replace <run_id> with the path printed by the example.
python examples/basic_usage.py
# then open runs/demo/<run_id>/dashboard.html in your browser
```

## Minimal Usage

```python
from skilllogboard import RunLogger

logger = RunLogger(
    project="demo",
    run_name="baseline",
    config={"model_name": "TinyNet", "seed": 42, "lr": 1e-3},
    main_metric={"name": "val/acc", "mode": "max"},
)

logger.log_metrics({"train/loss": 1.0, "val/acc": 0.8}, step=0)
logger.log_note("baseline run")
logger.run_skill_checks(skills_path="Skills.md")
logger.finish(build_dashboard=True, build_report=True)
```

## v0.3 Skills.md Rule Engine

Skills.md rule blocks are parsed and executed for MVP rule types:

- `required_config`
- `required_metric`
- `metric_threshold`
- `best_last_gap`
- `artifact_required`

Rule results are written to `skill_trace.jsonl` and displayed in the dashboard Rule Audit section.
Planned rule types such as `dashboard_panel` and `domain_breakdown` are parsed as planned/skipped
metadata and are not executed as MVP checks.

## v0.4 Multi-run Compare

Compare existing run folders under a runs root:

```bash
skilllog compare runs/demo --metric val/acc --mode max --output-dir runs/demo/compare
```

This writes:

```text
compare.csv
compare.md
compare.html
```

Export leaderboard tables for reports:

```bash
skilllog export-table runs/demo --metric val/acc --format csv --output compare.csv
skilllog export-table runs/demo --metric val/acc --format md --output compare.md
skilllog export-table runs/demo --metric val/acc --format latex --output compare.tex
```

Compare includes a leaderboard, config diff, inferred ablation axes, and seed summary. Research
templates build on these static outputs without adding mandatory domain dependencies.

## v0.5 Research Templates

List lightweight research templates:

```bash
skilllog templates
```

Initialize dependency-free template files:

```bash
skilllog init --template ir-drop
skilllog init --template trajectory
python examples/ir_drop_example.py
python examples/trajectory_example.py
python examples/sklearn_example.py
```

Implemented templates are `ir-drop` and `trajectory`. Planned templates are `classification`,
`segmentation`, and `finance-dashboard`. Optional integrations remain optional; core install does
not require torch, lightning, sklearn, pandas, or domain-specific packages.

The `ir-drop` template uses synthetic data and the metric convention `train/loss`, `val/mae`,
`val/high_drop_f1`, and `val/raw_mae`; it does not include a model or private dataset.
The `trajectory` template uses synthetic values and the metric convention `train/loss`,
`val/loss`, `val/pb_score`, and `val/endpoint_error`; model training is user-provided.
The `sklearn_example.py` file is a core `RunLogger` usage example with sklearn-style metrics, not
a required scikit-learn adapter.

## Troubleshooting

- If `pytest` is missing, install the dev extras: `pip install -e ".[dev,dashboard]"`.
- If `skilllog` is not found, activate the virtual environment or reinstall with `pip install -e .`.
- Generated local runs are written to `runs/`, which is ignored by git.
- Skills.md v0.3 executes MVP rules and records results in `skill_trace.jsonl`.

## Development Priority

1. Keep the run folder schema stable.
2. Keep core logger framework-agnostic.
3. Keep research plugins separate from the core compare/dashboard MVP.
