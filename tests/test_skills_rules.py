from skilllogboard.skills.parser import RuleSpec
from skilllogboard.skills.rules import execute_rule


def _context():
    return {
        "config": {"model_name": "TinyNet", "seed": 42},
        "metric_series": {
            "val/acc": [{"value": 0.7}, {"value": 0.9}, {"value": 0.85}],
            "val/loss": [{"value": 0.5}, {"value": 0.4}],
        },
        "artifacts": [{"name": "best_checkpoint", "type": "artifact"}],
    }


def test_rule_result_is_json_serializable():
    spec = RuleSpec("RULE-CONFIG-001", "required_config", params={"keys": ["model_name"]})

    result = execute_rule(spec, _context()).to_dict()

    assert result["rule_id"] == "RULE-CONFIG-001"
    assert result["outcome"] == "passed"
    assert result["timestamp"]


def test_required_config_pass_and_missing():
    passed = execute_rule(
        RuleSpec("RULE-CONFIG-001", "required_config", params={"keys": ["model_name", "seed"]}),
        _context(),
    )
    missing = execute_rule(
        RuleSpec("RULE-CONFIG-002", "required_config", severity="error", params={"keys": ["lr"]}),
        _context(),
    )

    assert passed.outcome == "passed"
    assert missing.outcome == "error"
    assert missing.details["missing"] == ["lr"]


def test_required_metric_pass_and_missing():
    passed = execute_rule(
        RuleSpec("RULE-METRIC-001", "required_metric", params={"keys": ["val/acc"]}),
        _context(),
    )
    missing = execute_rule(
        RuleSpec("RULE-METRIC-002", "required_metric", params={"keys": ["test/acc"]}),
        _context(),
    )

    assert passed.outcome == "passed"
    assert missing.outcome == "warning"
    assert missing.details["missing"] == ["test/acc"]


def test_metric_threshold_max_and_min_modes():
    max_pass = execute_rule(
        RuleSpec("RULE-THRESH-001", "metric_threshold", params={"metric": "val/acc", "threshold": 0.8, "mode": "max"}),
        _context(),
    )
    min_pass = execute_rule(
        RuleSpec("RULE-THRESH-002", "metric_threshold", params={"metric": "val/loss", "threshold": 0.45, "mode": "min"}),
        _context(),
    )
    max_fail = execute_rule(
        RuleSpec("RULE-THRESH-003", "metric_threshold", params={"metric": "val/acc", "threshold": 0.95, "mode": "max"}),
        _context(),
    )

    assert max_pass.outcome == "passed"
    assert min_pass.outcome == "passed"
    assert max_fail.outcome == "warning"
    assert max_fail.details["observed"] == 0.85


def test_best_last_gap_rule():
    ok = execute_rule(
        RuleSpec("RULE-GAP-001", "best_last_gap", params={"metric": "val/acc", "threshold": 0.1, "mode": "max"}),
        _context(),
    )
    warn = execute_rule(
        RuleSpec("RULE-GAP-002", "best_last_gap", params={"metric": "val/acc", "threshold": 0.01, "mode": "max"}),
        _context(),
    )

    assert ok.outcome == "passed"
    assert warn.outcome == "warning"
    assert warn.details["gap"] > 0.01


def test_artifact_required_and_planned_rule():
    artifact = execute_rule(
        RuleSpec("RULE-ART-001", "artifact_required", params={"artifacts": ["best_checkpoint"]}),
        _context(),
    )
    planned = execute_rule(
        RuleSpec("RULE-VIS-001", "dashboard_panel", status="Planned", params={"keys": ["metric_curve"]}),
        _context(),
    )

    assert artifact.outcome == "passed"
    assert planned.outcome == "planned"
    assert planned.status == "Planned"
