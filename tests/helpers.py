import json

import yaml


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def read_yaml(path):
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def assert_html_document(html):
    lowered = html.lower()
    assert lowered.startswith("<!doctype html>")
    assert "<html" in lowered
    assert "<head>" in lowered
    assert '<meta charset="utf-8">' in lowered
    assert "<body>" in lowered
    assert "</html>" in lowered


def assert_contains_sections(html, sections):
    for section in sections:
        assert section in html
