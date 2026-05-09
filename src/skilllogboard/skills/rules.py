"""Built-in Skills.md rule executors."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Callable

from skilllogboard.skills.parser import RuleSpec

OUTCOME_PASSED = "passed"
OUTCOME_WARNING = "warning"
OUTCOME_ERROR = "error"
OUTCOME_SKIPPED = "skipped"
OUTCOME_PLANNED = "planned"

MVP_RULE_TYPES = {
    "required_config",
    "required_metric",
    "metric_threshold",
    "best_last_gap",
    "artifact_required",
}


@dataclass
class RuleResult:
    rule_id: str
    rule_type: str
    severity: str
    status: str
    outcome: str
    message: str
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().astimezone().isoformat())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


RuleExecutor = Callable[[RuleSpec, dict[str, Any]], RuleResult]


def execute_rule(spec: RuleSpec, context: dict[str, Any]) -> RuleResult:
    if spec.status != "MVP":
        return _result(spec, OUTCOME_PLANNED, spec.message or "Rule is planned and was not executed.")
    executor = BUILTIN_RULES.get(spec.rule_type)
    if executor is None:
        return _result(spec, OUTCOME_SKIPPED, f"Unknown rule type: {spec.rule_type}")
    return executor(spec, context)


def required_config(spec: RuleSpec, context: dict[str, Any]) -> RuleResult:
    config = context.get("config") or {}
    keys = _as_list(spec.params.get("keys"))
    if not keys:
        return _failure(spec, "Missing required field for required_config: keys", {"missing": ["keys"]})
    missing = [key for key in keys if key not in config]
    if missing:
        return _failure(spec, f"Missing required config keys: {', '.join(missing)}", {"missing": missing})
    return _result(spec, OUTCOME_PASSED, spec.message or "Required config keys found.", {"keys": keys})


def required_metric(spec: RuleSpec, context: dict[str, Any]) -> RuleResult:
    available = set(context.get("metric_series", {}).keys())
    keys = _as_list(spec.params.get("keys"))
    if not keys:
        return _failure(spec, "Missing required field for required_metric: keys", {"missing": ["keys"]})
    missing = [key for key in keys if key not in available]
    if missing:
        return _failure(spec, f"Missing required metrics: {', '.join(missing)}", {"missing": missing})
    return _result(spec, OUTCOME_PASSED, spec.message or "Required metrics found.", {"keys": keys})


def metric_threshold(spec: RuleSpec, context: dict[str, Any]) -> RuleResult:
    metric = str(spec.params.get("metric", "")).strip()
    if not metric:
        return _failure(spec, "Missing required field for metric_threshold: metric", {"missing": ["metric"]})
    threshold = _as_float(spec.params.get("threshold"))
    if threshold is None:
        return _failure(
            spec,
            "Missing or invalid required field for metric_threshold: threshold",
            {"missing": ["threshold"]},
        )
    mode = str(spec.params.get("mode", "max"))
    series = context.get("metric_series", {}).get(metric, [])
    if not series:
        return _failure(spec, f"Metric not found for threshold rule: {metric}", {"metric": metric})
    observed = float(series[-1]["value"])
    passed = observed >= threshold if mode == "max" else observed <= threshold
    details = {"metric": metric, "observed": observed, "threshold": threshold, "mode": mode}
    if not passed:
        return _failure(spec, f"Metric threshold failed for {metric}.", details)
    return _result(spec, OUTCOME_PASSED, spec.message or f"Metric threshold passed for {metric}.", details)


def best_last_gap(spec: RuleSpec, context: dict[str, Any]) -> RuleResult:
    metric = str(spec.params.get("metric", "")).strip()
    if not metric:
        return _failure(spec, "Missing required field for best_last_gap: metric", {"missing": ["metric"]})
    threshold = _as_float(spec.params.get("threshold"))
    if threshold is None:
        return _failure(
            spec,
            "Missing or invalid required field for best_last_gap: threshold",
            {"missing": ["threshold"]},
        )
    mode = str(spec.params.get("mode", "max"))
    series = context.get("metric_series", {}).get(metric, [])
    if len(series) < 2:
        return _failure(spec, f"Not enough metric points for best_last_gap: {metric}", {"metric": metric})
    values = [float(row["value"]) for row in series]
    best = max(values) if mode == "max" else min(values)
    last = values[-1]
    gap = best - last if mode == "max" else last - best
    details = {"metric": metric, "best": best, "last": last, "gap": gap, "threshold": threshold, "mode": mode}
    if gap > threshold:
        return _failure(spec, f"Best/last gap exceeded threshold for {metric}.", details)
    return _result(spec, OUTCOME_PASSED, spec.message or f"Best/last gap is within threshold for {metric}.", details)


def artifact_required(spec: RuleSpec, context: dict[str, Any]) -> RuleResult:
    required = _as_list(spec.params.get("artifacts", spec.params.get("keys")))
    if not required:
        return _failure(
            spec,
            "Missing required field for artifact_required: artifacts or keys",
            {"missing": ["artifacts"]},
        )
    records = context.get("artifacts") or []
    available = {record.get("name") for record in records}
    missing = [name for name in required if name not in available]
    if missing:
        return _failure(spec, f"Missing required artifacts: {', '.join(missing)}", {"missing": missing})
    return _result(spec, OUTCOME_PASSED, spec.message or "Required artifacts found.", {"artifacts": required})


BUILTIN_RULES: dict[str, RuleExecutor] = {
    "required_config": required_config,
    "required_metric": required_metric,
    "metric_threshold": metric_threshold,
    "best_last_gap": best_last_gap,
    "artifact_required": artifact_required,
}


def _failure(spec: RuleSpec, message: str, details: dict[str, Any] | None = None) -> RuleResult:
    severity = spec.severity.lower()
    return _result(spec, OUTCOME_ERROR if severity == "error" else OUTCOME_WARNING, message, details)


def _result(
    spec: RuleSpec,
    outcome: str,
    message: str,
    details: dict[str, Any] | None = None,
) -> RuleResult:
    return RuleResult(
        rule_id=spec.rule_id,
        rule_type=spec.rule_type,
        severity=spec.severity.lower(),
        status=spec.status,
        outcome=outcome,
        message=message,
        details=details or {},
    )


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def _as_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
