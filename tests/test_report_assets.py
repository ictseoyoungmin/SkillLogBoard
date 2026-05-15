from skilllogboard.reports.assets import check_static_html_safety, resolve_asset_path


def test_resolve_asset_path_stays_inside_report_dir(tmp_path):
    report_dir = tmp_path / "report"
    report_dir.mkdir()

    assert resolve_asset_path(report_dir, "assets/report.css") == report_dir / "assets" / "report.css"

    try:
        resolve_asset_path(report_dir, "../escape.css")
    except ValueError as exc:
        assert "escapes" in str(exc)
    else:
        raise AssertionError("escaping asset path should fail")


def test_static_html_safety_rejects_external_references():
    issues = check_static_html_safety('<link href="https://cdn.example/style.css"><img src="figures/a.svg">')

    assert issues
    assert issues[0].severity == "error"
