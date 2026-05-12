from skilllogboard import RunLogger
from skilllogboard.agent.action_log import append_agent_action
from skilllogboard.agent.handoff import build_agent_handoff, collect_handoff_evidence


def _make_run(tmp_path):
    logger = RunLogger(
        project="demo",
        run_name="agent-run",
        root_dir=tmp_path / "runs",
        config={"model_name": "Tiny", "dataset_name": "Demo", "seed": 1},
        main_metric={"name": "val/acc", "mode": "max"},
    )
    logger.log_metric("val/acc", 0.8, step=1)
    logger.finish()
    return logger.run_dir


def test_collect_handoff_evidence_with_missing_optional_files_warns(tmp_path):
    run_dir = _make_run(tmp_path)

    evidence = collect_handoff_evidence(run_dir)

    assert evidence.manifest["run_id"] == run_dir.name
    assert evidence.metric_summary["val/acc"]["value"] == "0.8"
    assert evidence.warnings


def test_build_agent_handoff_references_actions_and_sections(tmp_path):
    run_dir = _make_run(tmp_path)
    append_agent_action(
        run_dir,
        {
            "actor": "codex",
            "action": "test",
            "status": "completed",
            "command": "pytest -q",
            "target": "src/skilllogboard/agent/handoff.py",
            "outputs": ["report.md"],
            "metadata": {"files_changed": ["tests/test_agent_handoff.py"]},
        },
    )

    out = build_agent_handoff(run_dir, actor="codex", task="Finish report", next_steps="Run next seed.")
    text = out.read_text(encoding="utf-8")

    assert "## Task" in text
    assert "## Source Evidence" in text
    assert "`pytest -q`" in text
    assert "## Files Changed" in text
    assert "`src/skilllogboard/agent/handoff.py`" in text
    assert "`tests/test_agent_handoff.py`" in text
    assert "Run next seed." in text
