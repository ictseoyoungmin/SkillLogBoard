import json

from skilllogboard import RunLogger
from tests.helpers import read_jsonl


def test_log_image_records_existing_file_without_optional_dependencies(tmp_path):
    image = tmp_path / "tiny.png"
    image.write_bytes(b"\x89PNG\r\n\x1a\n")
    logger = RunLogger(project="demo", run_name="image", root_dir=tmp_path / "runs")

    rel_path = logger.log_image("preview image", image, step=1, split="val")

    assert rel_path == "images/tiny.png"
    assert (logger.run_dir / rel_path).exists()
    index = json.loads((logger.run_dir / "artifact_index.json").read_text(encoding="utf-8"))
    assert index["artifacts"][-1]["type"] == "image"
    assert index["artifacts"][-1]["path"] == rel_path

    events = [event for event in read_jsonl(logger.run_dir / "events.jsonl") if event["type"] == "image"]
    assert events[-1]["path"] == rel_path
    assert events[-1]["metadata"]["split"] == "val"
