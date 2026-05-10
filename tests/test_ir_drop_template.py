from pathlib import Path

from examples.ir_drop_example import main as run_ir_drop_example
from skilllogboard import RunLogger
from skilllogboard.dashboards.compare_builder import build_compare_report
from skilllogboard.plugins.ir_drop import ir_drop_template
from skilllogboard.plugins.registry import get_template
from skilllogboard.skills.parser import parse_skills_text


def test_ir_drop_template_registered_and_dependency_free():
    template = get_template("ir-drop")

    assert template == ir_drop_template()
    assert template.is_implemented
    assert "val/high_drop_f1" in template.metric_names
    assert "dataset_path" not in template.default_config
    assert "private" not in " ".join(template.default_config)


def test_ir_drop_default_skills_parse_and_include_metrics():
    template = ir_drop_template()

    rules = parse_skills_text(template.default_skills)

    assert {rule.rule_type for rule in rules} >= {"required_config", "required_metric"}
    assert "val/high_drop_f1" in template.default_skills
    assert "val/raw_mae" in template.default_skills


def test_ir_drop_example_runs_without_external_data(tmp_path):
    run_dir = run_ir_drop_example(root_dir=tmp_path / "runs")

    assert (run_dir / "metrics.csv").exists()
    assert (run_dir / "dashboard.html").exists()
    assert (run_dir / "summary.md").exists()
    assert (run_dir / "skill_trace.jsonl").exists()
    assert "val/high_drop_f1" in (run_dir / "metrics.csv").read_text(encoding="utf-8")


def test_ir_drop_runs_compare_on_high_drop_f1(tmp_path):
    template = ir_drop_template()
    runs_root = tmp_path / "runs"
    skills_path = tmp_path / "Skills.ir-drop.md"
    skills_path.write_text(template.default_skills, encoding="utf-8")

    for seed, score in [(1, 0.61), (2, 0.79), (3, 0.72)]:
        logger = RunLogger(
            project="ir_drop_demo",
            run_name=f"ir-drop-seed-{seed}",
            root_dir=runs_root,
            config={**template.default_config, "seed": seed},
            main_metric={"name": "val/high_drop_f1", "mode": "max"},
        )
        logger.log_metrics(
            {
                "train/loss": 1.0 / seed,
                "val/mae": 3.0 - score,
                "val/high_drop_f1": score,
                "val/raw_mae": 3.6 - score,
            },
            step=1,
        )
        logger.run_skill_checks(skills_path)
        logger.finish(build_dashboard=True, build_report=True)

    paths = build_compare_report(
        runs_root,
        metric="val/high_drop_f1",
        mode="max",
        output_dir=tmp_path / "compare",
    )

    assert Path(paths["csv"]).exists()
    assert "val/high_drop_f1" in paths["md"].read_text(encoding="utf-8")
    html = paths["html"].read_text(encoding="utf-8")
    assert "Leaderboard" in html
    assert "dashboard.html" in html
