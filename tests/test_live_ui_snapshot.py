from skilllogboard.live.server import load_live_template


def test_live_ui_contains_required_sections():
    html = load_live_template()

    for label in [
        "Overview",
        "Metric Workspace",
        "Rule Audit",
        "Artifact Feed",
        "Log Tail",
        "Project Runs",
        "Agent Workspace",
    ]:
        assert label in html


def test_live_ui_uses_server_poll_interval_config():
    html = load_live_template()

    assert "/api/config" in html
    assert "refreshMs" in html
    assert "Math.max(250" in html


def test_live_ui_contains_v11_workspace_regions_and_controls():
    html = load_live_template()

    for snippet in [
        'data-skilllogboard-ui="v1.1"',
        "Metric Workspace",
        "Chart transform controls",
        "Bottom context tray",
        "Run detail drawer",
        "Full screen metric lab",
        "localStorage",
        "skilllogboard.live.ui.v1",
        "Compare",
        "Pin",
        "Reset",
    ]:
        assert snippet in html


def test_live_ui_has_accessible_names_and_no_external_assets():
    html = load_live_template()

    for snippet in [
        'aria-label="Live Board tools"',
        'aria-label="Metric Workspace"',
        'role="tablist"',
        'role="alert"',
        'aria-label="Close run detail drawer"',
    ]:
        assert snippet in html
    assert "https://" not in html
    assert "http://" not in html
