from skilllogboard import RunLogger
from tests.helpers import read_jsonl, read_yaml


def test_log_config_updates_yaml_event_and_manifest_metadata(tmp_path):
    logger = RunLogger(
        project="demo",
        run_name="config",
        root_dir=tmp_path / "runs",
        config={"model_name": "TinyNet", "dataset_name": "Old", "seed": 1, "nested": {"a": 1}},
    )

    logger.log_config({"dataset_name": "새데이터", "seed": 42, "nested": {"b": 2}})

    config = read_yaml(logger.run_dir / "config.yaml")
    manifest = read_yaml(logger.run_dir / "manifest.yaml")
    events = read_jsonl(logger.run_dir / "events.jsonl")
    config_events = [event for event in events if event["type"] == "config"]

    assert config["model_name"] == "TinyNet"
    assert config["dataset_name"] == "새데이터"
    assert config["seed"] == 42
    assert config["nested"] == {"b": 2}
    assert manifest["model_name"] == "TinyNet"
    assert manifest["dataset_name"] == "새데이터"
    assert manifest["seed"] == 42
    assert config_events[-1]["metadata"]["merge"] == "shallow"
