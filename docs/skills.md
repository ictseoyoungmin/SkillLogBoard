# Skills.md Rule Types

SkillLogBoard v0.3 supports a small Markdown rule format. A rule starts with a
`## RULE-*` heading and contains YAML-like bullet metadata.

```markdown
## RULE-CONFIG-001
- type: required_config
- keys: [model_name, dataset_name, seed]
- severity: warning
- status: MVP
- message: Core reproducibility config should be logged.
```

Supported fields: `type`, `keys`, `artifacts`, `metric`, `threshold`, `mode`,
`severity`, `status`, and `message`.

| Rule Type | Status | Required Fields | Purpose |
|---|---|---|---|
| `required_config` | MVP Supported | `keys` | Check required config keys in `config.yaml`. |
| `required_metric` | MVP Supported | `keys` | Check required metric names in `metrics.csv`. |
| `metric_threshold` | MVP Supported | `metric`, `threshold`, `mode` | Check latest metric value against a threshold. |
| `best_last_gap` | MVP Supported | `metric`, `threshold`, `mode` | Warn when best and last metric values diverge. |
| `artifact_required` | MVP Supported | `keys` or `artifacts` | Check required artifact names in `artifact_index.json`. |
| `dashboard_panel` | Planned | `keys` | Planned dashboard composition rule. |
| `domain_breakdown` | Planned | `keys` | Planned research-template rule. |

Status labels are `MVP`, `Planned`, and `Experimental`. Planned rules are
parsed and traced as planned, but they are not executed as MVP checks.
