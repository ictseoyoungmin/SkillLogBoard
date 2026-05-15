from pathlib import Path

import pytest

from skilllogboard.reports.report_spec import ReportSpecParseError, parse_report_spec_text


def test_parse_report_spec_blocks_in_order():
    items = parse_report_spec_text(
        """
# ReportSpec

## REPORT-MAIN
- title: Demo Report
- output: report/report.md

## TABLE-LEADERBOARD
- type: leaderboard
- metric: val/acc
- mode: max
- output: report/tables/leaderboard.md
- baseline_run_id: baseline
- reference_run_id: candidate
- delta_mode: absolute

## FIG-CURVE
- type: metric-curve
- metrics: [train/loss, val/acc]
- output: report/figures/curve.png
"""
    )

    assert [item.id for item in items] == ["REPORT-MAIN", "TABLE-LEADERBOARD", "FIG-CURVE"]
    assert items[0].kind == "report"
    assert items[1].kind == "table"
    assert items[1].metric == "val/acc"
    assert items[1].baseline_run_id == "baseline"
    assert items[1].reference_run_id == "candidate"
    assert items[1].delta_mode == "absolute"
    assert items[2].kind == "figure"
    assert items[2].metrics == ["train/loss", "val/acc"]


def test_report_spec_malformed_metadata_is_readable():
    with pytest.raises(ReportSpecParseError, match="Malformed report spec metadata"):
        parse_report_spec_text("## TABLE-BAD\n- missing-colon\n")


def test_example_report_specs_parse():
    for path in Path("examples/report_specs").glob("*.md"):
        assert parse_report_spec_text(path.read_text(encoding="utf-8"))
