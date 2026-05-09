import csv

from skilllogboard.compare.leaderboard import (
    build_leaderboard,
    latest_metric,
    leaderboard_to_markdown,
    metric_value,
    rows_to_latex,
    write_leaderboard_csv,
)


def _record(run_id, latest=0.8, best=None, mode="max"):
    best_value = latest if best is None else best
    return {
        "run_id": run_id,
        "run_name": run_id,
        "status": "completed",
        "created_at": "2026-05-10",
        "main_metric": {"name": "val/acc", "mode": mode},
        "best_metric": {
            "name": "val/acc",
            "mode": mode,
            "best_value": best_value,
            "best_step": 3,
        },
        "metrics": {"val/acc": {"value": latest, "step": 4}},
        "warning_count": 0,
        "error_count": 0,
    }


def test_metric_helpers_extract_latest_and_best():
    record = _record("a", latest=0.7, best=0.9)

    assert latest_metric(record, "val/acc") == 0.7
    assert metric_value(record, "val/acc") == ("val/acc", 0.9, 3)
    assert metric_value(record, "missing")[1] is None


def test_build_leaderboard_sorts_max_and_missing_last():
    rows = build_leaderboard(
        [_record("low", 0.1), {"run_id": "missing", "run_name": "missing"}, _record("high", 0.9)],
        metric="val/acc",
        mode="max",
    )

    assert [row["run_id"] for row in rows] == ["high", "low", "missing"]
    assert [row["rank"] for row in rows] == [1, 2, ""]


def test_build_leaderboard_sorts_min():
    rows = build_leaderboard([_record("slow", 2.0, mode="min"), _record("fast", 0.2, mode="min")], metric="val/acc", mode="min")

    assert [row["run_id"] for row in rows] == ["fast", "slow"]


def test_leaderboard_csv_and_markdown_export(tmp_path):
    rows = build_leaderboard([_record("a|b", 0.5)], metric="val/acc")

    out = write_leaderboard_csv(rows, tmp_path / "compare.csv")
    markdown = leaderboard_to_markdown(rows)
    latex = rows_to_latex(rows)

    with out.open(newline="", encoding="utf-8") as f:
        csv_rows = list(csv.DictReader(f))
    assert csv_rows[0]["run_id"] == "a|b"
    assert "| --- |" in markdown
    assert "a\\|b" in markdown
    assert "\\begin{tabular}" in latex
