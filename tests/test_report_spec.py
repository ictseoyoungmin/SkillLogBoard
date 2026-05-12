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
    assert items[2].kind == "figure"
    assert items[2].metrics == ["train/loss", "val/acc"]


def test_report_spec_malformed_metadata_is_readable():
    with pytest.raises(ReportSpecParseError, match="Malformed report spec metadata"):
        parse_report_spec_text("## TABLE-BAD\n- missing-colon\n")
