import csv
import json

import yaml

from skilllogboard.cli.main import main
from skilllogboard.index.builder import build_project_index
from skilllogboard.query import filter_runs, parse_filter_expression


def _run(root, name, value, status="completed", tags=None, group="", baseline=False):
    run_dir = root / name
    run_dir.mkdir(parents=True)
    (run_dir / "manifest.yaml").write_text(
        yaml.safe_dump(
            {
                "run_id": name,
                "run_name": name,
                "status": status,
                "tags": tags or [],
                "group": group,
                "baseline": baseline,
                "best_metric": {"name": "val/acc", "value": value, "mode": "max"},
            }
        ),
        encoding="utf-8",
    )
    with (run_dir / "metrics.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "step", "name", "value", "group", "metadata_json"])
        writer.writeheader()
        writer.writerow({"timestamp": "", "step": 1, "name": "val/acc", "value": value, "group": "val", "metadata_json": "{}"})
    return run_dir


def test_project_index_records_tags_baseline_and_metric_summary(tmp_path):
    _run(tmp_path, "baseline", 0.7, tags=["keep"], group="a", baseline=True)
    _run(tmp_path, "candidate", 0.9, tags=["fast"], group="a")

    index = build_project_index(tmp_path)

    assert index.runs[0].run_id in {"baseline", "candidate"}
    by_id = {run.run_id: run for run in index.runs}
    assert by_id["baseline"].baseline is True
    assert by_id["candidate"].tags == ["fast"]
    assert by_id["candidate"].metric_summaries[0]["best"] == 0.9


def test_query_filters_status_tag_group_and_metric_threshold(tmp_path):
    _run(tmp_path, "one", 0.8, tags=["fast"], group="g1")
    _run(tmp_path, "two", 0.4, status="failed", tags=["slow"], group="g2")
    rows = [run.to_dict() for run in build_project_index(tmp_path).runs]

    filtered, parsed = filter_runs(rows, "status:completed tag:fast group:g1 metric:val/acc>=0.75")

    assert parsed.ok
    assert [run["run_id"] for run in filtered] == ["one"]
    assert not parse_filter_expression("metric:val/acc>bad").ok


def test_index_rebuild_and_runs_list_cli(tmp_path, capsys):
    _run(tmp_path, "one", 0.8, tags=["fast"], group="g1")

    assert main(["index", "rebuild", str(tmp_path)]) == 0
    assert (tmp_path / ".skilllogboard" / "index.json").exists()
    capsys.readouterr()

    assert main(["runs", "list", str(tmp_path), "--filter", "tag:fast", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["count"] == 1
    assert payload["runs"][0]["run_id"] == "one"
