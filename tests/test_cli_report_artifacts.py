import pytest

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
            "--render-mode",
            "package",
        ]
    )

    assert result == 0
    assert (out / "report.md").exists()
    assert (out / "report.html").exists()
    assert (out / "report_manifest.yaml").exists()
    assert (out / "assets" / "report.css").exists()
    assert "Report directory" in capsys.readouterr().out

    check = main(["report", "check", str(out), "--required-table", "leaderboard"])
    assert check == 0
    assert "passed" in capsys.readouterr().out

    validate = main(["report", "validate", str(out), "--json"])
    assert validate == 0
    assert '"ok": true' in capsys.readouterr().out

    opened = main(["report", "open", str(out), "--dry-run"])
    assert opened == 0
    assert "report.html" in capsys.readouterr().out

    bundled = main(["report", "bundle", str(out), "--output", str(tmp_path / "report.zip")])
    assert bundled == 0
    assert (tmp_path / "report.zip").exists()


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


def test_cli_export_figure_builds_when_report_extra_available(tmp_path):
    import skilllogboard.reports.figure_builder as figure_builder

    try:
        figure_builder.require_matplotlib()
    except figure_builder.OptionalFigureDependencyError as exc:
        pytest.skip(str(exc))

    runs_root = _make_runs(tmp_path)
    out = tmp_path / "curve.png"

    result = main(
        [
            "export-figure",
            str(runs_root),
            "--type",
            "metric-curve-overlay",
            "--metric",
            "val/acc",
            "--output",
            str(out),
        ]
    )

    assert result == 0
    assert out.exists()
