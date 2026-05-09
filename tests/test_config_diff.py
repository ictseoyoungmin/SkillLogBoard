import csv

from skilllogboard.compare.config_diff import (
    ablation_axes_to_markdown,
    build_config_diff,
    config_diff_to_markdown,
    extract_ablation_axes,
    flatten_config,
    write_config_diff_csv,
)


def _record(run_id, config):
    return {"run_id": run_id, "config": config}


def test_flatten_config_handles_nested_scalars_and_lists():
    flat = flatten_config(
        {
            "optimizer": {"lr": 0.001, "name": "adam"},
            "layers": [1, 2],
            "enabled": True,
            "name": "Tiny",
        }
    )

    assert flat["optimizer.lr"] == 0.001
    assert flat["layers"] == "[1, 2]"
    assert flat["enabled"] is True
    assert flatten_config({}) == {}


def test_build_config_diff_excludes_constants_by_default():
    records = [
        _record("a", {"lr": 0.001, "model": "Tiny"}),
        _record("b", {"lr": 0.01, "model": "Tiny"}),
    ]

    rows = build_config_diff(records)
    all_rows = build_config_diff(records, include_constant=True)

    assert [row["key"] for row in rows] == ["lr"]
    assert {row["key"] for row in all_rows} == {"lr", "model"}
    assert rows[0]["run:a"] == 0.001


def test_extract_ablation_axes_inferred_and_explicit():
    records = [
        _record("a", {"activation": "relu", "norm": "bn", "loss_name": "ce", "lr": 0.001}),
        _record("b", {"activation": "gelu", "norm": "bn", "loss_name": "mse", "lr": 0.001}),
    ]

    inferred = extract_ablation_axes(records)
    explicit = extract_ablation_axes(records, candidate_keys=["activation", "norm"])

    assert {axis["key"] for axis in inferred} == {"activation", "loss_name"}
    assert [axis["key"] for axis in explicit] == ["activation", "norm"]
    assert explicit[0]["distinct_values"] == ["gelu", "relu"]


def test_config_diff_markdown_csv_and_axis_summary(tmp_path):
    rows = build_config_diff([_record("a", {"lr": 1}), _record("b", {"lr": 2})])
    axes = extract_ablation_axes([_record("a", {"lr": 1}), _record("b", {"lr": 2})])

    out = write_config_diff_csv(rows, tmp_path / "config_diff.csv")
    markdown = config_diff_to_markdown(rows)
    axes_md = ablation_axes_to_markdown(axes)

    with out.open(newline="", encoding="utf-8") as f:
        csv_rows = list(csv.DictReader(f))
    assert csv_rows[0]["key"] == "lr"
    assert "| --- |" in markdown
    assert "run:a" in markdown
    assert "lr" in axes_md
