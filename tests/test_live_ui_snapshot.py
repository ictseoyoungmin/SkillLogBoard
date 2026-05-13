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
