"""CLI tests for skilllog prune safety and wording."""

import json
import yaml

from skilllogboard.cli.main import main


def _run(root, name, baseline=False):
    run_dir = root / name
    run_dir.mkdir(parents=True)
    (run_dir / "manifest.yaml").write_text(
        yaml.safe_dump({"run_id": name, "status": "completed", "baseline": baseline}),
        encoding="utf-8",
    )
    (run_dir / "metrics.csv").write_text(
        "timestamp,step,name,value,group,metadata_json\n,1,score,1.0,val,{}\n",
        encoding="utf-8",
    )
    return run_dir


def test_prune_default_is_dry_run_json(tmp_path, capsys):
    _run(tmp_path, "run-a")
    _run(tmp_path, "run-b")

    assert main(["prune", str(tmp_path), "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["dry_run"] is True
    assert "destructive_actions_performed" in payload
    assert payload["destructive_actions_performed"] is False


def test_prune_execute_does_not_delete_files(tmp_path, capsys):
    run_a = _run(tmp_path, "run-a")
    run_b = _run(tmp_path, "run-b")

    assert main(["prune", str(tmp_path), "--execute", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["dry_run"] is False
    assert payload["destructive_actions_performed"] is False
    assert run_a.exists(), "run-a must not be deleted"
    assert run_b.exists(), "run-b must not be deleted"


def test_prune_text_output_includes_safety_note(tmp_path, capsys):
    _run(tmp_path, "run-a")

    assert main(["prune", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "NOTE" in out or "no files" in out.lower() or "plan" in out.lower()


def test_prune_execute_text_output_includes_external_runner_note(tmp_path, capsys):
    _run(tmp_path, "run-a")

    assert main(["prune", str(tmp_path), "--execute"]) == 0
    out = capsys.readouterr().out
    assert "external" in out.lower() or "retention runner" in out.lower()
