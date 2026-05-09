import csv
import json

from skilllogboard.writers.csv_writer import MetricsCsvWriter


def test_metrics_csv_writer_header_append_group_and_metadata(tmp_path):
    path = tmp_path / "metrics.csv"
    writer = MetricsCsvWriter(path)

    writer.write_metric("train/loss", 1.0, step=0, metadata={"epoch": 0})
    writer.write_metric("val_acc", 0.8)

    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert MetricsCsvWriter.fieldnames == [
        "timestamp",
        "step",
        "name",
        "value",
        "group",
        "metadata_json",
    ]
    assert len(rows) == 2
    assert rows[0]["name"] == "train/loss"
    assert rows[0]["group"] == "train"
    assert rows[0]["step"] == "0"
    assert json.loads(rows[0]["metadata_json"]) == {"epoch": 0}
    assert rows[1]["group"] == ""
