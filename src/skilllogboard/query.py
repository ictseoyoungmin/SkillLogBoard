"""Run query filters used by list and compare commands."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
import operator
import re


@dataclass
class FilterError:
    expression: str
    code: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {"expression": self.expression, "code": self.code, "message": self.message}


@dataclass
class FilterParseResult:
    filters: list[dict[str, Any]] = field(default_factory=list)
    errors: list[FilterError] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "filters": self.filters,
            "errors": [error.to_dict() for error in self.errors],
        }


_METRIC_RE = re.compile(r"^metric:([^<>=!]+)(>=|<=|>|<|==|=)(.+)$")
_UPDATED_RE = re.compile(r"^updated(>=|<=|>|<|==|=)(.+)$")
_OPS = {
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
    "=": operator.eq,
    "==": operator.eq,
}


def parse_filter_expression(expression: str | None) -> FilterParseResult:
    result = FilterParseResult()
    if not expression:
        return result
    tokens = [token.strip() for token in re.split(r"[\s,]+", expression) if token.strip()]
    for token in tokens:
        if token.startswith("status:"):
            result.filters.append({"kind": "status", "value": token.split(":", 1)[1]})
        elif token.startswith("tag:"):
            result.filters.append({"kind": "tag", "value": token.split(":", 1)[1]})
        elif token.startswith("group:"):
            result.filters.append({"kind": "group", "value": token.split(":", 1)[1]})
        elif token.startswith("baseline:"):
            result.filters.append({"kind": "baseline", "value": _truthy(token.split(":", 1)[1])})
        elif match := _METRIC_RE.match(token):
            name, op, raw_value = match.groups()
            try:
                value = float(raw_value)
            except ValueError:
                result.errors.append(FilterError(token, "INVALID_METRIC_THRESHOLD", "Metric threshold must be numeric."))
                continue
            result.filters.append({"kind": "metric", "name": name, "op": op, "value": value})
        elif match := _UPDATED_RE.match(token):
            op, raw_value = match.groups()
            timestamp = _parse_time(raw_value)
            if timestamp is None:
                result.errors.append(FilterError(token, "INVALID_UPDATED_RANGE", "updated filter must be a timestamp or YYYY-MM-DD."))
                continue
            result.filters.append({"kind": "updated", "op": op, "value": timestamp})
        else:
            result.errors.append(FilterError(token, "UNKNOWN_FILTER", "Supported filters: status, tag, group, baseline, metric, updated."))
    return result


def filter_runs(runs: list[dict[str, Any]], expression: str | None) -> tuple[list[dict[str, Any]], FilterParseResult]:
    parsed = parse_filter_expression(expression)
    if parsed.errors:
        return [], parsed
    return [run for run in runs if match_run(run, parsed.filters)], parsed


def match_run(run: dict[str, Any], filters: list[dict[str, Any]]) -> bool:
    for item in filters:
        kind = item["kind"]
        if kind == "status" and str(run.get("status") or "") != item["value"]:
            return False
        if kind == "tag" and item["value"] not in {str(tag) for tag in run.get("tags") or []}:
            return False
        if kind == "group" and str(run.get("group") or "") != item["value"]:
            return False
        if kind == "baseline" and bool(run.get("baseline")) is not bool(item["value"]):
            return False
        if kind == "metric" and not _match_metric(run, item):
            return False
        if kind == "updated" and not _match_updated(run, item):
            return False
    return True


def _match_metric(run: dict[str, Any], item: dict[str, Any]) -> bool:
    name = item["name"]
    candidate: Any = None
    for summary in run.get("metric_summaries") or run.get("metric_catalog") or []:
        if isinstance(summary, dict) and summary.get("name") == name:
            candidate = summary.get("best", summary.get("last_value", summary.get("latest")))
            break
    if candidate is None:
        metrics = run.get("metrics") or run.get("key_metrics") or {}
        metric = metrics.get(name) if isinstance(metrics, dict) else None
        candidate = metric.get("value") if isinstance(metric, dict) else metric
    return isinstance(candidate, (int, float)) and _OPS[item["op"]](float(candidate), item["value"])


def _match_updated(run: dict[str, Any], item: dict[str, Any]) -> bool:
    value = run.get("updated_at", run.get("updated", run.get("mtime")))
    try:
        timestamp = float(value)
    except (TypeError, ValueError):
        return False
    return _OPS[item["op"]](timestamp, item["value"])


def _truthy(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y", "baseline"}


def _parse_time(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        pass
    try:
        return datetime.fromisoformat(value).timestamp()
    except ValueError:
        return None
