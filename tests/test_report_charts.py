import json

from skilllogboard.reports.charts import chart_spec_from_artifact, write_chart_spec


def test_chart_spec_from_figure_artifact(tmp_path):
    spec = chart_spec_from_artifact(
        {
            "id": "curve",
            "kind": "metric-curve-overlay",
            "path": "figures/curve.png",
            "provenance": {"metrics": ["val/acc"], "files": ["runs/a/metrics.csv"]},
        }
    )
    out = write_chart_spec(tmp_path / "curve.chart.json", spec)

    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["metric"] == "val/acc"
    assert data["encoding"]["x"] == "step"
