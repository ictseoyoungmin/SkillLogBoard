from skilllogboard import RunLogger
from skilllogboard.cli.main import main


def _make_runs(tmp_path):
    runs_root = tmp_path / "runs"
    for seed, acc in [(1, 0.7), (2, 0.9)]:
        logger = RunLogger(
            project="demo",
            run_name=f"seed-{seed}",
            root_dir=runs_root,
            config={"model": "Tiny", "seed": seed, "lr": 0.001},
            main_metric={"name": "val/acc", "mode": "max"},
        )
        logger.log_metric("val/acc", acc, step=1)
        logger.finish(build_dashboard=True)
    return runs_root


def test_cli_compare_prints_leaderboard_and_writes_outputs(tmp_path, capsys):
    runs_root = _make_runs(tmp_path)
    out_dir = tmp_path / "compare"

    result = main(
        [
            "compare",
            str(runs_root),
            "--metric",
            "val/acc",
            "--mode",
            "max",
            "--output-dir",
            str(out_dir),
        ]
    )

    output = capsys.readouterr().out
    assert result == 0
    assert "val/acc" in output
    assert "seed-2" in output
    assert (out_dir / "compare.csv").exists()
    assert (out_dir / "compare.md").exists()
    assert (out_dir / "compare.html").exists()


def test_cli_compare_missing_runs_is_readable(tmp_path, capsys):
    result = main(["compare", str(tmp_path / "empty"), "--metric", "val/acc"])

    assert result == 1
    assert "No run folders" in capsys.readouterr().err


def test_cli_export_table_formats(tmp_path):
    runs_root = _make_runs(tmp_path)

    for fmt in ["csv", "md", "latex"]:
        out = tmp_path / f"leaderboard.{fmt}"
        result = main(
            [
                "export-table",
                str(runs_root),
                "--metric",
                "val/acc",
                "--format",
                fmt,
                "--output",
                str(out),
            ]
        )
        assert result == 0
        assert out.exists()

    assert "rank" in (tmp_path / "leaderboard.csv").read_text(encoding="utf-8")
    assert "| --- |" in (tmp_path / "leaderboard.md").read_text(encoding="utf-8")
    assert "\\begin{tabular}" in (tmp_path / "leaderboard.latex").read_text(encoding="utf-8")
