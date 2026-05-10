from pathlib import Path

from examples.trajectory_example import main as run_trajectory_example
from skilllogboard import RunLogger
from skilllogboard.dashboards.compare_builder import build_compare_report
from skilllogboard.plugins.registry import get_template
from skilllogboard.plugins.trajectory import trajectory_template
from skilllogboard.skills.parser import parse_skills_text


def test_trajectory_template_registered_and_has_pb_score():
    template = get_template("trajectory")

    assert template == trajectory_template()
    assert template.is_implemented
    assert "val/pb_score" in template.metric_names
    for key in ["model", "dataset", "seed", "encoder", "horizon", "lr", "batch_size"]:
        assert key in template.default_config


def test_trajectory_default_skills_parse_and_include_metrics():
    template = trajectory_template()

    rules = parse_skills_text(template.default_skills)

    assert {rule.rule_type for rule in rules} >= {"required_config", "required_metric"}
    assert "val/pb_score" in template.default_skills
    assert "val/endpoint_error" in template.default_skills


def test_trajectory_example_runs_without_external_data(tmp_path):
    run_dir = run_trajectory_example(root_dir=tmp_path / "runs")

    assert (run_dir / "metrics.csv").exists()
    assert (run_dir / "dashboard.html").exists()
    assert (run_dir / "summary.md").exists()
    assert (run_dir / "skill_trace.jsonl").exists()
    assert "val/pb_score" in (run_dir / "metrics.csv").read_text(encoding="utf-8")


def test_trajectory_runs_compare_on_pb_score(tmp_path):
    template = trajectory_template()
    runs_root = tmp_path / "runs"
    skills_path = tmp_path / "Skills.trajectory.md"
    skills_path.write_text(template.default_skills, encoding="utf-8")

    for seed, score in [(1, 0.57), (2, 0.73), (3, 0.69)]:
        logger = RunLogger(
            project="trajectory_demo",
            run_name=f"trajectory-seed-{seed}",
            root_dir=runs_root,
            config={**template.default_config, "seed": seed},
            main_metric={"name": "val/pb_score", "mode": "max"},
        )
        logger.log_metrics(
            {
                "train/loss": 1.0 / seed,
                "val/loss": 1.0 - score,
                "val/pb_score": score,
                "val/endpoint_error": 2.5 - score,
            },
            step=1,
        )
        logger.run_skill_checks(skills_path)
        logger.finish(build_dashboard=True, build_report=True)

    paths = build_compare_report(
        runs_root,
        metric="val/pb_score",
        mode="max",
        output_dir=tmp_path / "compare",
    )

    assert Path(paths["csv"]).exists()
    assert "val/pb_score" in paths["md"].read_text(encoding="utf-8")
    html = paths["html"].read_text(encoding="utf-8")
    assert "Leaderboard" in html
    assert "dashboard.html" in html
