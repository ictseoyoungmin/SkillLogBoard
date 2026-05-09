# SkillLogBoard Default Skills

These are starter rule definitions for future Skills.md validation. The rule
engine is planned for Week 4/v0.3 and is not executed by v0.2.

## RULE-CONFIG-001
- type: required_config
- keys: [model_name, dataset_name, seed, optimizer, lr, batch_size]
- severity: warning
- status: planned-v0.3

## RULE-METRIC-001
- type: required_metric
- keys: [train/loss, val/loss]
- severity: warning
- status: planned-v0.3
