import yaml

from skilllogboard.live.project import build_live_project_state, find_run_dirs


def _write_run(path, run_id, status, value, mtime):
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
    (path / "metrics.csv").write_text(
        f"timestamp,step,name,value,group,metadata_json\nt,1,val/acc,{value},val,{{}}\n",
        encoding="utf-8",
    )
    path.touch()


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
