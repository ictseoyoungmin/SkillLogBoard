from skilllogboard.core.manifest import Manifest, load_manifest


def test_manifest_save(tmp_path):
    m = Manifest(project="demo", run_name="baseline", run_id="run1", run_dir=str(tmp_path))
    path = tmp_path / "manifest.yaml"
    m.save(path)
    data = load_manifest(path)
    assert data["project"] == "demo"
    assert data["status"] == "running"
