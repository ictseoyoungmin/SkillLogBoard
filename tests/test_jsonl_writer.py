import json

from skilllogboard.core.events import Event
from skilllogboard.writers.jsonl_writer import JsonlWriter


def test_jsonl_writer_appends_dicts_and_preserves_unicode(tmp_path):
    path = tmp_path / "logs" / "events.jsonl"
    writer = JsonlWriter(path)

    writer.write({"type": "note", "key": "메모", "value": "안녕"})
    writer.write({"type": "metric", "key": "val/acc", "value": 0.8})

    lines = path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0])["key"] == "메모"
    assert json.loads(lines[1])["value"] == 0.8


def test_jsonl_writer_accepts_event_objects(tmp_path):
    path = tmp_path / "events.jsonl"
    writer = JsonlWriter(path)

    writer.write(Event(type="metric", key="val/acc", value=0.8, step=1, metadata={"split": "val"}))
    writer.write(Event(type="lifecycle", key="finish", value="completed"))
    writer.write(Event(type="artifact", key="best", path="artifacts/best.ckpt"))

    lines = path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 3
    records = [json.loads(line) for line in lines]
    assert records[0]["type"] == "metric"
    assert records[0]["metadata"] == {"split": "val"}
    assert records[1]["key"] == "finish"
    assert records[2]["path"] == "artifacts/best.ckpt"
