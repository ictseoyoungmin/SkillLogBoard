import subprocess
import sys

import yaml

from skilllogboard.cli.main import main


def test_cli_help_and_version():
    help_result = subprocess.run(
        [sys.executable, "-m", "skilllogboard.cli.main", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert help_result.returncode == 0
    for command in ["init", "inspect", "dashboard", "report", "compare", "export-table"]:
        assert command in help_result.stdout

    version_result = subprocess.run(
        [sys.executable, "-m", "skilllogboard.cli.main", "--version"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert version_result.returncode == 0
    assert "skilllog" in version_result.stdout


def test_init_creates_workspace_and_preserves_existing_skills(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    assert main(["init"]) == 0
    assert (tmp_path / "runs").is_dir()
    skills = tmp_path / "Skills.md"
    assert skills.exists()
    assert "RULE-CONFIG-001" in skills.read_text(encoding="utf-8")

    skills.write_text("custom skills\n", encoding="utf-8")
    assert main(["init"]) == 0
    assert skills.read_text(encoding="utf-8") == "custom skills\n"


def test_inspect_dashboard_and_report_placeholders(tmp_path, capsys):
    run_dir = tmp_path / "run1"
    run_dir.mkdir()
    manifest = {"project": "demo", "run_name": "baseline", "status": "running"}
    (run_dir / "manifest.yaml").write_text(yaml.safe_dump(manifest), encoding="utf-8")

    assert main(["inspect", str(run_dir)]) == 0
    output = capsys.readouterr().out
    assert "Run: baseline" in output
    assert "Status: running" in output

    assert main(["dashboard", str(run_dir)]) == 0
    assert (run_dir / "dashboard.html").exists()

    assert main(["report", str(run_dir)]) == 0
    assert (run_dir / "summary.md").exists()


def test_inspect_missing_manifest_returns_nonzero(tmp_path, capsys):
    run_dir = tmp_path / "missing"
    run_dir.mkdir()

    assert main(["inspect", str(run_dir)]) == 1
    assert "Manifest not found" in capsys.readouterr().err


def test_compare_and_export_table_are_planned_placeholders(capsys):
    assert main(["compare"]) == 2
    assert "planned for Week 5 / v0.4" in capsys.readouterr().out

    assert main(["export-table"]) == 2
    assert "planned for Week 5 / v0.4" in capsys.readouterr().out
