import importlib.util
import json
import socket
import threading
import time
from urllib.request import urlopen

import pytest
import yaml

from skilllogboard.live.server import (
    LiveServerOptions,
    create_live_app,
    load_live_app_html,
    load_live_template,
)


def _call_route(app, path, **kwargs):
    for route in app.routes:
        if getattr(route, "path", None) == path:
            return route.endpoint(**kwargs)
    raise AssertionError(f"route not found: {path}")


def test_load_live_template_is_self_contained():
    html = load_live_template()

    assert "<!doctype html>" in html.lower()
    assert "/api/state" in html
    assert "https://" not in html
    assert "http://" not in html


def test_load_live_app_html_has_fallback_or_compiled_app():
    html = load_live_app_html()

    assert "<!doctype html>" in html.lower()
    assert "SkillLogBoard Live" in html


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
    assert health["default_view"] == "lab"
    assert health["poll_interval"] == 2.5
    config = _call_route(app, "/api/config")
    assert config["poll_interval"] == 2.5
    assert config["default_view"] == "lab"
    state = _call_route(app, "/api/state")
    assert state["mode"] == "run"
    assert state["status"] == "running"
    assert state["current_view"] == "lab"


@pytest.mark.skipif(importlib.util.find_spec("fastapi") is None, reason="fastapi not installed")
def test_live_server_state_api_project_mode(tmp_path):
    run_dir = tmp_path / "run-a"
    run_dir.mkdir()
    (run_dir / "manifest.yaml").write_text(
        yaml.safe_dump({"run_id": "run-a", "status": "completed"}),
        encoding="utf-8",
    )

    app = create_live_app(tmp_path, LiveServerOptions(project=True))

    assert _call_route(app, "/api/config")["default_view"] == "overview"
    state = _call_route(app, "/api/state")
    assert state["mode"] == "project"
    assert state["current_view"] == "overview"
    assert state["runs"][0]["run_id"] == "run-a"
    compare = _call_route(app, "/api/compare")
    assert compare["runs"][0]["run_id"] == "run-a"


@pytest.mark.skipif(importlib.util.find_spec("fastapi") is None, reason="fastapi not installed")
def test_live_server_view_scoped_project_state(tmp_path):
    for run_id, value in [("run-a", 0.8), ("run-b", 0.9)]:
        run_dir = tmp_path / run_id
        run_dir.mkdir()
        (run_dir / "manifest.yaml").write_text(
            yaml.safe_dump({"run_id": run_id, "status": "completed"}),
            encoding="utf-8",
        )
        (run_dir / "metrics.csv").write_text(
            "timestamp,step,name,value,group,metadata_json\n"
            f"t,1,val/acc,{value},val,{{}}\n",
            encoding="utf-8",
        )
    app = create_live_app(tmp_path, LiveServerOptions(project=True))

    overview = _call_route(app, "/api/state", view="overview")
    compare = _call_route(app, "/api/state", view="compare")

    assert overview["payload_scope"] == "summary"
    assert overview["compare"]["series"] == []
    assert compare["payload_scope"] == "series"
    assert compare["compare"]["series"]


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
        html = _get_text(f"http://127.0.0.1:{port}/")
    finally:
        server.should_exit = True
        thread.join(timeout=5)

    assert health["ok"] is True
    assert health["poll_interval"] == 1.5
    assert state["mode"] == "run"
    assert state["status"] == "running"
    assert "SkillLogBoard Live" in html
    assert 'data-skilllogboard-ui="v1.1.1"' in html or 'data-skilllogboard-ui="v1.3-react"' in html


@pytest.mark.skipif(importlib.util.find_spec("fastapi") is None, reason="fastapi not installed")
def test_live_server_compare_api_project_mode(tmp_path):
    for run_id, value in [("baseline", 0.7), ("candidate", 0.8)]:
        run_dir = tmp_path / run_id
        run_dir.mkdir()
        (run_dir / "manifest.yaml").write_text(
            yaml.safe_dump(
                {
                    "run_id": run_id,
                    "status": "completed",
                    "best_metric": {"name": "val/acc", "value": value},
                }
            ),
            encoding="utf-8",
        )
        (run_dir / "metrics.csv").write_text(
            "timestamp,step,name,value,group,metadata_json\n"
            f"t,1,val/acc,{value},val,{{}}\n"
            f"t,2,val/acc,{value + 0.01},val,{{}}\n",
            encoding="utf-8",
        )

    app = create_live_app(tmp_path, LiveServerOptions(project=True))

    compare = _call_route(
        app,
        "/api/compare",
        metric="val/acc",
        runs="candidate",
        normalize=True,
        align="relative",
    )

    assert compare["selected_run_ids"] == ["candidate"]
    assert compare["normalize"] is True
    assert compare["series"][0]["points"][0]["x"] == 0


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


def _get_text(url):
    with urlopen(url, timeout=5) as response:
        assert response.status == 200
        return response.read().decode("utf-8")
