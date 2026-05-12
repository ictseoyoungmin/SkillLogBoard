"""Optional report figure builders."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
import csv

from skilllogboard.compare.run_index import discover_runs


class OptionalFigureDependencyError(RuntimeError):
    """Raised when optional plotting dependencies are unavailable."""


@dataclass
class ReportFigure:
    figure_id: str
    figure_type: str
    path: str
    metric: str = ""
    source_files: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def require_matplotlib():
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise OptionalFigureDependencyError(
            "Figure export requires the optional report extra: pip install 'skilllogboard[report]'"
        ) from exc
    return plt


def build_metric_curve_figure(
    run_dir: str | Path,
    metrics: str | list[str],
    output_path: str | Path,
    format: str = "png",
) -> ReportFigure:
    run_dir = Path(run_dir)
    names = [metrics] if isinstance(metrics, str) else list(metrics)
    series = _read_metric_series(run_dir / "metrics.csv")
    missing = [name for name in names if name not in series]
    if missing:
        raise ValueError(f"Metrics not found for figure: {', '.join(missing)}")
    plt = require_matplotlib()
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7, 4))
    for name in names:
        points = series[name]
        ax.plot([p["step"] for p in points], [p["value"] for p in points], marker="o", label=name)
    ax.set_title("Metric Curve")
    ax.set_xlabel("step")
    ax.set_ylabel("value")
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out, format=format)
    plt.close(fig)
    return ReportFigure(
        figure_id="metric-curve",
        figure_type="metric-curve",
        path=out.as_posix(),
        metric=", ".join(names),
        source_files=[(run_dir / "metrics.csv").as_posix()],
        metadata={"format": format},
    )


def build_metric_curve_overlay_figure(
    root_dir: str | Path,
    metric: str,
    output_path: str | Path,
    mode: str | None = None,
) -> ReportFigure:
    run_dirs = discover_runs(root_dir)
    if not run_dirs and (Path(root_dir) / "manifest.yaml").exists():
        run_dirs = [Path(root_dir)]
    data: list[tuple[Path, list[dict[str, float]]]] = []
    for run_dir in run_dirs:
        series = _read_metric_series(run_dir / "metrics.csv")
        if metric in series:
            data.append((run_dir, series[metric]))
    if not data:
        raise ValueError(f"Metric not found for overlay figure: {metric}")
    plt = require_matplotlib()
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7, 4))
    for run_dir, points in data:
        ax.plot([p["step"] for p in points], [p["value"] for p in points], marker="o", label=run_dir.name)
    ax.set_title(f"Metric Overlay: {metric}")
    ax.set_xlabel("step")
    ax.set_ylabel(metric)
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)
    return ReportFigure(
        figure_id="metric-curve-overlay",
        figure_type="metric-curve-overlay",
        path=out.as_posix(),
        metric=metric,
        source_files=[(run_dir / "metrics.csv").as_posix() for run_dir, _points in data],
        metadata={"mode": mode},
    )


def build_seed_errorbar_figure(summary_rows: list[dict[str, Any]], output_path: str | Path) -> ReportFigure:
    plt = require_matplotlib()
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    labels = [str(row.get("group_key", "")) for row in summary_rows]
    means = [float(row.get("mean") or 0.0) for row in summary_rows]
    stds = [float(row.get("std") or 0.0) for row in summary_rows]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.errorbar(labels, means, yerr=stds, fmt="o")
    ax.set_title("Seed Summary")
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)
    return ReportFigure("seed-errorbar", "seed-errorbar", out.as_posix(), metadata={"row_count": len(summary_rows)})


def build_ablation_bar_figure(summary_rows: list[dict[str, Any]], output_path: str | Path) -> ReportFigure:
    plt = require_matplotlib()
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    labels = [f"{row.get('axis')}={row.get('value')}" for row in summary_rows]
    values = [float(row.get("mean") or row.get("best") or 0.0) for row in summary_rows]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(labels, values)
    ax.set_title("Ablation Summary")
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)
    return ReportFigure("ablation-bar", "ablation-bar", out.as_posix(), metadata={"row_count": len(summary_rows)})


def _read_metric_series(path: Path) -> dict[str, list[dict[str, float]]]:
    if not path.exists():
        return {}
    series: dict[str, list[dict[str, float]]] = {}
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for index, row in enumerate(reader):
            name = row.get("name")
            if not name:
                continue
            try:
                value = float(row.get("value", ""))
            except ValueError:
                continue
            try:
                step = int(row.get("step") or index)
            except ValueError:
                step = index
            series.setdefault(name, []).append({"step": step, "value": value})
    return series
