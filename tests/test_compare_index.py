import csv
import json

import yaml

from skilllogboard.compare.run_index import (
    RunRecord,
    build_run_index,
    discover_runs,
    load_run_record,
    save_run_index,
)


def _make_run(root, project="demo", run_id="run-a", metric_value=0.8, seed=1):
    run_dir = root / project / run_id
    run_dir.mkdir(parents=True)
    manifest = {
        "project": project,
        "run_id": run_id,
        "run_name": run_id,
        "run_dir": str(run_dir),
        "status": "completed",
        "created_at": "2026-05-10T00:00:00+09:00",
        "main_metric": {"name": "val/acc", "mode": "max"},
        "best_metric": {
            "name": "val/acc",
            "mode": "max",
            "best_value": metric_value,
            "best_step": 2,
        },
        "seed": seed,
    }
    (run_dir / "manifest.yaml").write_text(yaml.safe_dump(manifest), encoding="utf-8")
    (run_dir / "config.yaml").write_text(
        yaml.safe_dump({"model_name": "TinyNet", "seed": seed, "lr": 0.001}),
        encoding="utf-8",
    )
    with (run_dir / "metrics.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "value", "step", "metadata_json"])
        writer.writeheader()
        writer.writerow({"name": "val/acc", "value": metric_value - 0.1, "step": 1, "metadata_json": "{}"})
        writer.writerow({"name": "val/acc", "value": metric_value, "step": 2, "metadata_json": "{}"})
    (run_dir / "artifact_index.json").write_text(
        json.dumps({"artifacts": [{"name": "plot"}, {"name": "weights"}]}),
        encoding="utf-8",
    )
    (run_dir / "skill_trace.jsonl").write_text(
        json.dumps({"outcome": "warning"}) + "\n" + json.dumps({"outcome": "error"}) + "\n",
        encoding="utf-8",
    )
    return run_dir


def test_run_record_is_json_friendly():
    record = RunRecord(project="demo", run_id="r1", run_name="r1", run_dir="runs/demo/r1")

    data = record.to_dict()

    assert data["status"] == "unknown"
    json.dumps(data)


def test_discover_runs_recursive_and_deterministic(tmp_path):
    root = tmp_path / "runs"
    second = _make_run(root, run_id="run-b")
    first = _make_run(root, run_id="run-a")
    (root / ".cache" / "ignored").mkdir(parents=True)

    assert discover_runs(root) == [first, second]
    assert discover_runs(tmp_path / "missing") == []


def test_load_run_record_complete_run(tmp_path):
    run_dir = _make_run(tmp_path / "runs", metric_value=0.91, seed=7)

    record = load_run_record(run_dir).to_dict()

    assert record["project"] == "demo"
    assert record["config"]["seed"] == 7
    assert record["metrics"]["val/acc"]["value"] == 0.91
    assert record["artifact_count"] == 2
    assert record["warning_count"] == 1
    assert record["error_count"] == 1


def test_load_run_record_partial_run_does_not_crash(tmp_path):
    run_dir = tmp_path / "runs" / "demo" / "partial"
    run_dir.mkdir(parents=True)
    (run_dir / "manifest.yaml").write_text("project: demo\nrun_id: partial\n", encoding="utf-8")

    record = load_run_record(run_dir).to_dict()

    assert record["run_id"] == "partial"
    assert record["metrics"] == {}
    assert record["artifact_count"] == 0


def test_build_and_save_run_index_json(tmp_path):
    root = tmp_path / "runs"
    _make_run(root, run_id="run-a")
    _make_run(root, run_id="run-b")

    records = build_run_index(root)
    out = save_run_index(records, tmp_path / "index.json")

    assert [record["run_id"] for record in records] == ["run-a", "run-b"]
    assert json.loads(out.read_text(encoding="utf-8"))[0]["run_id"] == "run-a"
