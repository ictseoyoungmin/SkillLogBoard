"""Static dashboard builder."""

from __future__ import annotations

from importlib import resources
from pathlib import Path
import html

from skilllogboard.dashboards.components import (
    load_run_context,
    render_artifact_table,
    render_best_metric_card,
    render_config_table,
    render_metric_panel,
)


def build_dashboard(run_dir: str | Path, output_path: str | Path | None = None) -> Path:
    run_dir = Path(run_dir)
    out = Path(output_path) if output_path is not None else run_dir / "dashboard.html"
    context = load_run_context(run_dir)
    context.update(
        {
            "best_metric_html": render_best_metric_card(context["manifest"]),
            "metric_panel_html": render_metric_panel(context["metric_series"]),
            "config_table_html": render_config_table(context["config"]),
            "artifact_table_html": render_artifact_table(context["artifacts"]),
        }
    )
    out.write_text(_render_dashboard(context), encoding="utf-8")
    return out


def _render_dashboard(context: dict) -> str:
    try:
        from jinja2 import Environment, select_autoescape

        template_text = resources.files("skilllogboard.dashboards.templates").joinpath(
            "run.html.j2"
        ).read_text(encoding="utf-8")
        env = Environment(autoescape=select_autoescape(["html", "xml"]))
        template = env.from_string(template_text)
        return template.render(**context)
    except Exception:
        return _fallback_html(context)


def _fallback_html(context: dict) -> str:
    title = html.escape(context.get("title") or "SkillLogBoard Dashboard")
    manifest = context.get("manifest", {})
    file_links = "".join(
        f'<li><a href="{html.escape(link["href"])}">{html.escape(link["label"])}</a></li>'
        for link in context.get("file_links", [])
    )
    return f"""<!doctype html>
<html lang="ko">
<head><meta charset="utf-8"><title>{title}</title></head>
<body>
  <h1>SkillLogBoard Dashboard</h1>
  <p>Fallback renderer used because the Jinja2 template path was unavailable.</p>
  <h2>Run Summary</h2>
  <p>Status: <code>{html.escape(str(manifest.get("status", "unknown")))}</code></p>
  <h2>Files</h2>
  <ul>
    {file_links}
  </ul>
</body>
</html>
"""
