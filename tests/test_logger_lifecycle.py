import pytest

from skilllogboard import RunLogger
from tests.helpers import read_jsonl, read_yaml


def test_runlogger_initial_state(tmp_path):
    logger = RunLogger(project="demo", run_name="baseline", root_dir=tmp_path / "runs")

    manifest = read_yaml(logger.run_dir / "manifest.yaml")
    events = read_jsonl(logger.run_dir / "events.jsonl")

    assert logger.run_dir.exists()
    assert (logger.run_dir / "config.yaml").exists()
    assert (logger.run_dir / "system.json").exists()
    assert (logger.run_dir / "git.json").exists()
    assert manifest["status"] == "running"
    assert events[0]["type"] == "lifecycle"
    assert events[0]["key"] == "start"
    assert events[0]["value"] == "running"


def test_context_manager_success_completes_once(tmp_path):
    with RunLogger(project="demo", run_name="ctx", root_dir=tmp_path / "runs") as logger:
        logger.log_note("inside")

    manifest = read_yaml(logger.run_dir / "manifest.yaml")
    events = read_jsonl(logger.run_dir / "events.jsonl")
    finish_events = [event for event in events if event["type"] == "lifecycle" and event["key"] == "finish"]

    assert manifest["status"] == "completed"
    assert len(finish_events) == 1
    assert (logger.run_dir / "summary.md").exists()
    assert (logger.run_dir / "dashboard.html").exists()


def test_context_manager_failure_marks_failed_and_propagates(tmp_path):
    with pytest.raises(RuntimeError, match="boom"):
        with RunLogger(project="demo", run_name="fail", root_dir=tmp_path / "runs") as logger:
            raise RuntimeError("boom")

    manifest = read_yaml(logger.run_dir / "manifest.yaml")
    events = read_jsonl(logger.run_dir / "events.jsonl")

    assert manifest["status"] == "failed"
    assert manifest["error_summary"] == "boom"
    assert events[-1]["type"] == "lifecycle"
    assert events[-1]["key"] == "fail"


def test_finish_and_fail_are_idempotent(tmp_path):
    logger = RunLogger(project="demo", run_name="idem", root_dir=tmp_path / "runs")

    logger.finish()
    logger.finish()
    logger.fail("late failure")

    manifest = read_yaml(logger.run_dir / "manifest.yaml")
    events = read_jsonl(logger.run_dir / "events.jsonl")
    finish_events = [event for event in events if event["type"] == "lifecycle" and event["key"] == "finish"]

    assert manifest["status"] == "completed"
    assert len(finish_events) == 1


def test_fail_then_finish_keeps_failed_status(tmp_path):
    logger = RunLogger(project="demo", run_name="failed", root_dir=tmp_path / "runs")

    logger.fail("first failure")
    logger.finish()
    logger.close()

    manifest = read_yaml(logger.run_dir / "manifest.yaml")
    events = read_jsonl(logger.run_dir / "events.jsonl")
    fail_events = [event for event in events if event["type"] == "lifecycle" and event["key"] == "fail"]

    assert manifest["status"] == "failed"
    assert manifest["error_summary"] == "first failure"
    assert len(fail_events) == 1
    assert events[-1]["key"] == "fail"
