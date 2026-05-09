from skilllogboard import RunLogger
from skilllogboard.dashboards.compare_builder import build_compare_report


def _make_runs(tmp_path):
    runs_root = tmp_path / "runs"
    for seed, acc, lr in [(1, 0.7, 0.001), (2, 0.9, 0.001), (3, 0.6, 0.01)]:
        logger = RunLogger(
            project="demo",
            run_name=f"seed-{seed}",
            root_dir=runs_root,
            config={"model": "Tiny", "seed": seed, "lr": lr},
            main_metric={"name": "val/acc", "mode": "max"},
        )
        logger.log_metric("val/acc", acc, step=1)
        logger.finish(build_dashboard=True)
    return runs_root


def test_build_compare_report_writes_csv_markdown_and_html(tmp_path):
    runs_root = _make_runs(tmp_path)
    out_dir = tmp_path / "compare"

    paths = build_compare_report(runs_root, metric="val/acc", mode="max", output_dir=out_dir)

    assert paths["csv"].name == "compare.csv"
    assert paths["md"].exists()
    assert paths["html"].exists()
    md = paths["md"].read_text(encoding="utf-8")
    html = paths["html"].read_text(encoding="utf-8")
    assert "## Leaderboard" in md
    assert "## Config Diff" in md
    assert "## Ablation Axes" in md
    assert "## Seed Summary" in md
    assert "<!doctype html>" in html
    assert "Leaderboard" in html
    assert "Config Diff" in html
    assert "Ablation Axes" in html
    assert "Seed Summary" in html
    assert "dashboard.html" in html
