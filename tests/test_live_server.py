import importlib.util
import json
import socket
import threading
import time
from urllib.request import urlopen

import pytest
import yaml

from skilllogboard.live.server import LiveServerOptions, create_live_app, load_live_template


def _call_route(app, path):
    for route in app.routes:
        if getattr(route, "path", None) == path:
            return route.endpoint()
    raise AssertionError(f"route not found: {path}")


def test_load_live_template_is_self_contained():
    html = load_live_template()

    assert "<!doctype html>" in html.lower()
    assert "/api/state" in html
    assert "https://" not in html
    assert "http://" not in html


@pytest.mark.skipif(importlib.util.find_spec("fastapi") is None, reason="fastapi not installed")
def test_live_server_state_api_run_mode(tmp_path):
    (tmp_path / "manifest.yaml").write_text(
        yaml.safe_dump({"run_id": "r1", "status": "running"}),
        encoding="utf-8",
    )
    (tmp_path / "metrics.csv").write_text(
        "timestamp,step,name,value,group,metadata_json\nt,1,val/acc,0.8,val,{}\n",
        encoding="utf-8",
    )

    app = create_live_app(tmp_path, LiveServerOptions(poll_interval=2.5))

    health = _call_route(app, "/api/health")
    assert health["mode"] == "run"
    assert health["poll_interval"] == 2.5
    assert _call_route(app, "/api/config")["poll_interval"] == 2.5
    state = _call_route(app, "/api/state")
    assert state["mode"] == "run"
    assert state["status"] == "running"


@pytest.mark.skipif(importlib.util.find_spec("fastapi") is None, reason="fastapi not installed")
def test_live_server_state_api_project_mode(tmp_path):
    run_dir = tmp_path / "run-a"
    run_dir.mkdir()
    (run_dir / "manifest.yaml").write_text(
        yaml.safe_dump({"run_id": "run-a", "status": "completed"}),
        encoding="utf-8",
    )

    app = create_live_app(tmp_path, LiveServerOptions(project=True))

    state = _call_route(app, "/api/state")
    assert state["mode"] == "project"
    assert state["runs"][0]["run_id"] == "run-a"


@pytest.mark.skipif(
    importlib.util.find_spec("fastapi") is None or importlib.util.find_spec("uvicorn") is None,
    reason="live HTTP dependencies not installed",
)
def test_live_server_http_smoke_run_mode(tmp_path):
    import uvicorn

    (tmp_path / "manifest.yaml").write_text(
        yaml.safe_dump({"run_id": "http-run", "status": "running"}),
        encoding="utf-8",
    )
    (tmp_path / "metrics.csv").write_text(
        "timestamp,step,name,value,group,metadata_json\nt,1,val/acc,0.8,val,{}\n",
        encoding="utf-8",
    )
    app = create_live_app(tmp_path, LiveServerOptions(poll_interval=1.5))
    port = _free_port()
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    try:
        _wait_for_server(server)
        health = _get_json(f"http://127.0.0.1:{port}/api/health")
        state = _get_json(f"http://127.0.0.1:{port}/api/state")
    finally:
        server.should_exit = True
        thread.join(timeout=5)

    assert health["ok"] is True
    assert health["poll_interval"] == 1.5
    assert state["mode"] == "run"
    assert state["status"] == "running"


def _free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def _wait_for_server(server):
    deadline = time.time() + 5
    while not server.started and time.time() < deadline:
        time.sleep(0.05)
    if not server.started:
        raise AssertionError("uvicorn test server did not start")


def _get_json(url):
    with urlopen(url, timeout=5) as response:
        assert response.status == 200
        return json.loads(response.read().decode("utf-8"))
