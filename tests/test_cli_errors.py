from skilllogboard.cli.main import main


def test_cli_returns_nonzero_for_missing_run_dir(capsys):
    assert main(["inspect", "does-not-exist"]) == 1
    assert "Run directory not found" in capsys.readouterr().err


def test_cli_returns_nonzero_for_file_path(tmp_path, capsys):
    path = tmp_path / "not-a-run.txt"
    path.write_text("x", encoding="utf-8")

    assert main(["dashboard", str(path)]) == 1
    assert "not a directory" in capsys.readouterr().err


def test_cli_report_requires_manifest(tmp_path, capsys):
    run_dir = tmp_path / "run"
    run_dir.mkdir()

    assert main(["report", str(run_dir)]) == 1
    assert "Manifest not found" in capsys.readouterr().err
