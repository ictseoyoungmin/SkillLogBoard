from skilllogboard.reports.report_manifest import (
    ReportArtifact,
    ReportManifest,
    read_report_manifest,
    write_report_manifest,
)


def test_report_artifact_schema_is_serializable():
    artifact = ReportArtifact(
        id="leaderboard",
        type="table",
        path="tables/leaderboard.md",
        kind="leaderboard",
        title="Leaderboard",
        source_files=["runs/demo/a/metrics.csv"],
        metadata={"metric": "val/acc"},
    )

    data = artifact.to_dict()

    assert data["type"] == "table"
    assert data["kind"] == "leaderboard"
    assert data["metadata"]["metric"] == "val/acc"


def test_report_manifest_roundtrip(tmp_path):
    manifest = ReportManifest(
        report_id="report-demo",
        source={"root_dir": "runs/demo", "run_count": 2},
        outputs=[
            ReportArtifact("leaderboard", "table", "tables/leaderboard.md", "leaderboard"),
            ReportArtifact("curve", "figure", "figures/curve.png", "metric-curve"),
        ],
        parameters={"metric": "val/acc"},
        warnings=["figure skipped"],
    )
    path = write_report_manifest(tmp_path / "report_manifest.yaml", manifest)

    loaded = read_report_manifest(path)

    assert loaded["report_id"] == "report-demo"
    assert loaded["source"]["run_count"] == 2
    assert {item["type"] for item in loaded["outputs"]} == {"table", "figure"}
    assert loaded["warnings"] == ["figure skipped"]
