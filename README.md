# SkillLogBoard

Portable experiment logging and dashboard package for local-first ML research.

## v0.2 Static Dashboard MVP

SkillLogBoard v0.2 creates a local single-run evidence package and a static dashboard:

- installable `src/skilllogboard` package
- `RunLogger` lifecycle: running, completed, failed
- metrics CSV and event JSONL logging
- config/system/git snapshots
- artifact, image-path, and table logging
- `summary.md` and single-run `dashboard.html`
- CLI `init`, `inspect`, `report`, and `dashboard`

## Install

```bash
pip install -e ".[dev,dashboard]"
```

## CLI

```bash
skilllog --help
skilllog init
skilllog inspect runs/demo/latest
```

## Smoke Test

```bash
python examples/basic_usage.py
```

The example writes a run folder under `runs/demo/<run_id>/` with:

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
logger.finish(build_dashboard=True, build_report=True)
```

## Troubleshooting

- If `pytest` is missing, install the dev extras: `pip install -e ".[dev,dashboard]"`.
- If `skilllog` is not found, activate the virtual environment or reinstall with `pip install -e .`.
- Generated local runs are written to `runs/`, which is ignored by git.
- `skilllog compare` and `skilllog export-table` are visible placeholders for Week 5/v0.4.

## Development Priority

1. Keep the run folder schema stable.
2. Keep core logger framework-agnostic.
3. Keep multi-run compare and Skills.md execution out of the v0.2 dashboard scope.
