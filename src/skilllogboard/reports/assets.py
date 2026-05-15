"""Portable report asset path and offline safety helpers."""

from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable

RENDER_MODES = {"minimal", "portable_interactive", "package"}


def normalize_render_mode(value: str) -> str:
    if value not in RENDER_MODES:
        raise ValueError(f"Unsupported report render mode: {value}")
    return value


def resolve_asset_path(report_dir: str | Path, asset_path: str | Path) -> Path:
    report_root = Path(report_dir).resolve()
    candidate = Path(asset_path)
    if not candidate.is_absolute():
        candidate = report_root / candidate
    resolved = candidate.resolve()
    try:
        resolved.relative_to(report_root)
    except ValueError as exc:
        raise ValueError(f"Report asset path escapes report directory: {asset_path}") from exc
    return resolved


def relative_asset_path(path: str | Path, report_dir: str | Path) -> str:
    return Path(path).resolve().relative_to(Path(report_dir).resolve()).as_posix()


def has_external_reference(value: str) -> bool:
    lowered = value.strip().lower()
    return lowered.startswith(("http://", "https://", "//"))


@dataclass
class StaticHtmlIssue:
    severity: str
    message: str
    value: str = ""

    def to_dict(self) -> dict[str, str]:
        return {"severity": self.severity, "message": self.message, "value": self.value}


class _StaticHtmlParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.issues: list[StaticHtmlIssue] = []

    def handle_starttag(self, tag: str, attrs: Iterable[tuple[str, str | None]]) -> None:
        attrs_dict = {key.lower(): value or "" for key, value in attrs}
        for key in ["src", "href"]:
            value = attrs_dict.get(key, "")
            if has_external_reference(value):
                self.issues.append(
                    StaticHtmlIssue("error", f"external {key} reference is not portable", value)
                )
        if tag.lower() == "script" and attrs_dict.get("src", "").strip() == "":
            return
        if tag.lower() == "script" and has_external_reference(attrs_dict.get("src", "")):
            self.issues.append(StaticHtmlIssue("error", "external script is not portable"))


def check_static_html_safety(html: str) -> list[StaticHtmlIssue]:
    parser = _StaticHtmlParser()
    parser.feed(html)
    return parser.issues
