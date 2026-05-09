import csv
import json

from skilllogboard import RunLogger
from tests.helpers import read_jsonl


def test_log_table_writes_csv_html_event_and_index(tmp_path):
    logger = RunLogger(project="demo", run_name="table", root_dir=tmp_path / "runs")

    rel_path = logger.log_table(
        "leaderboard",
        [{"run": "a", "score": 0.8}, {"run": "b", "score": 0.9}],
        split="val",
    )

    assert rel_path == "tables/leaderboard.csv"
    assert (logger.run_dir / "tables/leaderboard.html").exists()
    with (logger.run_dir / rel_path).open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows[1]["run"] == "b"
    assert rows[1]["score"] == "0.9"

    index = json.loads((logger.run_dir / "artifact_index.json").read_text(encoding="utf-8"))
    assert index["artifacts"][-1]["type"] == "table"
    assert index["artifacts"][-1]["path"] == rel_path
    events = [event for event in read_jsonl(logger.run_dir / "events.jsonl") if event["type"] == "table"]
    assert events[-1]["metadata"] == {"split": "val"}
