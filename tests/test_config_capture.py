import json

import yaml

from skilllogboard.core.config_capture import capture_git, capture_system, save_config, save_json


def test_save_config_preserves_nested_and_unicode_values(tmp_path):
    path = tmp_path / "nested" / "config.yaml"
    config = {"model": {"name": "작은모델", "layers": [1, 2, 3]}, "seed": 42}

    save_config(config, path)

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert data["model"]["name"] == "작은모델"
    assert data["model"]["layers"] == [1, 2, 3]
    assert data["seed"] == 42


def test_capture_system_and_save_json(tmp_path):
    system = capture_system()
    assert isinstance(system, dict)
    assert system["platform"]
    assert system["python_version"]

    path = tmp_path / "system.json"
    save_json(system, path)
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded["python_version"] == system["python_version"]


def test_capture_git_never_raises_outside_repo(tmp_path):
    result = capture_git(tmp_path)
    assert isinstance(result, dict)
    assert isinstance(result["available"], bool)
    if result["available"]:
        assert result["commit"]
        assert result["branch"]
