"""Tests for RetentionPolicy metric mode and keep_best correctness."""

import yaml

from skilllogboard.retention.planner import plan_prune
from skilllogboard.retention.policy import RetentionPolicy


def _run(root, name, metric_value, metric_name="score", baseline=False):
    run_dir = root / name
    run_dir.mkdir(parents=True)
    (run_dir / "manifest.yaml").write_text(
        yaml.safe_dump({
            "run_id": name,
            "status": "completed",
            "baseline": baseline,
            "best_metric": {"name": metric_name, "value": metric_value},
        }),
        encoding="utf-8",
    )
    (run_dir / "metrics.csv").write_text(
        f"timestamp,step,name,value,group,metadata_json\n,1,{metric_name},{metric_value},val,{{}}\n",
        encoding="utf-8",
    )
    return run_dir


def test_keep_best_max_protects_highest_score(tmp_path):
    _run(tmp_path, "low", 0.5)
    _run(tmp_path, "mid", 0.7)
    _run(tmp_path, "high", 0.9)

    plan = plan_prune(
        tmp_path,
        RetentionPolicy(
            keep_best=1, keep_latest=0,
            best_metric_name="score", best_metric_mode="max",
            dry_run=True,
        ),
    )
    by_id = {a["run_id"]: a for a in plan["actions"]}
    assert by_id["high"]["protected"] is True
    assert by_id["low"]["protected"] is False
    assert by_id["mid"]["protected"] is False


def test_keep_best_min_protects_lowest_loss(tmp_path):
    _run(tmp_path, "low-loss", 0.1, metric_name="loss")
    _run(tmp_path, "mid-loss", 0.5, metric_name="loss")
    _run(tmp_path, "high-loss", 0.9, metric_name="loss")

    plan = plan_prune(
        tmp_path,
        RetentionPolicy(
            keep_best=1, keep_latest=0,
            best_metric_name="loss", best_metric_mode="min",
            dry_run=True,
        ),
    )
    by_id = {a["run_id"]: a for a in plan["actions"]}
    assert by_id["low-loss"]["protected"] is True
    assert by_id["high-loss"]["protected"] is False


def test_keep_best_fallback_no_metric_name(tmp_path):
    """Without best_metric_name, falls back to max of any numeric metric."""
    _run(tmp_path, "run-1", 0.3)
    _run(tmp_path, "run-2", 0.8)

    plan = plan_prune(
        tmp_path,
        RetentionPolicy(keep_best=1, keep_latest=0, dry_run=True),
    )
    by_id = {a["run_id"]: a for a in plan["actions"]}
    assert by_id["run-2"]["protected"] is True


def test_retention_policy_from_dict_best_metric_fields():
    p = RetentionPolicy.from_dict({"best_metric_name": "val_loss", "best_metric_mode": "min"})
    assert p.best_metric_name == "val_loss"
    assert p.best_metric_mode == "min"


def test_retention_policy_to_dict_includes_best_metric():
    p = RetentionPolicy(best_metric_name="acc", best_metric_mode="max")
    d = p.to_dict()
    assert d["best_metric_name"] == "acc"
    assert d["best_metric_mode"] == "max"


def test_plan_prune_destructive_actions_performed_is_false(tmp_path):
    _run(tmp_path, "run-a", 0.5)
    plan = plan_prune(tmp_path)
    assert plan["destructive_actions_performed"] is False
