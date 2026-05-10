# Research Templates

SkillLogBoard templates are lightweight logging/reporting starters. They do not include private
datasets, trained models, or heavy framework dependencies.

## Status

| Template | Status | Purpose |
|---|---|---|
| `ir-drop` | Implemented | Synthetic IR-drop logging, dashboard, and compare conventions. |
| `trajectory` | Implemented | Synthetic trajectory logging, dashboard, and compare conventions. |
| `classification` | Planned | Future classification starter. |
| `segmentation` | Planned | Future segmentation starter. |
| `finance-dashboard` | Planned | Future finance dashboard starter. |

## IR-drop

Initialize workspace files:

```bash
skilllog init --template ir-drop
```

Run the synthetic example:

```bash
python examples/ir_drop_example.py
```

Default config fields:

```text
template
design_name
corner
seed
grid_size
label
```

Metric convention:

```text
train/loss
val/mae
val/high_drop_f1
val/raw_mae
```

The IR-drop template is a logging/reporting template only. It does not include a model, external
dataset, private design data, or EDA-tool dependency.

## Trajectory

Initialize workspace files:

```bash
skilllog init --template trajectory
```

Run the synthetic example:

```bash
python examples/trajectory_example.py
```

Default config fields:

```text
template
model
dataset
seed
encoder
horizon
lr
batch_size
```

Metric convention:

```text
train/loss
val/loss
val/pb_score
val/endpoint_error
```

The trajectory template is a logging/reporting template only. Model training, datasets, and
framework-specific integrations are supplied by the user.

## Optional Integrations

PyTorch and Lightning helpers are optional and import their frameworks lazily. The core package
works without torch or Lightning installed.

`examples/sklearn_example.py` is a core `RunLogger` example with sklearn-style accuracy/F1 metrics.
It intentionally avoids importing scikit-learn so the example can run in lightweight environments.
