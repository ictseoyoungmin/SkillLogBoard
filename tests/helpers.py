import json

import yaml


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def read_yaml(path):
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
