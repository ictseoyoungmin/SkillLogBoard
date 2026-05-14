from skilllogboard.cli.main import build_parser, main
from skilllogboard.live.server import LiveDependencyError


def test_watch_is_registered_command():
    help_text = build_parser().format_help()

    assert "watch" in help_text


def test_watch_no_open_does_not_open_browser(tmp_path, monkeypatch, capsys):
    calls = []

    monkeypatch.setattr("skilllogboard.live.server.require_live_dependencies", lambda: None)
    monkeypatch.setattr(
        "skilllogboard.live.server.run_live_server",
        lambda *args, **kwargs: calls.append((args, kwargs)),
    )
    monkeypatch.setattr("webbrowser.open", lambda url: calls.append(("open", url)))

    assert main(["watch", str(tmp_path), "--port", "9876", "--no-open"]) == 0

    output = capsys.readouterr().out
    assert "http://127.0.0.1:9876" in output
    assert all(call[0] != "open" for call in calls)
    assert calls[0][0][0] == tmp_path


def test_watch_auto_detects_project_root(tmp_path, monkeypatch, capsys):
    calls = []
    run_dir = tmp_path / "demo" / "run-a"
    run_dir.mkdir(parents=True)
    (run_dir / "manifest.yaml").write_text("run_id: run-a\n", encoding="utf-8")

    monkeypatch.setattr("skilllogboard.live.server.require_live_dependencies", lambda: None)
    monkeypatch.setattr(
        "skilllogboard.live.server.run_live_server",
        lambda *args, **kwargs: calls.append((args, kwargs)),
    )
    monkeypatch.setattr("webbrowser.open", lambda url: calls.append(("open", url)))

    assert main(["watch", str(tmp_path), "--port", "9876", "--no-open"]) == 0

    output = capsys.readouterr().out
    assert "enabled project mode" in output
    assert "Mode: project" in output
    assert calls[0][1]["options"].project is True


def test_watch_opens_browser_after_dependency_check(tmp_path, monkeypatch):
    calls = []

    monkeypatch.setattr("skilllogboard.live.server.require_live_dependencies", lambda: None)
    monkeypatch.setattr(
        "skilllogboard.live.server.run_live_server",
        lambda *args, **kwargs: calls.append(("server", args, kwargs)),
    )
    monkeypatch.setattr("webbrowser.open", lambda url: calls.append(("open", url)))

    assert main(["watch", str(tmp_path), "--port", "9876"]) == 0

    assert calls[0] == ("open", "http://127.0.0.1:9876")
    assert calls[1][0] == "server"


def test_watch_dependency_error_does_not_open_browser(tmp_path, monkeypatch, capsys):
    def raise_dependency_error():
        raise LiveDependencyError("install live extras")

    calls = []
    monkeypatch.setattr("skilllogboard.live.server.require_live_dependencies", raise_dependency_error)
    monkeypatch.setattr("webbrowser.open", lambda url: calls.append(("open", url)))

    assert main(["watch", str(tmp_path)]) == 2

    assert calls == []
    assert "install live extras" in capsys.readouterr().err
