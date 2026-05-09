import pytest

from skilllogboard.skills.parser import SkillsParseError, parse_skills, parse_skills_text


def test_parse_complete_rule_block():
    rules = parse_skills_text(
        """
# Experiment Skills

## RULE-CONFIG-001
- type: required_config
- keys: [model_name, dataset_name, seed]
- severity: error
- status: MVP
- message: Required config keys must exist.
"""
    )

    assert len(rules) == 1
    rule = rules[0]
    assert rule.rule_id == "RULE-CONFIG-001"
    assert rule.rule_type == "required_config"
    assert rule.severity == "error"
    assert rule.status == "MVP"
    assert rule.message == "Required config keys must exist."
    assert rule.params["keys"] == ["model_name", "dataset_name", "seed"]


def test_parse_multiple_blocks_and_ignore_non_rule_sections():
    rules = parse_skills_text(
        """
## Notes
- this is ignored

## RULE-METRIC-001
- type: required_metric
- keys: [train/loss, val/acc]

## RULE-VIS-001
- type: dashboard_panel
- keys: [metric_curve]
- status: Planned
"""
    )

    assert [rule.rule_id for rule in rules] == ["RULE-METRIC-001", "RULE-VIS-001"]
    assert rules[0].severity == "warning"
    assert rules[1].status == "Planned"


def test_malformed_rule_missing_type_raises_readable_error():
    with pytest.raises(SkillsParseError, match="missing required field: type"):
        parse_skills_text(
            """
## RULE-BAD-001
- keys: [a]
"""
        )


def test_default_skills_parse():
    rules = parse_skills("src/skilllogboard/skills/default_skills.md")

    assert {rule.rule_type for rule in rules}.issuperset(
        {"required_config", "required_metric", "metric_threshold", "best_last_gap", "artifact_required"}
    )
    assert any(rule.status == "Planned" for rule in rules)
