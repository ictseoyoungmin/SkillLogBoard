from pathlib import Path

from skilllogboard.cli.main import main
from skilllogboard.skills.parser import parse_skills


def test_templates_command_lists_implemented_and_planned_templates(capsys):
    code = main(["templates"])

    out = capsys.readouterr().out
    assert code == 0
    assert "ir-drop" in out
    assert "trajectory" in out
    assert "classification" in out
    assert "segmentation" in out
    assert "finance-dashboard" in out
    assert "Implemented" in out
    assert "Planned" in out


def test_init_template_creates_workspace_files(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    code = main(["init", "--template", "ir-drop"])

    out = capsys.readouterr().out
    assert code == 0
    assert "ir-drop" in out
    assert Path("runs").is_dir()
    assert Path("Skills.md").exists()
    assert Path("template_config.yaml").exists()
    assert "val/high_drop_f1" in Path("Skills.md").read_text(encoding="utf-8")
    assert "template: ir-drop" in Path("template_config.yaml").read_text(encoding="utf-8")
    assert parse_skills("Skills.md")


def test_init_trajectory_template_creates_parseable_skills(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    code = main(["init", "--template", "trajectory"])

    out = capsys.readouterr().out
    assert code == 0
    assert "trajectory" in out
    assert "val/pb_score" in Path("Skills.md").read_text(encoding="utf-8")
    assert "template: trajectory" in Path("template_config.yaml").read_text(encoding="utf-8")
    assert parse_skills("Skills.md")


def test_init_template_does_not_overwrite_existing_skills(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    Path("Skills.md").write_text("custom skills", encoding="utf-8")

    code = main(["init", "--template", "trajectory"])

    out = capsys.readouterr().out
    assert code == 0
    assert "Skipped existing files" in out
    assert Path("Skills.md").read_text(encoding="utf-8") == "custom skills"
    assert "template: trajectory" in Path("template_config.yaml").read_text(encoding="utf-8")


def test_init_planned_template_is_explicit(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    code = main(["init", "--template", "classification"])

    out = capsys.readouterr().out
    assert code == 2
    assert "Planned" in out
    assert not Path("Skills.md").exists()
