from skilllogboard import RunLogger
from skilllogboard.compare.leaderboard import build_leaderboard
from skilllogboard.compare.run_index import build_run_index
from skilllogboard.compare.seed_group import group_runs_by_seed


def test_run_index_leaderboard_and_seed_summary_integrate(tmp_path):
    runs_root = tmp_path / "runs"
    for seed, value in [(1, 0.7), (2, 0.9), (3, 0.4)]:
        logger = RunLogger(
            project="demo",
            run_name=f"seed-{seed}",
            root_dir=runs_root,
            config={"model": "Tiny", "lr": 0.001 if seed < 3 else 0.01, "seed": seed},
            main_metric={"name": "val/acc", "mode": "max"},
        )
        logger.log_metric("val/acc", value, step=1)
        logger.finish()

    records = build_run_index(runs_root)
    leaderboard = build_leaderboard(records, metric="val/acc", mode="max")
    summary = group_runs_by_seed(records, metric="val/acc", mode="max")

    assert len(leaderboard) == 3
    assert leaderboard[0]["run_name"] == "seed-2"
    assert [row["count"] for row in summary] == [2, 1]
    assert summary[0]["best_run_id"]
