from skilllogboard import RunLogger
from skilllogboard.cli.main import main


def test_cli_can_inspect_report_and_dashboard_existing_v01_run(tmp_path, capsys):
    logger = RunLogger(project="demo", run_name="cli", root_dir=tmp_path / "runs")
    logger.log_metric("val/acc", 0.9, step=1)
    logger.finish(build_report=True, build_dashboard=True)

    assert main(["inspect", str(logger.run_dir)]) == 0
    assert "project: demo" in capsys.readouterr().out

    assert main(["report", str(logger.run_dir)]) == 0
    assert (logger.run_dir / "summary.md").stat().st_size > 0

    assert main(["dashboard", str(logger.run_dir)]) == 0
    assert (logger.run_dir / "dashboard.html").stat().st_size > 0


def test_cli_missing_manifest_error_is_readable(tmp_path, capsys):
    run_dir = tmp_path / "missing"
    run_dir.mkdir()

    assert main(["inspect", str(run_dir)]) == 1
    assert "Manifest not found" in capsys.readouterr().out
