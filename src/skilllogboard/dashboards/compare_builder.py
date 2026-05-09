"""Static multi-run compare report builder."""

from __future__ import annotations

from importlib import resources
from pathlib import Path
from typing import Any
import html

from skilllogboard.compare.config_diff import (
    ablation_axes_to_markdown,
    build_config_diff,
    config_diff_to_markdown,
    extract_ablation_axes,
)
from skilllogboard.compare.leaderboard import (
    build_leaderboard,
    leaderboard_to_markdown,
    write_leaderboard_csv,
)
from skilllogboard.compare.run_index import build_run_index
from skilllogboard.compare.seed_group import group_runs_by_seed, seed_summary_to_markdown


def build_compare_report(
    runs_dir: str | Path,
    metric: str,
    mode: str = "max",
    output_dir: str | Path | None = None,
) -> dict[str, Path]:
    runs_root = Path(runs_dir)
    out_dir = Path(output_dir) if output_dir is not None else runs_root
    out_dir.mkdir(parents=True, exist_ok=True)

    records = build_run_index(runs_root)
    if not records:
        raise ValueError(f"No run folders with manifest.yaml found under {runs_root}")

    leaderboard = build_leaderboard(records, metric=metric, mode=mode)
    config_diff = build_config_diff(records)
    axes = extract_ablation_axes(records)
    seed_summary = group_runs_by_seed(records, metric=metric, mode=mode)

    csv_path = write_leaderboard_csv(leaderboard, out_dir / "compare.csv")
    md_path = _write_compare_markdown(
        out_dir / "compare.md",
        leaderboard,
        config_diff,
        axes,
        seed_summary,
    )
    html_path = _write_compare_html(
        out_dir / "compare.html",
        records,
        leaderboard,
        config_diff,
        axes,
        seed_summary,
    )
    return {"csv": csv_path, "md": md_path, "html": html_path}


def build_compare_dashboard(*args: Any, **kwargs: Any) -> Path:
    return build_compare_report(*args, **kwargs)["html"]


def _write_compare_markdown(
    path: Path,
    leaderboard: list[dict[str, Any]],
    config_diff: list[dict[str, Any]],
    axes: list[dict[str, Any]],
    seed_summary: list[dict[str, Any]],
) -> Path:
    lines = [
        "# SkillLogBoard Compare",
        "",
        "## Leaderboard",
        "",
        leaderboard_to_markdown(leaderboard),
        "",
        "## Config Diff",
        "",
        config_diff_to_markdown(config_diff) if config_diff else "No varying config keys were detected.",
        "",
        "## Ablation Axes",
        "",
        ablation_axes_to_markdown(axes),
        "",
        "## Seed Summary",
        "",
        seed_summary_to_markdown(seed_summary),
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def _write_compare_html(
    path: Path,
    records: list[dict[str, Any]],
    leaderboard: list[dict[str, Any]],
    config_diff: list[dict[str, Any]],
    axes: list[dict[str, Any]],
    seed_summary: list[dict[str, Any]],
) -> Path:
    context = {
        "title": "SkillLogBoard Compare",
        "records": _records_with_links(records, path.parent),
        "leaderboard_html": _markdown_table_to_html(leaderboard_to_markdown(leaderboard)),
        "config_diff_html": _markdown_table_to_html(config_diff_to_markdown(config_diff))
        if config_diff
        else "<p>No varying config keys were detected.</p>",
        "ablation_axes_html": _markdown_table_to_html(ablation_axes_to_markdown(axes)),
        "seed_summary_html": _markdown_table_to_html(seed_summary_to_markdown(seed_summary)),
    }
    path.write_text(_render_compare_html(context), encoding="utf-8")
    return path


def _render_compare_html(context: dict[str, Any]) -> str:
    try:
        from jinja2 import Environment, select_autoescape

        template_text = resources.files("skilllogboard.dashboards.templates").joinpath(
            "compare.html.j2"
        ).read_text(encoding="utf-8")
        env = Environment(autoescape=select_autoescape(["html", "xml"]))
        template = env.from_string(template_text)
        return template.render(**context)
    except Exception:
        return _fallback_compare_html(context)


def _records_with_links(records: list[dict[str, Any]], output_dir: Path) -> list[dict[str, Any]]:
    linked = []
    for record in records:
        run_dir = Path(record.get("run_dir", ""))
        dashboard = run_dir / "dashboard.html"
        href = ""
        if dashboard.exists():
            href = dashboard.relative_to(output_dir).as_posix() if _is_relative_to(dashboard, output_dir) else dashboard.as_posix()
        linked.append({**record, "dashboard_href": href})
    return linked


def _is_relative_to(path: Path, base: Path) -> bool:
    try:
        path.relative_to(base)
    except ValueError:
        return False
    return True


def _markdown_table_to_html(markdown: str) -> str:
    lines = [line for line in markdown.splitlines() if line.startswith("|")]
    if len(lines) < 2:
        return f"<p>{html.escape(markdown)}</p>"
    headers = [_clean_cell(cell) for cell in lines[0].strip("|").split("|")]
    body = []
    for line in lines[2:]:
        body.append([_clean_cell(cell) for cell in line.strip("|").split("|")])
    head_html = "".join(f"<th>{html.escape(header)}</th>" for header in headers)
    body_html = "".join(
        "<tr>" + "".join(f"<td>{html.escape(cell)}</td>" for cell in row) + "</tr>" for row in body
    )
    return f"<table><thead><tr>{head_html}</tr></thead><tbody>{body_html}</tbody></table>"


def _clean_cell(value: str) -> str:
    return value.strip().replace("\\|", "|")


def _fallback_compare_html(context: dict[str, Any]) -> str:
    return f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>{html.escape(context["title"])}</title></head>
<body>
  <h1>{html.escape(context["title"])}</h1>
  <h2>Leaderboard</h2>
  {context["leaderboard_html"]}
  <h2>Config Diff</h2>
  {context["config_diff_html"]}
  <h2>Ablation Axes</h2>
  {context["ablation_axes_html"]}
  <h2>Seed Summary</h2>
  {context["seed_summary_html"]}
</body>
</html>
"""
