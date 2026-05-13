import json

from skilllogboard.cli.main import main


def _write_brief(path):
    path.write_text(
        """
# ResearchBrief

## Research Topic
Custom trajectory research.

## Task Type
trajectory

## Input Data
Synthetic paths.

## Target
Future position.

## Main Metric
val/pb_score

## Secondary Metrics
- val/ade

## Required Outputs
- docs
- tests
""",
        encoding="utf-8",
    )


def test_cli_forge_init_brief_creates_and_skips_existing(tmp_path):
    output = tmp_path / "ResearchBrief.md"

    created = main(["forge", "init-brief", "--output", str(output)])
    skipped = main(["forge", "init-brief", "--output", str(output)])

    assert created == 0
    assert skipped == 0
    assert "ResearchBrief" in output.read_text(encoding="utf-8")


def test_cli_forge_plan_scaffold_validate_e2e(tmp_path, capsys):
    brief = tmp_path / "ResearchBrief.md"
    spec = tmp_path / "TemplateSpec.md"
    _write_brief(brief)

    planned = main(
        [
            "forge",
            "plan",
            "--brief",
            str(brief),
            "--name",
            "custom-trajectory",
            "--output",
            str(spec),
        ]
    )
    scaffolded = main(["forge", "scaffold", "--spec", str(spec), "--root-dir", str(tmp_path)])
    validated = main(["forge", "validate", "custom-trajectory", "--root-dir", str(tmp_path)])
    validated_json = main(
        ["forge", "validate", "custom-trajectory", "--root-dir", str(tmp_path), "--json"]
    )

    assert planned == 0
    assert scaffolded == 0
    assert validated == 0
    assert validated_json == 0
    assert (tmp_path / "src" / "skilllogboard" / "plugins" / "custom_trajectory.py").exists()
    assert "Template scaffold" in capsys.readouterr().out


def test_cli_forge_validate_returns_nonzero_for_missing_files(tmp_path, capsys):
    result = main(["forge", "validate", "missing-template", "--root-dir", str(tmp_path), "--json"])

    assert result == 1
    data = json.loads(capsys.readouterr().out)
    assert any(item["outcome"] == "error" for item in data)
