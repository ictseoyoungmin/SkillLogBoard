import json

from skilllogboard import RunLogger
from skilllogboard.reports.table_builder import (
    ReportTable,
    build_ablation_summary_table,
    build_leaderboard_table,
    build_rule_audit_table,
    build_seed_summary_table,
    table_to_csv_string,
    table_to_latex,
    table_to_markdown,
)
from skilllogboard.reports.tables import get_table_definition, list_table_types


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
        logger.log_metric("val/acc", acc, step=seed)
        logger.finish()
        trace = logger.run_dir / "skill_trace.jsonl"
        trace.write_text(
            json.dumps(
                {
                    "rule_id": "RULE-1",
                    "outcome": "passed",
                    "severity": "warning",
                    "message": "ok",
                }
            )
            + "\n",
            encoding="utf-8",
        )
    return runs_root


def test_report_table_export_helpers_are_deterministic():
    table = ReportTable(
        "demo",
        "demo",
        ["a", "b"],
        [{"a": "one", "b": 2}],
    )

    assert "| a | b |" in table_to_markdown(table)
    assert table_to_csv_string(table).startswith("a,b")
    assert "\\begin{tabular}" in table_to_latex(table)


def test_report_table_adapters_build_from_runs(tmp_path):
    runs_root = _make_runs(tmp_path)

    leaderboard = build_leaderboard_table(runs_root, metric="val/acc", mode="max")
    seed_summary = build_seed_summary_table(runs_root, metric="val/acc", mode="max", group_by=["model"])
    ablation = build_ablation_summary_table(runs_root, metric="val/acc", mode="max")
    audit = build_rule_audit_table(runs_root)

    assert leaderboard.rows[0]["run_name"] == "seed-2"
    assert seed_summary.rows[0]["count"] == 3
    assert any(row["axis"] == "lr" for row in ablation.rows)
    assert len(audit.rows) == 3


def test_table_registry_lists_supported_tables():
    assert "leaderboard" in list_table_types()
    assert get_table_definition("leaderboard").requires_metric is True
