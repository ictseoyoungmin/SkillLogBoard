import json
from importlib import resources

from skilllogboard import RunLogger
from skilllogboard.skills.rule_engine import RuleEngine
from tests.helpers import read_jsonl, read_yaml


def _write_skills(path):
    path.write_text(
        """
## RULE-CONFIG-001
- type: required_config
- keys: [model_name, seed]
- severity: error
- status: MVP

## RULE-METRIC-001
- type: required_metric
- keys: [val/acc]
- severity: warning
- status: MVP

## RULE-THRESHOLD-001
- type: metric_threshold
- metric: val/acc
- threshold: 0.8
- mode: max
- severity: warning
- status: MVP

## RULE-GAP-001
- type: best_last_gap
- metric: val/acc
- threshold: 0.2
- mode: max
- severity: warning
- status: MVP

## RULE-ARTIFACT-001
- type: artifact_required
- artifacts: [best_checkpoint]
- severity: warning
- status: MVP

## RULE-VIS-001
- type: dashboard_panel
- keys: [metric_curve]
- severity: info
- status: Planned
""",
        encoding="utf-8",
    )


def test_rule_engine_executes_mvp_rules_and_planned_rules(tmp_path):
    artifact = tmp_path / "best.ckpt"
    artifact.write_text("checkpoint", encoding="utf-8")
    logger = RunLogger(
        project="demo",
        run_name="rules",
        root_dir=tmp_path / "runs",
        config={"model_name": "TinyNet", "seed": 42},
    )
    logger.log_metrics({"val/acc": 0.7}, step=0)
    logger.log_metrics({"val/acc": 0.9}, step=1)
    logger.log_artifact("best_checkpoint", artifact)
    skills_path = tmp_path / "Skills.md"
    _write_skills(skills_path)

    results = RuleEngine.from_file(skills_path).run(logger.run_dir)

    outcomes = {result.rule_id: result.outcome for result in results}
    assert outcomes["RULE-CONFIG-001"] == "passed"
    assert outcomes["RULE-METRIC-001"] == "passed"
    assert outcomes["RULE-THRESHOLD-001"] == "passed"
    assert outcomes["RULE-GAP-001"] == "passed"
    assert outcomes["RULE-ARTIFACT-001"] == "passed"
    assert outcomes["RULE-VIS-001"] == "planned"


def test_rule_engine_missing_skills_is_safe(tmp_path):
    logger = RunLogger(project="demo", run_name="missing-skills", root_dir=tmp_path / "runs")

    results = RuleEngine.from_file(tmp_path / "missing.md").run(logger.run_dir)

    assert results[0].outcome == "skipped"
    assert "not found" in results[0].message


def test_rule_engine_writes_skill_trace_and_manifest_file_map(tmp_path):
    logger = RunLogger(
        project="demo",
        run_name="trace",
        root_dir=tmp_path / "runs",
        config={"model_name": "TinyNet"},
    )
    skills_path = tmp_path / "Skills.md"
    skills_path.write_text(
        """
## RULE-CONFIG-001
- type: required_config
- keys: [model_name, seed]
- severity: warning
- status: MVP
""",
        encoding="utf-8",
    )

    results = logger.run_skill_checks(skills_path=skills_path, stage="finish")

    assert results[0].outcome == "warning"
    trace = read_jsonl(logger.run_dir / "skill_trace.jsonl")
    assert trace[0]["rule_id"] == "RULE-CONFIG-001"
    assert trace[0]["outcome"] == "warning"
    assert trace[0]["status"] == "MVP"
    manifest = read_yaml(logger.run_dir / "manifest.yaml")
    assert manifest["files"]["skill_trace"] == "skill_trace.jsonl"


def test_default_skills_do_not_fail_on_planned_rules(tmp_path):
    artifact = tmp_path / "example_artifact.txt"
    artifact.write_text("artifact", encoding="utf-8")
    logger = RunLogger(
        project="demo",
        run_name="default-skills",
        root_dir=tmp_path / "runs",
        config={
            "model_name": "TinyNet",
            "dataset_name": "Synthetic",
            "seed": 42,
            "optimizer": "AdamW",
            "lr": 0.001,
            "batch_size": 8,
        },
    )
    logger.log_metrics({"train/loss": 1.0, "val/acc": 0.8}, step=0)
    logger.log_metrics({"train/loss": 0.5, "val/acc": 0.85}, step=1)
    logger.log_artifact("example_artifact", artifact)
    default_path = resources.files("skilllogboard.skills").joinpath("default_skills.md")

    results = RuleEngine.from_file(default_path).run(logger.run_dir, write_trace=True)

    assert any(result.outcome == "planned" for result in results)
    assert not any(result.outcome == "error" for result in results)
    assert json.loads((logger.run_dir / "skill_trace.jsonl").read_text(encoding="utf-8").splitlines()[0])
