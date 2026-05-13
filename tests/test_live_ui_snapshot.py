from skilllogboard.live.server import load_live_template


def test_live_ui_contains_required_sections():
    html = load_live_template()

    for label in [
        "Overview",
        "Run Status",
        "Metric Curves",
        "Rule Audit",
        "Artifact Feed",
        "Event Timeline",
        "Log Tail",
        "Project Runs",
        "Resource Summary",
    ]:
        assert label in html


def test_live_ui_uses_server_poll_interval_config():
    html = load_live_template()

    assert "/api/config" in html
    assert "refreshMs" in html
    assert "Math.max(250" in html
