from skilllogboard import RunLogger
from skilllogboard.reports.report_builder import build_report_package


def _make_runs(tmp_path):
    runs_root = tmp_path / "runs"
    for seed, acc in [(1, 0.7), (2, 0.9)]:
        logger = RunLogger(
            project="demo",
            run_name=f"seed-{seed}",
            root_dir=runs_root,
            config={"model": "Tiny", "seed": seed},
            main_metric={"name": "val/acc", "mode": "max"},
        )
        logger.log_metric("val/acc", acc, step=seed)
        logger.finish()
    return runs_root


def test_report_html_minimal_is_offline_safe(tmp_path):
    result = build_report_package(_make_runs(tmp_path), metric="val/acc", output_dir=tmp_path / "report")
    html = result.report_html.read_text(encoding="utf-8")

    assert "https://" not in html
    assert "http://" not in html
    assert "<style>" in html


def test_report_package_mode_uses_relative_assets(tmp_path):
    result = build_report_package(
        _make_runs(tmp_path),
        metric="val/acc",
        output_dir=tmp_path / "report",
        render_mode="package",
    )
    html = result.report_html.read_text(encoding="utf-8")

    assert 'href="assets/report.css"' in html
    assert 'src="assets/report.js"' in html
    assert (result.report_dir / "assets" / "report.css").exists()
