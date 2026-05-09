from datetime import datetime

from skilllogboard.core.run_id import ensure_unique_run_dir, make_run_id, slugify


def test_slugify():
    assert slugify("Hello World!") == "hello_world"
    assert slugify("실험 01!") == "실험_01"
    assert slugify("  ...  ") == "run"
    assert slugify("a" * 80, max_length=8) == "a" * 8


def test_make_run_id_uses_timestamp_and_slug():
    created_at = datetime(2026, 5, 9, 12, 30, 5)

    assert make_run_id("Hello World!", created_at=created_at) == "2026-05-09_12-30-05_hello_world"


def test_ensure_unique_run_dir_does_not_create_and_suffixes_collisions(tmp_path):
    project_dir = tmp_path / "demo"
    run_id = "2026-05-09_12-30-05_baseline"

    first = ensure_unique_run_dir(project_dir, run_id)
    assert first == project_dir / run_id
    assert not first.exists()

    first.mkdir(parents=True)
    second = ensure_unique_run_dir(project_dir, run_id)
    assert second == project_dir / f"{run_id}_001"
    assert not second.exists()
