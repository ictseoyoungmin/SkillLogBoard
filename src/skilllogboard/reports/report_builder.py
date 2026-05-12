"""Build static report artifact packages."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from skilllogboard.compare.run_index import build_run_index
from skilllogboard.reports.figure_builder import (
    OptionalFigureDependencyError,
    build_metric_curve_overlay_figure,
)
from skilllogboard.reports.report_manifest import (
    ReportArtifact,
    ReportManifest,
    relative_artifact_path,
    write_report_manifest,
)
from skilllogboard.reports.report_spec import ReportSpecItem, parse_report_spec
from skilllogboard.reports.table_builder import (
    ReportTable,
    build_report_table,
    table_to_csv_string,
    table_to_html,
    table_to_latex,
    table_to_markdown,
)


@dataclass
class ReportBuildResult:
    report_dir: Path
    report_md: Path
    report_html: Path
    report_manifest: Path
    tables: list[Path] = field(default_factory=list)
    figures: list[Path] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    outputs: list[ReportArtifact] = field(default_factory=list)


def create_report_layout(root_or_run_dir: str | Path, output_dir: str | Path | None = None) -> Path:
    root = Path(root_or_run_dir)
    if output_dir is not None:
        report_dir = Path(output_dir)
    elif (root / "manifest.yaml").exists():
        report_dir = root / "report"
    else:
        report_dir = root / "_reports" / _make_report_id()
    (report_dir / "tables").mkdir(parents=True, exist_ok=True)
    (report_dir / "figures").mkdir(parents=True, exist_ok=True)
    return report_dir


def build_report_package(
    root_or_run_dir: str | Path,
    metric: str,
    mode: str = "max",
    output_dir: str | Path | None = None,
    group_by: str | list[str] | None = None,
    spec_path: str | Path | None = None,
    overwrite: bool = True,
) -> ReportBuildResult:
    root = Path(root_or_run_dir)
    records = build_run_index(root)
    if not records:
        raise ValueError(f"No run folders with manifest.yaml found under {root}")
    report_dir = create_report_layout(root, output_dir)
    tables_dir = report_dir / "tables"
    figures_dir = report_dir / "figures"
    outputs: list[ReportArtifact] = []
    warnings: list[str] = []
    table_paths: list[Path] = []
    figure_paths: list[Path] = []

    table_specs = _table_specs(spec_path, metric, mode, group_by)
    generated_tables: list[ReportTable] = []
    for spec in table_specs:
        table = build_report_table(
            spec.type,
            records,
            metric=spec.metric or metric,
            mode=spec.mode or mode,
            group_by=spec.group_by or group_by,
        )
        table.table_id = _table_id(spec, table)
        generated_tables.append(table)
        table_paths.extend(_write_table_bundle(table, tables_dir, overwrite=overwrite))
        outputs.append(
            ReportArtifact(
                id=table.table_id,
                type="table",
                kind=table.table_type,
                title=spec.title or table.table_id,
                path=relative_artifact_path(tables_dir / f"{table.table_id}.md", report_dir),
                source_files=[str(root)],
                metadata=table.metadata,
            )
        )

    try:
        figure_path = figures_dir / "metric-curve-overlay.png"
        figure = build_metric_curve_overlay_figure(root, metric=metric, output_path=figure_path, mode=mode)
        figure_paths.append(figure_path)
        outputs.append(
            ReportArtifact(
                id=figure.figure_id,
                type="figure",
                kind=figure.figure_type,
                title=f"Metric Curve Overlay: {metric}",
                path=relative_artifact_path(figure_path, report_dir),
                source_files=figure.source_files,
                metadata=figure.metadata,
            )
        )
    except OptionalFigureDependencyError as exc:
        warnings.append(str(exc))
    except ValueError as exc:
        warnings.append(str(exc))

    report_md = report_dir / "report.md"
    report_html = report_dir / "report.html"
    manifest_path = report_dir / "report_manifest.yaml"

    report_md.write_text(
        _render_markdown_report(
            records=records,
            metric=metric,
            mode=mode,
            table_artifacts=[artifact for artifact in outputs if artifact.type == "table"],
            figure_artifacts=[artifact for artifact in outputs if artifact.type == "figure"],
            warnings=warnings,
        ),
        encoding="utf-8",
    )
    report_html.write_text(
        _render_html_report(
            records=records,
            metric=metric,
            mode=mode,
            tables=generated_tables,
            figure_artifacts=[artifact for artifact in outputs if artifact.type == "figure"],
            warnings=warnings,
        ),
        encoding="utf-8",
    )
    outputs.extend(
        [
            ReportArtifact("report-md", "report", "report.md", "markdown", "Markdown Report", [str(root)]),
            ReportArtifact("report-html", "report", "report.html", "html", "HTML Report", [str(root)]),
        ]
    )
    manifest = ReportManifest(
        report_id=report_dir.name,
        source={
            "root_dir": str(root),
            "run_count": len(records),
            "source_files": [str(Path(record.get("run_dir", "")) / "manifest.yaml") for record in records],
        },
        outputs=outputs,
        parameters={"metric": metric, "mode": mode, "group_by": group_by, "spec_path": str(spec_path or "")},
        warnings=warnings,
    )
    write_report_manifest(manifest_path, manifest)
    return ReportBuildResult(
        report_dir=report_dir,
        report_md=report_md,
        report_html=report_html,
        report_manifest=manifest_path,
        tables=table_paths,
        figures=figure_paths,
        warnings=warnings,
        outputs=outputs,
    )


def _table_specs(
    spec_path: str | Path | None,
    metric: str,
    mode: str,
    group_by: str | list[str] | None,
) -> list[ReportSpecItem]:
    if spec_path:
        parsed = [item for item in parse_report_spec(spec_path) if item.kind == "table"]
        if parsed:
            return parsed
    group_keys = [group_by] if isinstance(group_by, str) else list(group_by or [])
    return [
        ReportSpecItem("TABLE-LEADERBOARD", "table", "leaderboard", metric=metric, mode=mode),
        ReportSpecItem(
            "TABLE-SEED-SUMMARY",
            "table",
            "seed-summary",
            metric=metric,
            mode=mode,
            group_by=group_keys,
        ),
        ReportSpecItem("TABLE-ABLATION-SUMMARY", "table", "ablation-summary", metric=metric, mode=mode),
        ReportSpecItem("TABLE-RULE-AUDIT", "table", "rule-audit"),
    ]


def _table_id(spec: ReportSpecItem, table: ReportTable) -> str:
    if spec.output:
        return Path(spec.output).stem
    return table.table_id


def _write_table_bundle(table: ReportTable, tables_dir: Path, overwrite: bool = True) -> list[Path]:
    paths = [
        tables_dir / f"{table.table_id}.md",
        tables_dir / f"{table.table_id}.csv",
        tables_dir / f"{table.table_id}.tex",
    ]
    contents = [table_to_markdown(table) + "\n", table_to_csv_string(table), table_to_latex(table) + "\n"]
    for path, content in zip(paths, contents):
        if path.exists() and not overwrite:
            raise FileExistsError(f"Report output already exists: {path}")
        path.write_text(content, encoding="utf-8")
    return paths


def _render_markdown_report(
    records: list[dict[str, Any]],
    metric: str,
    mode: str,
    table_artifacts: list[ReportArtifact],
    figure_artifacts: list[ReportArtifact],
    warnings: list[str],
) -> str:
    lines = [
        "# SkillLogBoard Report",
        "",
        "## Summary",
        "",
        f"- Source runs: `{len(records)}`",
        f"- Metric: `{metric}`",
        f"- Mode: `{mode}`",
        "",
        "## Key Findings",
        "",
        "- TODO: Add human-authored findings based on the generated evidence.",
        "",
        "## Source Runs",
        "",
        "| Run ID | Run Name | Status |",
        "|---|---|---|",
    ]
    for record in records:
        lines.append(
            f"| `{record.get('run_id', '')}` | `{record.get('run_name', '')}` | `{record.get('status', '')}` |"
        )
    lines.extend(["", "## Leaderboard", ""])
    _append_artifact_links(lines, table_artifacts, "leaderboard")
    lines.extend(["", "## Tables", ""])
    _append_artifact_links(lines, table_artifacts)
    lines.extend(["", "## Figures", ""])
    _append_artifact_links(lines, figure_artifacts)
    lines.extend(["", "## Rule Audit", ""])
    _append_artifact_links(lines, table_artifacts, "rule-audit")
    lines.extend(["", "## Provenance", "", "- `report_manifest.yaml`", ""])
    lines.extend(["## Warnings", ""])
    if warnings:
        lines.extend(f"- {warning}" for warning in warnings)
    else:
        lines.append("- None")
    lines.append("")
    return "\n".join(lines)


def _append_artifact_links(
    lines: list[str],
    artifacts: list[ReportArtifact],
    kind: str | None = None,
) -> None:
    selected = [artifact for artifact in artifacts if kind is None or artifact.kind == kind]
    if not selected:
        lines.append("No artifacts generated for this section.")
        return
    for artifact in selected:
        lines.append(f"- [{artifact.title or artifact.id}]({artifact.path})")


def _render_html_report(
    records: list[dict[str, Any]],
    metric: str,
    mode: str,
    tables: list[ReportTable],
    figure_artifacts: list[ReportArtifact],
    warnings: list[str],
) -> str:
    table_html = "\n".join(
        f"<section><h3>{_escape_html(table.table_id)}</h3>{table_to_html(table)}</section>"
        for table in tables
    )
    figures = "\n".join(
        f'<figure><img src="{_escape_html(artifact.path)}" alt="{_escape_html(artifact.title)}"></figure>'
        for artifact in figure_artifacts
    )
    run_items = "\n".join(
        f"<li>{_escape_html(str(record.get('run_id', '')))} - {_escape_html(str(record.get('status', '')))}</li>"
        for record in records
    )
    warning_items = "\n".join(f"<li>{_escape_html(warning)}</li>" for warning in warnings) or "<li>None</li>"
    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>SkillLogBoard Report</title>
<style>
body {{ font-family: system-ui, sans-serif; margin: 2rem; color: #1f2933; }}
table {{ border-collapse: collapse; width: 100%; margin: 1rem 0 2rem; }}
th, td {{ border: 1px solid #d5dbe3; padding: 0.45rem; text-align: left; }}
th {{ background: #f4f6f8; }}
img {{ max-width: 100%; height: auto; }}
code {{ background: #eef2f5; padding: 0.1rem 0.25rem; }}
</style>
</head>
<body>
<h1>SkillLogBoard Report</h1>
<section><h2>Summary</h2><p>Metric: <code>{_escape_html(metric)}</code>, mode: <code>{_escape_html(mode)}</code></p></section>
<section><h2>Key Findings</h2><p>TODO: Add human-authored findings based on the generated evidence.</p></section>
<section><h2>Source Runs</h2><ul>{run_items}</ul></section>
<section><h2>Tables</h2>{table_html}</section>
<section><h2>Figures</h2>{figures or '<p>No figures generated.</p>'}</section>
<section><h2>Provenance</h2><p>See <code>report_manifest.yaml</code>.</p></section>
<section><h2>Warnings</h2><ul>{warning_items}</ul></section>
</body>
</html>
"""


def _make_report_id() -> str:
    return "report-" + datetime.now().strftime("%Y%m%d-%H%M%S")


def _escape_html(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
