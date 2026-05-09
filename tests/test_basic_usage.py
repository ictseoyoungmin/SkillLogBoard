from skilllogboard import RunLogger


def test_basic_run(tmp_path):
    logger = RunLogger(
        project="demo",
        run_name="baseline",
        config={"model_name": "TinyNet", "dataset_name": "Synthetic", "seed": 42},
        root_dir=tmp_path / "runs",
        main_metric={"name": "val/acc", "mode": "max"},
    )
    logger.log_metrics({"train/loss": 1.0, "val/acc": 0.8}, step=0)
    logger.finish(build_dashboard=True, build_report=True)

    assert (logger.run_dir / "manifest.yaml").exists()
    assert (logger.run_dir / "metrics.csv").exists()
    assert (logger.run_dir / "events.jsonl").exists()
    assert (logger.run_dir / "summary.md").exists()
    assert (logger.run_dir / "dashboard.html").exists()
