from skilllogboard import RunLogger
from skilllogboard.cli.main import main


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


def test_cli_report_build_and_check(tmp_path, capsys):
    runs_root = _make_runs(tmp_path)
    out = tmp_path / "report"

    result = main(
        [
            "report",
            "build",
            str(runs_root),
            "--metric",
            "val/acc",
            "--output-dir",
            str(out),
        ]
    )

    assert result == 0
    assert (out / "report.md").exists()
    assert (out / "report.html").exists()
    assert (out / "report_manifest.yaml").exists()
    assert "Report directory" in capsys.readouterr().out

    check = main(["report", "check", str(out), "--required-table", "leaderboard"])
    assert check == 0
    assert "passed" in capsys.readouterr().out


def test_cli_export_table_supports_seed_summary(tmp_path):
    runs_root = _make_runs(tmp_path)
    out = tmp_path / "seed-summary.md"

    result = main(
        [
            "export-table",
            str(runs_root),
            "--table",
            "seed-summary",
            "--metric",
            "val/acc",
            "--group-by",
            "model",
            "--format",
            "md",
            "--output",
            str(out),
        ]
    )

    assert result == 0
    assert "group_key" in out.read_text(encoding="utf-8")


def test_cli_export_figure_missing_dependency_is_readable(tmp_path, capsys, monkeypatch):
    runs_root = _make_runs(tmp_path)

    import skilllogboard.reports.figure_builder as figure_builder

    def missing():
        raise figure_builder.OptionalFigureDependencyError("missing report extra")

    monkeypatch.setattr(figure_builder, "require_matplotlib", missing)

    result = main(
        [
            "export-figure",
            str(runs_root),
            "--type",
            "metric-curve-overlay",
            "--metric",
            "val/acc",
            "--output",
            str(tmp_path / "curve.png"),
        ]
    )

    assert result == 2
    assert "missing report extra" in capsys.readouterr().err
