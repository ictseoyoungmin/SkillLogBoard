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
        'data-skilllogboard-ui="v1.1.1"',
        "Metric Workspace",
        "Chart transform controls",
        "Bottom context tray",
        "Run detail drawer",
        "Full screen metric lab",
        "localStorage",
        "skilllogboard.live.ui.v1.1.1",
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


def test_live_ui_contains_v111_compare_and_polish_contracts():
    html = load_live_template()

    for snippet in [
        'data-live-action="toggle-compare"',
        'data-live-action="open-run-picker"',
        'data-live-action="toggle-tray"',
        'data-live-region="compare-legend"',
        'data-live-region="artifact-preview"',
        'data-compare-run-picker',
        "Run Picker",
        "Artifact Preview",
        "Normalized",
        "tray-collapsed",
        "toggle-side-panel",
        "/api/compare",
    ]:
        assert snippet in html


def test_live_ui_contains_v112_showcase_contracts():
    html = load_live_template()

    for snippet in [
        'data-live-region="capability-hints"',
        'data-live-region="metric-summary"',
        'data-live-region="compare-banner"',
        'data-live-region="chart-affordance"',
        'data-live-region="artifact-groups"',
        'data-live-region="agent-showcase"',
        'data-live-region="agent-empty"',
        "Compare mode",
        "Shared",
        "Log scale clamps non-positive values",
        "python examples/live_demo.py --multi-run --runs 5 --rich",
    ]:
        assert snippet in html


def test_live_ui_contains_v12_app_shell_contracts():
    html = load_live_template()

    for snippet in [
        'data-app-shell-version="v1.2"',
        'data-current-view="loading"',
        'data-view-button="overview"',
        'data-view-button="runs"',
        'data-view-button="compare"',
        'data-view-button="lab"',
        'data-view-button="artifacts"',
        'data-view-button="reports"',
        'data-view-button="agent"',
        'data-view-button="settings"',
        'data-view-panel="overview"',
        'data-view-panel="runs"',
        'data-view-panel="compare"',
        'data-view-panel="lab"',
        'data-view-panel="artifacts"',
        'data-view-panel="reports"',
        'data-view-panel="agent"',
        'data-view-panel="settings"',
        "Local Settings",
        "Local files only",
        "series loads only for this view",
        "view=", 
    ]:
        assert snippet in html


def test_live_ui_avoids_cloud_account_language():
    html = load_live_template().lower()

    for forbidden in ["avatar", "team", "invite", "organization", "cloud project"]:
        assert forbidden not in html


def test_live_ui_guided_empty_states_are_actionable():
    html = load_live_template()

    for snippet in [
        "Start a local run or create a rich demo",
        "Watch a project folder",
        "Build a report",
        "Add local agent/actions.jsonl",
        "--log-file train.log",
    ]:
        assert snippet in html
