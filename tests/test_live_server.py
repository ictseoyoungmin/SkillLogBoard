import importlib.util

import pytest
import yaml

from skilllogboard.live.server import LiveServerOptions, create_live_app, load_live_template


def test_load_live_template_is_self_contained():
    html = load_live_template()

    assert "<!doctype html>" in html.lower()
    assert "/api/state" in html
    assert "https://" not in html
    assert "http://" not in html


@pytest.mark.skipif(importlib.util.find_spec("fastapi") is None, reason="fastapi not installed")
def test_live_server_state_api_run_mode(tmp_path):
    from fastapi.testclient import TestClient

    (tmp_path / "manifest.yaml").write_text(
        yaml.safe_dump({"run_id": "r1", "status": "running"}),
        encoding="utf-8",
    )
    (tmp_path / "metrics.csv").write_text(
        "timestamp,step,name,value,group,metadata_json\nt,1,val/acc,0.8,val,{}\n",
        encoding="utf-8",
    )

    client = TestClient(create_live_app(tmp_path))

    assert client.get("/api/health").json()["mode"] == "run"
    state = client.get("/api/state").json()
    assert state["mode"] == "run"
    assert state["status"] == "running"


@pytest.mark.skipif(importlib.util.find_spec("fastapi") is None, reason="fastapi not installed")
def test_live_server_state_api_project_mode(tmp_path):
    from fastapi.testclient import TestClient

    run_dir = tmp_path / "run-a"
    run_dir.mkdir()
    (run_dir / "manifest.yaml").write_text(
        yaml.safe_dump({"run_id": "run-a", "status": "completed"}),
        encoding="utf-8",
    )

    client = TestClient(create_live_app(tmp_path, LiveServerOptions(project=True)))

    state = client.get("/api/state").json()
    assert state["mode"] == "project"
    assert state["runs"][0]["run_id"] == "run-a"
