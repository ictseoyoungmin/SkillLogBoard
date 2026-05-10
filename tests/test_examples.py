from examples.basic_usage import main as run_basic_usage
from examples.ir_drop_example import main as run_ir_drop_example
from examples.sklearn_example import main as run_sklearn_example
from examples.trajectory_example import main as run_trajectory_example


def _assert_core_outputs(run_dir, expect_skill_trace=True):
    assert (run_dir / "metrics.csv").exists()
    assert (run_dir / "dashboard.html").exists()
    assert (run_dir / "summary.md").exists()
    if expect_skill_trace:
        assert (run_dir / "skill_trace.jsonl").exists()


def test_basic_usage_example_smoke(tmp_path):
    run_dir = run_basic_usage(root_dir=tmp_path / "runs")

    _assert_core_outputs(run_dir)


def test_ir_drop_example_smoke(tmp_path):
    run_dir = run_ir_drop_example(root_dir=tmp_path / "runs")

    _assert_core_outputs(run_dir)
    assert "val/high_drop_f1" in (run_dir / "metrics.csv").read_text(encoding="utf-8")


def test_trajectory_example_smoke(tmp_path):
    run_dir = run_trajectory_example(root_dir=tmp_path / "runs")

    _assert_core_outputs(run_dir)
    assert "val/pb_score" in (run_dir / "metrics.csv").read_text(encoding="utf-8")


def test_sklearn_style_example_smoke(tmp_path):
    run_dir = run_sklearn_example(root_dir=tmp_path / "runs")

    _assert_core_outputs(run_dir, expect_skill_trace=False)
    assert "val/f1" in (run_dir / "metrics.csv").read_text(encoding="utf-8")
