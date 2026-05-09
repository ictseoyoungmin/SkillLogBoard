# SkillLogBoard

Portable experiment logging and dashboard package for local-first ML research.

## Week 1 Skeleton

This repository skeleton is prepared for Week 1 development:

- package skeleton and `pyproject.toml`
- `src/skilllogboard` layout
- CLI entry point
- run id generation
- manifest schema
- event schema and JSONL writer
- metrics CSV writer placeholder
- config/git/system snapshot placeholder
- docs/examples/tests placeholders

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
logger.finish(build_dashboard=True, build_report=True)
```

## Development Priority

1. Keep the run folder schema stable.
2. Keep core logger framework-agnostic.
3. Avoid heavy dashboard work before writers and manifest are reliable.
