import csv

from skilllogboard.compare.seed_group import (
    extract_seed,
    group_runs_by_seed,
    make_group_key,
    seed_summary_to_markdown,
    write_seed_summary_csv,
)


def _record(run_id, seed, metric, config=None):
    cfg = {"model": "Tiny", "lr": 0.001, "seed": seed}
    if config:
        cfg.update(config)
    return {
        "run_id": run_id,
        "config": cfg,
        "manifest": {"seed": seed},
        "main_metric": {"name": "val/acc", "mode": "max"},
        "best_metric": {
            "name": "val/acc",
            "mode": "max",
            "best_value": metric,
            "best_step": 1,
        },
        "metrics": {"val/acc": {"value": metric, "step": 1}},
    }


def test_extract_seed_from_config_manifest_and_missing():
    assert extract_seed(_record("a", 1, 0.8)) == 1
    assert extract_seed({"config": {}, "manifest": {"seed": 2}}) == 2
    assert extract_seed({"config": {}, "manifest": {}}) is None


def test_make_group_key_ignores_seed_and_supports_group_by():
    a = _record("a", 1, 0.8)
    b = _record("b", 2, 0.9)

    assert make_group_key(a) == make_group_key(b)
    assert make_group_key(a, group_by=["model"]) == '{"model": "Tiny"}'


def test_group_runs_by_seed_computes_summary():
    records = [_record("a", 1, 0.8), _record("b", 2, 1.0), _record("c", 3, 0.6, {"lr": 0.01})]

    rows = group_runs_by_seed(records, "val/acc", mode="max")

    assert len(rows) == 2
    first = rows[0]
    assert first["count"] == 2
    assert first["mean"] == 0.9
    assert first["std"] == 0.09999999999999998
    assert first["median"] == 0.9
    assert first["best"] == 1.0
    assert first["best_run_id"] == "b"


def test_seed_summary_markdown_and_csv(tmp_path):
    rows = group_runs_by_seed([_record("a", 1, 0.8)], "val/acc")

    out = write_seed_summary_csv(rows, tmp_path / "seed_summary.csv")
    markdown = seed_summary_to_markdown(rows)

    with out.open(newline="", encoding="utf-8") as f:
        csv_rows = list(csv.DictReader(f))
    assert csv_rows[0]["count"] == "1"
    assert "| --- |" in markdown
    assert "best_run_id" in markdown
