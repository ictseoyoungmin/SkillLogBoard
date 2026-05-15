"""Build static report artifact packages."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any
import csv

from skilllogboard.compare.run_index import build_run_index
from skilllogboard.reports.assets import normalize_render_mode
from skilllogboard.reports.charts import chart_spec_from_artifact, write_chart_spec
from skilllogboard.reports.figure_builder import (
    OptionalFigureDependencyError,
    ReportFigure,
    build_ablation_bar_figure,
    build_metric_curve_figure,
    build_metric_curve_overlay_figure,
    build_seed_errorbar_figure,
)
from skilllogboard.reports.figures import write_svg_fallback
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
    assets: list[Path] = field(default_factory=list)
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
    (report_dir / "assets").mkdir(parents=True, exist_ok=True)
    return report_dir


def build_report_package(
    root_or_run_dir: str | Path,
    metric: str,
    mode: str = "max",
    output_dir: str | Path | None = None,
    group_by: str | list[str] | None = None,
    spec_path: str | Path | None = None,
    render_mode: str = "minimal",
    overwrite: bool = True,
) -> ReportBuildResult:
    render_mode = normalize_render_mode(render_mode)
    root = Path(root_or_run_dir)
    records = build_run_index(root)
    if not records:
        raise ValueError(f"No run folders with manifest.yaml found under {root}")
    report_dir = create_report_layout(root, output_dir)
    tables_dir = report_dir / "tables"
    figures_dir = report_dir / "figures"
    assets_dir = report_dir / "assets"
    outputs: list[ReportArtifact] = []
    warnings: list[str] = []
    table_paths: list[Path] = []
    figure_paths: list[Path] = []
    asset_paths: list[Path] = []

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
                source_files=_source_files_for_table(table, records),
                metadata=table.metadata,
                provenance=_table_provenance(table, records),
            )
        )

    figure_specs = _figure_specs(spec_path, metric, mode)
    generated_figures, skipped_figure_artifacts = _build_figures(
        specs=figure_specs,
        root=root,
        records=records,
        figures_dir=figures_dir,
        report_dir=report_dir,
        metric=metric,
        mode=mode,
        warnings=warnings,
        render_mode=render_mode,
    )
    figure_paths.extend(report_dir / artifact.path for artifact in generated_figures)
    outputs.extend(generated_figures)
    outputs.extend(skipped_figure_artifacts)
    chart_spec_paths = _write_chart_specs(
        [artifact for artifact in [*generated_figures, *skipped_figure_artifacts] if artifact.type == "figure"],
        figures_dir,
        report_dir,
        overwrite=overwrite,
    )

    report_md = report_dir / "report.md"
    report_html = report_dir / "report.html"
    manifest_path = report_dir / "report_manifest.yaml"
    asset_paths.extend(_write_report_assets(assets_dir, render_mode, overwrite=overwrite))

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
            render_mode=render_mode,
        ),
        encoding="utf-8",
    )
    outputs.extend(
        [
            ReportArtifact("report-md", "report", "report.md", "markdown", "Markdown Report", [str(root)]),
            ReportArtifact(
                "report-html",
                "report",
                "report.html",
                "html",
                "HTML Report",
                [str(root)],
                metadata={"render_mode": render_mode},
            ),
        ]
    )
    outputs.extend(_asset_artifacts(asset_paths, report_dir, render_mode))
    outputs.extend(_chart_spec_artifacts(chart_spec_paths, report_dir))
    manifest = ReportManifest(
        report_id=report_dir.name,
        source={
            "root_dir": str(root),
            "run_count": len(records),
            "source_files": [str(Path(record.get("run_dir", "")) / "manifest.yaml") for record in records],
        },
        outputs=outputs,
        parameters={
            "metric": metric,
            "mode": mode,
            "group_by": group_by,
            "spec_path": str(spec_path or ""),
            "render_mode": render_mode,
        },
        warnings=warnings,
        provenance=_package_provenance(records, outputs, metric),
    )
    write_report_manifest(manifest_path, manifest)
    return ReportBuildResult(
        report_dir=report_dir,
        report_md=report_md,
        report_html=report_html,
        report_manifest=manifest_path,
        tables=table_paths,
        figures=figure_paths,
        assets=asset_paths,
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


def _write_report_assets(assets_dir: Path, render_mode: str, overwrite: bool = True) -> list[Path]:
    if render_mode != "package":
        return []
    assets = {
        assets_dir / "report.css": _report_css(),
        assets_dir / "report.js": _report_js(),
    }
    written: list[Path] = []
    for path, content in assets.items():
        if path.exists() and not overwrite:
            raise FileExistsError(f"Report output already exists: {path}")
        path.write_text(content, encoding="utf-8")
        written.append(path)
    return written


def _asset_artifacts(asset_paths: list[Path], report_dir: Path, render_mode: str) -> list[ReportArtifact]:
    return [
        ReportArtifact(
            id=path.stem,
            type="asset",
            path=relative_artifact_path(path, report_dir),
            kind=path.suffix.lstrip("."),
            title=path.name,
            metadata={"render_mode": render_mode},
        )
        for path in asset_paths
    ]


def _write_chart_specs(
    figure_artifacts: list[ReportArtifact],
    figures_dir: Path,
    report_dir: Path,
    overwrite: bool = True,
) -> list[Path]:
    paths: list[Path] = []
    for artifact in figure_artifacts:
        path = figures_dir / f"{artifact.id}.chart.json"
        if path.exists() and not overwrite:
            raise FileExistsError(f"Report output already exists: {path}")
        write_chart_spec(path, chart_spec_from_artifact(artifact.to_dict()))
        paths.append(path)
    return paths


def _chart_spec_artifacts(chart_spec_paths: list[Path], report_dir: Path) -> list[ReportArtifact]:
    return [
        ReportArtifact(
            id=path.stem,
            type="chart-spec",
            path=relative_artifact_path(path, report_dir),
            kind="json",
            title=path.name,
            metadata={"format": "chart-spec"},
        )
        for path in chart_spec_paths
    ]


def _figure_specs(
    spec_path: str | Path | None,
    metric: str,
    mode: str,
) -> list[ReportSpecItem]:
    if spec_path:
        parsed = [item for item in parse_report_spec(spec_path) if item.kind == "figure"]
        if parsed:
            return parsed
    return [
        ReportSpecItem(
            "FIG-METRIC-CURVE-OVERLAY",
            "figure",
            "metric-curve-overlay",
            metric=metric,
            mode=mode,
            output="figures/metric-curve-overlay.png",
        )
    ]


def _build_figures(
    specs: list[ReportSpecItem],
    root: Path,
    records: list[dict[str, Any]],
    figures_dir: Path,
    report_dir: Path,
    metric: str,
    mode: str,
    warnings: list[str],
    render_mode: str,
) -> tuple[list[ReportArtifact], list[ReportArtifact]]:
    generated: list[ReportArtifact] = []
    skipped: list[ReportArtifact] = []
    for spec in specs:
        figure_path = _figure_output_path(spec, figures_dir)
        try:
            figure = _dispatch_figure(spec, root, records, figure_path, metric=metric, mode=mode)
        except OptionalFigureDependencyError as exc:
            message = f"Skipped {spec.id}: {exc}"
            if render_mode == "minimal":
                fallback_path = figure_path.with_suffix(".svg")
                write_svg_fallback(fallback_path, spec.title or spec.type.replace("-", " ").title(), message)
                warnings.append(f"Used SVG fallback for {spec.id}: {exc}")
                generated.append(_svg_fallback_figure_artifact(spec, fallback_path, report_dir, message))
            else:
                warnings.append(message)
                skipped.append(_skipped_figure_artifact(spec, figure_path, report_dir, message))
            continue
        except ValueError as exc:
            message = f"Skipped {spec.id}: {exc}"
            warnings.append(message)
            skipped.append(_skipped_figure_artifact(spec, figure_path, report_dir, message))
            continue
        generated.append(_figure_artifact(spec, figure, figure_path, report_dir))
    return generated, skipped


def _dispatch_figure(
    spec: ReportSpecItem,
    root: Path,
    records: list[dict[str, Any]],
    output_path: Path,
    metric: str,
    mode: str,
) -> ReportFigure:
    figure_type = spec.type
    selected_metric = spec.metric or metric
    if figure_type == "metric-curve-overlay":
        return build_metric_curve_overlay_figure(root, metric=selected_metric, output_path=output_path, mode=mode)
    if figure_type == "metric-curve":
        metrics = spec.metrics or [selected_metric]
        run_dir = root if (root / "manifest.yaml").exists() else Path(str(records[0].get("run_dir", "")))
        return build_metric_curve_figure(run_dir, metrics=metrics, output_path=output_path)
    if figure_type == "seed-errorbar":
        table = build_report_table(
            "seed-summary",
            records,
            metric=selected_metric,
            mode=spec.mode or mode,
            group_by=spec.group_by,
        )
        return build_seed_errorbar_figure(table.rows, output_path)
    if figure_type == "ablation-bar":
        table = build_report_table(
            "ablation-summary",
            records,
            metric=selected_metric,
            mode=spec.mode or mode,
        )
        return build_ablation_bar_figure(table.rows, output_path)
    raise ValueError(f"Unsupported report figure type: {figure_type}")


def _figure_output_path(spec: ReportSpecItem, figures_dir: Path) -> Path:
    if spec.output:
        path = Path(spec.output)
        if path.is_absolute():
            return path
        return figures_dir / path.name
    return figures_dir / f"{spec.type}.png"


def _figure_artifact(
    spec: ReportSpecItem,
    figure: ReportFigure,
    figure_path: Path,
    report_dir: Path,
) -> ReportArtifact:
    return ReportArtifact(
        id=Path(spec.output).stem if spec.output else figure.figure_id,
        type="figure",
        kind=figure.figure_type,
        title=spec.title or figure.figure_type.replace("-", " ").title(),
        path=relative_artifact_path(figure_path, report_dir),
        source_files=figure.source_files,
        metadata={**figure.metadata, "status": "generated"},
        provenance={
            "files": sorted(figure.source_files),
            "metrics": [figure.metric] if figure.metric else [],
            "columns": [],
            "step_range": figure.metadata.get("step_range"),
        },
    )


def _svg_fallback_figure_artifact(
    spec: ReportSpecItem,
    figure_path: Path,
    report_dir: Path,
    message: str,
) -> ReportArtifact:
    return ReportArtifact(
        id=Path(spec.output).stem if spec.output else spec.type,
        type="figure",
        kind=f"{spec.type}-svg-fallback",
        title=spec.title or spec.type.replace("-", " ").title(),
        path=relative_artifact_path(figure_path, report_dir),
        source_files=[],
        metadata={"status": "generated", "fallback": "svg", "warning": message},
        provenance={
            "files": [],
            "metrics": [spec.metric] if spec.metric else [],
            "columns": [],
            "step_range": None,
        },
    )


def _skipped_figure_artifact(
    spec: ReportSpecItem,
    figure_path: Path,
    report_dir: Path,
    message: str,
) -> ReportArtifact:
    return ReportArtifact(
        id=Path(spec.output).stem if spec.output else spec.type,
        type="figure",
        kind=spec.type,
        title=spec.title or spec.type.replace("-", " ").title(),
        path=relative_artifact_path(figure_path, report_dir),
        source_files=[],
        metadata={"status": "skipped", "warning": message},
        provenance={
            "files": [],
            "metrics": [spec.metric] if spec.metric else [],
            "columns": [],
            "step_range": None,
        },
    )


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


def _source_files_for_table(table: ReportTable, records: list[dict[str, Any]]) -> list[str]:
    files: list[str] = []
    for record in records:
        run_dir = Path(str(record.get("run_dir", "")))
        candidates = [run_dir / "manifest.yaml"]
        if table.metadata.get("metric"):
            candidates.append(run_dir / "metrics.csv")
        if table.table_type == "config-diff":
            candidates.append(run_dir / "config.yaml")
        if table.table_type == "rule-audit":
            candidates.append(run_dir / "skill_trace.jsonl")
        files.extend(path.as_posix() for path in candidates if path.exists())
    return sorted(set(files))


def _table_provenance(table: ReportTable, records: list[dict[str, Any]]) -> dict[str, Any]:
    metric = table.metadata.get("metric")
    metrics = [str(metric)] if metric else []
    return {
        "files": _source_files_for_table(table, records),
        "metrics": metrics,
        "columns": list(table.columns),
        "step_range": _metric_step_range(records, str(metric)) if metric else None,
        "run_ids": [str(record.get("run_id", "")) for record in records if record.get("run_id")],
        "row_count": len(table.rows),
    }


def _package_provenance(
    records: list[dict[str, Any]],
    outputs: list[ReportArtifact],
    metric: str,
) -> dict[str, Any]:
    files = sorted({file for output in outputs for file in output.source_files})
    columns = {
        output.id: output.provenance.get("columns", [])
        for output in outputs
        if output.type == "table"
    }
    return {
        "files": files,
        "metrics": [metric] if metric else [],
        "columns": columns,
        "step_range": _metric_step_range(records, metric) if metric else None,
        "run_ids": [str(record.get("run_id", "")) for record in records if record.get("run_id")],
    }


def _metric_step_range(records: list[dict[str, Any]], metric: str) -> dict[str, int] | None:
    steps: list[int] = []
    for record in records:
        metrics_path = Path(str(record.get("run_dir", ""))) / "metrics.csv"
        if metrics_path.exists():
            steps.extend(_metric_steps_from_csv(metrics_path, metric))
            continue
        value = record.get("metrics", {}).get(metric)
        if isinstance(value, dict) and isinstance(value.get("step"), int):
            steps.append(value["step"])
    if not steps:
        return None
    return {"min": min(steps), "max": max(steps)}


def _metric_steps_from_csv(path: Path, metric: str) -> list[int]:
    steps: list[int] = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for index, row in enumerate(reader):
            if row.get("name") != metric:
                continue
            try:
                steps.append(int(row.get("step") or index))
            except ValueError:
                steps.append(index)
    return steps


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
    selected = [
        artifact
        for artifact in artifacts
        if (kind is None or artifact.kind == kind) and artifact.metadata.get("status") != "skipped"
    ]
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
    render_mode: str,
) -> str:
    table_html = "\n".join(
        f'<section class="report-section"><h3>{_escape_html(table.table_id)}</h3>{table_to_html(table)}</section>'
        for table in tables
    )
    visible_figures = [
        artifact for artifact in figure_artifacts if artifact.metadata.get("status") != "skipped"
    ]
    figures = "\n".join(
        f'<figure><img src="{_escape_html(artifact.path)}" alt="{_escape_html(artifact.title)}"></figure>'
        for artifact in visible_figures
    )
    run_items = "\n".join(
        f"<li>{_escape_html(str(record.get('run_id', '')))} - {_escape_html(str(record.get('status', '')))}</li>"
        for record in records
    )
    warning_items = "\n".join(f"<li>{_escape_html(warning)}</li>" for warning in warnings) or "<li>None</li>"
    head_assets = _html_assets(render_mode)
    table_filter = (
        '<label class="filter-label">Filter tables <input type="search" id="table-filter" '
        'placeholder="run id, metric, status"></label>'
        if render_mode in {"portable_interactive", "package"}
        else ""
    )
    package_note = "Portable package" if render_mode == "package" else "Offline report"
    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SkillLogBoard Report</title>
{head_assets}
</head>
<body>
<header class="report-header"><p>{_escape_html(package_note)}</p><h1>SkillLogBoard Report</h1></header>
<section><h2>Summary</h2><p>Metric: <code>{_escape_html(metric)}</code>, mode: <code>{_escape_html(mode)}</code></p></section>
<section><h2>Key Findings</h2><p>TODO: Add human-authored findings based on the generated evidence.</p></section>
<section><h2>Source Runs</h2><ul>{run_items}</ul></section>
<section><h2>Tables</h2>{table_filter}{table_html}</section>
<section><h2>Figures</h2>{figures or '<p>No figures generated.</p>'}</section>
<section><h2>Provenance</h2><p>See <code>report_manifest.yaml</code>.</p></section>
<section><h2>Warnings</h2><ul>{warning_items}</ul></section>
</body>
</html>
"""


def _html_assets(render_mode: str) -> str:
    if render_mode == "package":
        return '<link rel="stylesheet" href="assets/report.css">\n<script defer src="assets/report.js"></script>'
    css = f"<style>\n{_report_css()}\n</style>"
    if render_mode == "portable_interactive":
        return f"{css}\n<script>\n{_report_js()}\n</script>"
    return css


def _report_css() -> str:
    return """body { font-family: system-ui, sans-serif; margin: 2rem; color: #1f2933; background: #fbfcfd; }
.report-header { border-bottom: 1px solid #d5dbe3; margin-bottom: 1.5rem; padding-bottom: 1rem; }
.report-header p { color: #5f6b7a; font-size: 0.9rem; margin: 0 0 0.25rem; text-transform: uppercase; }
h1, h2, h3 { line-height: 1.2; }
section { margin: 1.5rem 0; }
.report-section { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; margin: 1rem 0 2rem; background: white; }
th, td { border: 1px solid #d5dbe3; padding: 0.45rem; text-align: left; }
th { background: #f4f6f8; }
img { max-width: 100%; height: auto; }
code { background: #eef2f5; padding: 0.1rem 0.25rem; }
.filter-label { display: block; color: #344054; font-weight: 600; margin: 0.5rem 0 1rem; }
.filter-label input { display: block; width: min(32rem, 100%); margin-top: 0.35rem; padding: 0.45rem 0.55rem; border: 1px solid #b8c1cc; border-radius: 6px; }
@media (max-width: 720px) { body { margin: 1rem; } th, td { padding: 0.35rem; } }"""


def _report_js() -> str:
    return """document.addEventListener('DOMContentLoaded', function () {
  var input = document.getElementById('table-filter');
  if (!input) return;
  input.addEventListener('input', function () {
    var query = input.value.toLowerCase();
    document.querySelectorAll('tbody tr').forEach(function (row) {
      row.hidden = query && !row.textContent.toLowerCase().includes(query);
    });
  });
});"""


def _make_report_id() -> str:
    return "report-" + datetime.now().strftime("%Y%m%d-%H%M%S")


def _escape_html(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
