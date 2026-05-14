import os

import yaml

from examples.live_demo import _write_demo_run
from skilllogboard.live.project import build_compare_state, build_live_project_state, find_run_dirs


def _write_run(path, run_id, status, value, mtime, points=1):
    path.mkdir(parents=True)
    (path / "manifest.yaml").write_text(
        yaml.safe_dump(
            {
                "run_id": run_id,
                "run_name": run_id,
                "status": status,
                "best_metric": {"name": "val/acc", "value": value, "step": 1},
            }
        ),
        encoding="utf-8",
    )
    rows = ["timestamp,step,name,value,group,metadata_json"]
    for step in range(1, points + 1):
        rows.append(f"t,{step},val/acc,{value + (step * 0.001):.4f},val,{{}}")
    (path / "metrics.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
    os.utime(path, (mtime, mtime))


def test_find_run_dirs_accepts_run_or_project_root(tmp_path):
    run_dir = tmp_path / "run-a"
    _write_run(run_dir, "run-a", "completed", 0.9, 1)

    assert find_run_dirs(run_dir) == [run_dir]
    assert find_run_dirs(tmp_path) == [run_dir / "manifest.yaml"]


def test_build_live_project_state_counts_and_leaderboard(tmp_path):
    _write_run(tmp_path / "run-a", "run-a", "completed", 0.9, 1)
    _write_run(tmp_path / "run-b", "run-b", "running", 0.7, 2)

    state = build_live_project_state(tmp_path)

    assert state["mode"] == "project"
    assert state["status_counts"] == {"completed": 1, "running": 1}
    assert len(state["runs"]) == 2
    assert state["leaderboard"][0]["metric"] == "val/acc"
    assert state["metric_catalog"][0]["name"] == "val/acc"
    assert state["compare"]["metric"] == "val/acc"
    assert state["capabilities"]["run_count"] == 2
    assert state["capabilities"]["shared_metric_count"] == 1
    assert state["capabilities"]["compare_ready"] is True
    assert state["capabilities"]["running_count"] == 1


def test_project_overview_state_is_summary_first(tmp_path):
    _write_run(tmp_path / "run-a", "run-a", "completed", 0.9, 1, points=40)
    _write_run(tmp_path / "run-b", "run-b", "running", 0.7, 2, points=40)

    state = build_live_project_state(tmp_path, view="overview")

    assert state["current_view"] == "overview"
    assert state["payload_scope"] == "summary"
    assert state["compare"]["series"] == []
    assert "metric_series" not in state["runs"][0]
    assert state["runs"][0]["metric_catalog"][0]["count"] == 40


def test_project_summary_cache_invalidates_on_metric_mtime(tmp_path):
    run_dir = tmp_path / "run-a"
    _write_run(run_dir, "run-a", "completed", 0.5, 1, points=1)

    first = build_live_project_state(tmp_path, view="overview")
    (run_dir / "metrics.csv").write_text(
        "timestamp,step,name,value,group,metadata_json\n"
        "t,1,val/acc,0.95,val,{}\n",
        encoding="utf-8",
    )
    os.utime(run_dir / "metrics.csv", (10, 10))
    second = build_live_project_state(tmp_path, view="overview")

    assert first["runs"][0]["metrics"]["val/acc"]["value"] != second["runs"][0]["metrics"]["val/acc"]["value"]
    assert second["runs"][0]["metrics"]["val/acc"]["value"] == 0.95


def test_find_run_dirs_skips_irrelevant_and_deep_folders(tmp_path):
    _write_run(tmp_path / "project" / "run-a", "run-a", "completed", 0.9, 1)
    _write_run(tmp_path / ".venv" / "fake-run", "fake", "failed", 0.1, 1)
    _write_run(tmp_path / "project" / "run-a" / "artifacts" / "nested", "fake", "failed", 0.1, 1)
    _write_run(tmp_path / "too" / "deep" / "for" / "default" / "scan" / "run-b", "run-b", "completed", 0.8, 1)

    runs = find_run_dirs(tmp_path)

    assert runs == [tmp_path / "project" / "run-a" / "manifest.yaml"]


def test_build_live_project_state_latest_uses_run_directory_mtime(tmp_path):
    old_run = tmp_path / "old"
    new_run = tmp_path / "new"
    _write_run(old_run, "old", "completed", 0.7, 1)
    _write_run(new_run, "new", "running", 0.9, 2)

    state = build_live_project_state(tmp_path, latest=True)

    assert [run["run_id"] for run in state["runs"]] == ["new"]


def test_build_compare_state_returns_bounded_series_and_roles(tmp_path):
    _write_run(tmp_path / "baseline", "baseline", "completed", 0.7, 1, points=20)
    _write_run(tmp_path / "best", "best", "completed", 0.9, 2, points=20)
    _write_run(tmp_path / "latest", "latest", "running", 0.8, 3, points=20)

    compare = build_compare_state(tmp_path, metric="val/acc", max_runs=3, max_points=5)

    assert compare["metric"] == "val/acc"
    assert compare["bounds"] == {"max_runs": 3, "max_points": 5}
    assert len(compare["series"]) == 3
    assert all(len(item["points"]) <= 5 for item in compare["series"])
    roles = {role for run in compare["runs"] for role in run["roles"]}
    assert {"best", "latest", "baseline"}.issubset(roles)


def test_build_compare_state_supports_selection_and_normalized_relative_points(tmp_path):
    _write_run(tmp_path / "run-a", "run-a", "completed", 0.5, 1, points=4)
    _write_run(tmp_path / "run-b", "run-b", "completed", 0.8, 2, points=4)

    compare = build_compare_state(
        tmp_path,
        metric="val/acc",
        selected_run_ids=["run-b"],
        normalize=True,
        align="relative",
    )

    assert compare["selected_run_ids"] == ["run-b"]
    points = compare["series"][0]["points"]
    assert points[0]["x"] == 0
    assert all(0 <= point["value"] <= 1 for point in points)


def test_project_leaderboard_accepts_logger_best_metric_shape(tmp_path):
    run_dir = tmp_path / "run-a"
    run_dir.mkdir()
    (run_dir / "manifest.yaml").write_text(
        yaml.safe_dump(
            {
                "run_id": "run-a",
                "run_name": "run-a",
                "status": "completed",
                "best_metric": {"name": "val/acc", "best_value": 0.88, "best_step": 3},
            }
        ),
        encoding="utf-8",
    )
    (run_dir / "metrics.csv").write_text(
        "timestamp,step,name,value,group,metadata_json\n"
        "t,3,val/acc,0.88,val,{}\n",
        encoding="utf-8",
    )

    state = build_live_project_state(tmp_path)

    assert state["leaderboard"][0]["value"] == 0.88
    assert state["leaderboard"][0]["step"] == 3


def test_rich_live_demo_run_has_shared_showcase_metrics(tmp_path):
    run_dirs = [_write_demo_run(index, root_dir=tmp_path / "live_demo", rich=True) for index in range(5)]

    state = build_live_project_state(tmp_path / "live_demo")

    assert len(run_dirs) == 5
    assert {"baseline", "best", "overfit", "failed", "current"}.issubset(
        {run["run_name"] for run in state["runs"]}
    )
    assert {"completed", "failed", "running"}.issubset(set(state["status_counts"]))
    for metric in ["train/loss", "val/loss", "val/acc", "val/f1", "lr", "grad_norm"]:
        assert metric in state["shared_metrics"]
    assert state["capabilities"]["artifact_count"] >= 5
    assert state["capabilities"]["agent_evidence"] is True
