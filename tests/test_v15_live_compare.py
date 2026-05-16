import csv

import yaml

from skilllogboard.live.downsample import downsample_points
from skilllogboard.live.project import build_compare_state


def _run(root, name, start, baseline=False, tag=""):
    run_dir = root / name
    run_dir.mkdir(parents=True)
    (run_dir / "manifest.yaml").write_text(
        yaml.safe_dump(
            {
                "run_id": name,
                "status": "completed",
                "baseline": baseline,
                "tags": [tag] if tag else [],
            }
        ),
        encoding="utf-8",
    )
    with (run_dir / "metrics.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "step", "name", "value", "group", "metadata_json"])
        writer.writeheader()
        for step in range(10):
            writer.writerow({"timestamp": "", "step": step, "name": "loss", "value": start + step, "group": "train", "metadata_json": "{}"})


def test_downsample_preserves_first_and_last():
    rows = [{"step": step, "value": step} for step in range(20)]

    bounded, metadata = downsample_points(rows, max_points=5)

    assert metadata["downsampled"] is True
    assert bounded[0]["step"] == 0
    assert bounded[-1]["step"] == 19
    assert len(bounded) == 5


def test_compare_clamps_filters_and_reports_baseline_delta(tmp_path):
    _run(tmp_path, "baseline", 0, baseline=True, tag="keep")
    _run(tmp_path, "candidate", 10, tag="keep")
    _run(tmp_path, "other", 50, tag="skip")

    payload = build_compare_state(
        tmp_path,
        metric="loss",
        max_runs=999,
        max_points=3,
        filters="tag:keep",
    )

    assert payload["bounds"]["max_runs"] == 25
    assert set(payload["selected_run_ids"]) == {"candidate", "baseline"}
    assert all(series["downsampling"]["returned_count"] == 3 for series in payload["series"])
    deltas = {series["run_id"]: series["delta_from_baseline"] for series in payload["series"]}
    assert deltas["baseline"] == 0
    assert deltas["candidate"] == 10
