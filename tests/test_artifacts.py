import json

from skilllogboard import RunLogger
from tests.helpers import read_jsonl


def test_artifact_copy_and_reference_modes_update_index_and_events(tmp_path):
    source = tmp_path / "source file.txt"
    source.write_text("payload", encoding="utf-8")
    logger = RunLogger(project="demo", run_name="artifacts", root_dir=tmp_path / "runs")

    copied = logger.log_artifact("copied artifact", source)
    referenced = logger.log_artifact("referenced artifact", source, copy=False)

    assert copied.startswith("artifacts/")
    assert (logger.run_dir / copied).read_text(encoding="utf-8") == "payload"
    assert referenced == str(source)

    index = json.loads((logger.run_dir / "artifact_index.json").read_text(encoding="utf-8"))
    assert [record["copy"] for record in index["artifacts"]] == [True, False]
    assert index["artifacts"][1]["source"] == str(source)

    events = [event for event in read_jsonl(logger.run_dir / "events.jsonl") if event["type"] == "artifact"]
    assert len(events) == 2
    assert events[0]["path"] == copied
    assert events[1]["path"] == str(source)


def test_artifact_safe_paths_and_collisions(tmp_path):
    source = tmp_path / "../../unsafe name.txt"
    source = tmp_path / "unsafe name.txt"
    source.write_text("payload", encoding="utf-8")
    logger = RunLogger(project="demo", run_name="safe", root_dir=tmp_path / "runs")

    first = logger.log_artifact("../../bad name", source)
    second = logger.log_artifact("../../bad name", source)

    assert first == "artifacts/unsafe_name.txt"
    assert second == "artifacts/unsafe_name_001.txt"
    assert (logger.run_dir / first).resolve().is_relative_to(logger.run_dir.resolve())
    assert (logger.run_dir / second).resolve().is_relative_to(logger.run_dir.resolve())
