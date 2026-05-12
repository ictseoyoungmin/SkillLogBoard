from skilllogboard import RunLogger
from skilllogboard.reports.report_builder import build_report_package, create_report_layout
from skilllogboard.reports.report_manifest import read_report_manifest
from tests.helpers import assert_html_document


def _make_runs(tmp_path):
    runs_root = tmp_path / "runs"
    for seed, acc in [(1, 0.7), (2, 0.9)]:
        logger = RunLogger(
            project="demo",
            run_name=f"seed-{seed}",
            root_dir=runs_root,
            config={"model": "Tiny", "seed": seed},
            main_metric={"name": "val/acc", "mode": "max"},
        )
        logger.log_metric("val/acc", acc, step=seed)
        logger.finish()
    return runs_root


def test_create_report_layout_uses_explicit_output_dir(tmp_path):
    out = create_report_layout(tmp_path / "runs", output_dir=tmp_path / "report-out")

    assert (out / "tables").exists()
    assert (out / "figures").exists()


def test_build_report_package_writes_reports_and_manifest(tmp_path):
    runs_root = _make_runs(tmp_path)
    out_dir = tmp_path / "report"

    result = build_report_package(
        runs_root,
        metric="val/acc",
        mode="max",
        output_dir=out_dir,
        group_by=["model"],
    )

    assert result.report_md.exists()
    assert result.report_html.exists()
    assert result.report_manifest.exists()
    assert (out_dir / "tables" / "leaderboard.md").exists()
    assert "## Key Findings" in result.report_md.read_text(encoding="utf-8")
    assert_html_document(result.report_html.read_text(encoding="utf-8"))
    manifest = read_report_manifest(result.report_manifest)
    assert manifest["source"]["run_count"] == 2
    assert any(output["type"] == "table" for output in manifest["outputs"])
    assert manifest["parameters"]["metric"] == "val/acc"


def test_build_report_package_executes_spec_fig_blocks_or_records_skip(tmp_path):
    runs_root = _make_runs(tmp_path)
    spec = tmp_path / "ReportSpec.md"
    spec.write_text(
        """
## TABLE-LEADERBOARD
- type: leaderboard
- metric: val/acc
- output: report/tables/custom_leaderboard.md

## FIG-OVERLAY
- type: metric-curve-overlay
- metric: val/acc
- output: report/figures/custom_overlay.png
""",
        encoding="utf-8",
    )
    out_dir = tmp_path / "report"

    result = build_report_package(
        runs_root,
        metric="val/acc",
        output_dir=out_dir,
        spec_path=spec,
    )

    assert (out_dir / "tables" / "custom_leaderboard.md").exists()
    manifest = read_report_manifest(result.report_manifest)
    figures = [output for output in manifest["outputs"] if output["type"] == "figure"]
    assert figures
    assert figures[0]["kind"] == "metric-curve-overlay"
    assert figures[0]["metadata"]["status"] in {"generated", "skipped"}
    if figures[0]["metadata"]["status"] == "skipped":
        assert result.warnings
