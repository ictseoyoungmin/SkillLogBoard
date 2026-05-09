import json

from skilllogboard import RunLogger
from tests.helpers import read_jsonl


def test_artifact_image_table_outputs_work_together(tmp_path):
    artifact = tmp_path / "note.txt"
    artifact.write_text("artifact", encoding="utf-8")
    image = tmp_path / "plot.png"
    image.write_bytes(b"\x89PNG\r\n\x1a\n")
    logger = RunLogger(project="demo", run_name="outputs", root_dir=tmp_path / "runs")

    logger.log_artifact("note", artifact)
    logger.log_image("plot", image)
    logger.log_table("scores", [{"metric": "acc", "value": 0.9}])
    logger.finish()

    assert (logger.run_dir / "artifacts").is_dir()
    assert (logger.run_dir / "images").is_dir()
    assert (logger.run_dir / "tables").is_dir()
    index = json.loads((logger.run_dir / "artifact_index.json").read_text(encoding="utf-8"))
    assert {record["type"] for record in index["artifacts"]} == {"artifact", "image", "table"}

    events = read_jsonl(logger.run_dir / "events.jsonl")
    assert {"artifact", "image", "table"}.issubset({event["type"] for event in events})
