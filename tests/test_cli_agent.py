import json

from skilllogboard import RunLogger
from skilllogboard.cli.main import main


def _make_run(tmp_path):
    logger = RunLogger(
        project="demo",
        run_name="agent-cli",
        root_dir=tmp_path / "runs",
        config={"model_name": "Tiny", "dataset_name": "Demo", "seed": 1},
        main_metric={"name": "val/acc", "mode": "max"},
    )
    logger.log_metric("val/acc", 0.8, step=1)
    logger.finish()
    return logger.run_dir


def test_cli_agent_init_creates_control_plane(tmp_path, capsys):
    result = main(["agent", "init", "--root-dir", str(tmp_path), "--template", "trajectory"])

    assert result == 0
    assert (tmp_path / ".skilllog" / "agent_skills.md").exists()
    assert "Initialized agent control plane" in capsys.readouterr().out


def test_cli_agent_log_action_handoff_check_and_inspect(tmp_path, capsys):
    run_dir = _make_run(tmp_path)
    (run_dir / "skill_trace.jsonl").write_text(
        json.dumps({"rule_id": "RULE-1", "outcome": "passed", "severity": "warning"}) + "\n",
        encoding="utf-8",
    )

    logged = main(
        [
            "agent",
            "log-action",
            str(run_dir),
            "--actor",
            "codex",
            "--action",
            "run tests",
            "--status",
            "completed",
            "--command",
            "pytest -q",
            "--output",
            "agent/handoff.md",
        ]
    )
    handed = main(["agent", "handoff", str(run_dir), "--actor", "codex", "--task", "handoff"])
    checked = main(["agent", "check", str(run_dir)])
    inspected = main(["agent", "inspect", str(run_dir)])

    assert logged == 0
    assert handed == 0
    assert checked == 0
    assert inspected == 0
    assert (run_dir / "agent" / "actions.jsonl").exists()
    assert (run_dir / "agent" / "handoff.md").exists()
    assert "Check errors: 0" in capsys.readouterr().out


def test_cli_agent_check_json_returns_nonzero_for_missing_files(tmp_path, capsys):
    run_dir = _make_run(tmp_path)

    result = main(["agent", "check", str(run_dir), "--json"])

    assert result == 1
    data = json.loads(capsys.readouterr().out)
    assert any(item["outcome"] == "error" for item in data)
