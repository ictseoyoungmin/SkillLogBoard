def test_reports_public_api_exports_documented_names():
    from skilllogboard.reports import (
        OptionalFigureDependencyError,
        ReportArtifact,
        ReportBuildResult,
        ReportFigure,
        ReportManifest,
        ReportSpecItem,
        ReportTable,
        build_metric_curve_overlay_figure,
        build_report_package,
        build_report_table,
        create_report_layout,
        parse_report_spec_text,
        read_report_manifest,
        table_to_markdown,
        write_report_manifest,
    )

    assert ReportArtifact
    assert ReportBuildResult
    assert ReportFigure
    assert ReportManifest
    assert ReportSpecItem
    assert ReportTable
    assert OptionalFigureDependencyError
    assert callable(build_metric_curve_overlay_figure)
    assert callable(build_report_package)
    assert callable(build_report_table)
    assert callable(create_report_layout)
    assert callable(parse_report_spec_text)
    assert callable(read_report_manifest)
    assert callable(table_to_markdown)
    assert callable(write_report_manifest)
