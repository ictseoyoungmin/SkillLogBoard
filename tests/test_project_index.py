"""Tests for project index builder, artifact count lightweighting."""

import json
import yaml

from skilllogboard.index.builder import build_project_index
from skilllogboard.live.readers import read_artifact_count


def _run(root, name, artifact_count=0, use_dir=False):
    run_dir = root / name
    run_dir.mkdir(parents=True)
    (run_dir / "manifest.yaml").write_text(
        yaml.safe_dump({"run_id": name, "status": "completed"}),
        encoding="utf-8",
    )
    (run_dir / "metrics.csv").write_text(
        "timestamp,step,name,value,group,metadata_json\n,1,acc,0.9,val,{}\n",
        encoding="utf-8",
    )
    if artifact_count > 0 and not use_dir:
        artifacts = [{"name": f"file_{i}.pt", "type": "model"} for i in range(artifact_count)]
        (run_dir / "artifact_index.json").write_text(
            json.dumps({"artifacts": artifacts}), encoding="utf-8"
        )
    elif artifact_count > 0 and use_dir:
        artifacts_dir = run_dir / "artifacts"
        artifacts_dir.mkdir()
        for i in range(artifact_count):
            (artifacts_dir / f"file_{i}.pt").write_bytes(b"data")
    return run_dir


def test_artifact_count_from_index_json(tmp_path):
    count, warnings = read_artifact_count(tmp_path / "run-x")
    assert count == 0

    _run(tmp_path, "run-a", artifact_count=5)
    count, warnings = read_artifact_count(tmp_path / "run-a")
    assert count == 5
    assert warnings == []


def test_artifact_count_from_artifacts_dir(tmp_path):
    _run(tmp_path, "run-b", artifact_count=3, use_dir=True)
    count, warnings = read_artifact_count(tmp_path / "run-b")
    assert count == 3
    assert warnings == []


def test_build_project_index_stores_artifact_count(tmp_path):
    _run(tmp_path, "run-a", artifact_count=7)
    _run(tmp_path, "run-b", artifact_count=0)

    index = build_project_index(tmp_path)
    by_id = {r.run_id: r for r in index.runs}
    assert by_id["run-a"].artifact_count == 7
    assert by_id["run-b"].artifact_count == 0


def test_build_project_index_large_artifact_count(tmp_path):
    """Index builder handles many synthetic artifacts without loading full payload."""
    many = 200
    _run(tmp_path, "run-many", artifact_count=many)
    index = build_project_index(tmp_path)
    assert index.runs[0].artifact_count == many


def test_artifact_count_dir_truncation(tmp_path):
    """Artifact count from directory is bounded at max_scan."""
    run_dir = tmp_path / "run-x"
    run_dir.mkdir()
    artifacts_dir = run_dir / "artifacts"
    artifacts_dir.mkdir()
    for i in range(15):
        (artifacts_dir / f"f{i}.pt").write_bytes(b"x")

    count, warnings = read_artifact_count(run_dir, max_scan=10)
    assert count == 10
    assert any("truncated" in w for w in warnings)
