from datetime import datetime

from skilllogboard.core.manifest import Manifest, load_manifest


def test_manifest_defaults_and_required_fields(tmp_path):
    m = Manifest(project="demo", run_name="baseline", run_id="run1", run_dir=str(tmp_path))
    data = m.to_dict()

    assert data["project"] == "demo"
    assert data["run_name"] == "baseline"
    assert data["run_id"] == "run1"
    assert data["status"] == "running"
    assert data["files"] == {}
    assert isinstance(datetime.fromisoformat(data["created_at"]), datetime)


def test_manifest_save_load_unicode_and_temp_cleanup(tmp_path):
    m = Manifest(project="데모", run_name="기준", run_id="run1", run_dir=str(tmp_path))
    path = tmp_path / "manifest.yaml"
    m.save(path)

    data = load_manifest(path)
    assert data["project"] == "데모"
    assert data["run_name"] == "기준"
    assert data["status"] == "running"
    assert data["updated_at"]
    assert list(tmp_path.glob(".manifest_*.yaml")) == []


def test_manifest_status_files_and_metric_metadata_serialization(tmp_path):
    m = Manifest(
        project="demo",
        run_name="baseline",
        run_id="run1",
        run_dir=str(tmp_path),
        main_metric={"name": "val/acc", "mode": "max"},
        best_metric={"name": "val/acc", "value": 0.9, "step": 3},
    )
    m.status = "completed"
    m.files["metrics"] = "metrics.csv"
    m.files["events"] = "events.jsonl"
    path = tmp_path / "nested" / "manifest.yaml"

    m.save(path)
    data = load_manifest(path)

    assert data["status"] == "completed"
    assert data["files"] == {"metrics": "metrics.csv", "events": "events.jsonl"}
    assert data["main_metric"] == {"name": "val/acc", "mode": "max"}
    assert data["best_metric"] == {"name": "val/acc", "value": 0.9, "step": 3}
