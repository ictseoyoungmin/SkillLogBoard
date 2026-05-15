"""Report builders and portable report artifact helpers."""

from skilllogboard.reports.figure_builder import (
    OptionalFigureDependencyError,
    ReportFigure,
    build_ablation_bar_figure,
    build_metric_curve_figure,
    build_metric_curve_overlay_figure,
    build_seed_errorbar_figure,
)
from skilllogboard.reports.report_builder import (
    ReportBuildResult,
    build_report_package,
    create_report_layout,
)
from skilllogboard.reports.report_manifest import (
    ReportArtifact,
    ReportManifest,
    read_report_manifest,
    validate_report_manifest_schema,
    write_report_manifest,
)
from skilllogboard.reports.report_spec import (
    ReportSpecItem,
    parse_report_spec,
    parse_report_spec_text,
)
from skilllogboard.reports.table_builder import (
    ReportTable,
    build_report_table,
    table_to_csv_string,
    table_to_latex,
    table_to_markdown,
)
from skilllogboard.reports.validate import (
    ReportValidationResult,
    validate_report_package,
    validation_summary,
)

__all__ = [
    "OptionalFigureDependencyError",
    "ReportArtifact",
    "ReportBuildResult",
    "ReportFigure",
    "ReportManifest",
    "ReportSpecItem",
    "ReportTable",
    "ReportValidationResult",
    "build_ablation_bar_figure",
    "build_metric_curve_figure",
    "build_metric_curve_overlay_figure",
    "build_report_package",
    "build_report_table",
    "build_seed_errorbar_figure",
    "create_report_layout",
    "parse_report_spec",
    "parse_report_spec_text",
    "read_report_manifest",
    "table_to_csv_string",
    "table_to_latex",
    "table_to_markdown",
    "validate_report_manifest_schema",
    "validate_report_package",
    "validation_summary",
    "write_report_manifest",
]
