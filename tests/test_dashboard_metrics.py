from skilllogboard import RunLogger
from skilllogboard.dashboards.components import group_metrics, load_metrics
from skilllogboard.dashboards.static_builder import build_dashboard


def test_metrics_loader_groups_series(tmp_path):
    logger = RunLogger(project="demo", run_name="metrics", root_dir=tmp_path / "runs")
    logger.log_metrics({"train/loss": 1.0, "val/acc": 0.7}, step=0)
    logger.log_metrics({"train/loss": 0.5, "val/acc": 0.9}, step=1)

    rows = load_metrics(logger.run_dir / "metrics.csv")
    grouped = group_metrics(rows)

    assert grouped["train/loss"][0]["value"] == 1.0
    assert grouped["train/loss"][1]["step"] == 1
    assert grouped["val/acc"][1]["value"] == 0.9
    assert load_metrics(logger.run_dir / "missing.csv") == []


def test_dashboard_renders_metrics_and_best_metric(tmp_path):
    logger = RunLogger(
        project="demo",
        run_name="metric-dashboard",
        root_dir=tmp_path / "runs",
        main_metric={"name": "val/acc", "mode": "max"},
    )
    logger.log_metrics({"train/loss": 1.0, "val/acc": 0.7}, step=0)
    logger.log_metrics({"train/loss": 0.5, "val/acc": 0.9}, step=1)
    logger.finish(build_dashboard=True)

    html = (logger.run_dir / "dashboard.html").read_text(encoding="utf-8")

    assert "train/loss" in html
    assert "val/acc" in html
    assert "Best value:" in html
    assert "0.9" in html
    assert "Metric curve data:" in html


def test_dashboard_no_best_metric_empty_state(tmp_path):
    logger = RunLogger(project="demo", run_name="no-best", root_dir=tmp_path / "runs")
    out = build_dashboard(logger.run_dir)

    assert "No main metric configured yet." in out.read_text(encoding="utf-8")
