import pytest

from skilllogboard import RunLogger
from skilllogboard.reports.figure_builder import (
    OptionalFigureDependencyError,
    build_ablation_bar_figure,
    build_metric_curve_figure,
    build_metric_curve_overlay_figure,
    build_seed_errorbar_figure,
    require_matplotlib,
)
from skilllogboard.reports.figures import list_figure_types, write_svg_fallback


def _make_runs(tmp_path):
    runs_root = tmp_path / "runs"
    for seed, acc, lr in [(1, 0.7, 0.001), (2, 0.9, 0.001), (3, 0.6, 0.01)]:
        logger = RunLogger(
            project="demo",
            run_name=f"seed-{seed}",
            root_dir=runs_root,
            config={"model": "Tiny", "seed": seed, "lr": lr},
            main_metric={"name": "val/acc", "mode": "max"},
        )
        logger.log_metric("val/acc", acc - 0.1, step=0)
        logger.log_metric("val/acc", acc, step=1)
        logger.finish()
    return runs_root


def _matplotlib_or_skip():
    try:
        require_matplotlib()
    except OptionalFigureDependencyError as exc:
        pytest.skip(str(exc))


def test_metric_curve_figure_builds_when_report_extra_available(tmp_path):
    _matplotlib_or_skip()
    runs_root = _make_runs(tmp_path)
    run_dir = next((runs_root / "demo").iterdir())
    out = tmp_path / "curve.png"

    figure = build_metric_curve_figure(run_dir, metrics=["val/acc"], output_path=out)

    assert out.exists()
    assert figure.figure_type == "metric-curve"


def test_metric_curve_overlay_builds_when_report_extra_available(tmp_path):
    _matplotlib_or_skip()
    runs_root = _make_runs(tmp_path)
    out = tmp_path / "overlay.png"

    figure = build_metric_curve_overlay_figure(runs_root, metric="val/acc", output_path=out)

    assert out.exists()
    assert figure.figure_type == "metric-curve-overlay"


def test_aggregate_figures_build_when_report_extra_available(tmp_path):
    _matplotlib_or_skip()
    seed_out = tmp_path / "seed.png"
    ablation_out = tmp_path / "ablation.png"

    seed = build_seed_errorbar_figure(
        [{"group_key": "Tiny", "mean": 0.8, "std": 0.1}],
        seed_out,
    )
    ablation = build_ablation_bar_figure(
        [{"axis": "lr", "value": "0.001", "mean": 0.8}],
        ablation_out,
    )

    assert seed_out.exists()
    assert ablation_out.exists()
    assert seed.figure_type == "seed-errorbar"
    assert ablation.figure_type == "ablation-bar"


def test_figure_registry_and_svg_fallback(tmp_path):
    out = write_svg_fallback(tmp_path / "fallback.svg", "Metric Curve", "matplotlib unavailable")

    assert "metric-curve-overlay" in list_figure_types()
    assert out.exists()
    assert "<svg" in out.read_text(encoding="utf-8")
