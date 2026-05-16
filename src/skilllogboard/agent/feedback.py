"""Structured validation feedback for agents."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class ValidationFeedback:
    status: str
    code: str
    path: str
    message: str
    suggested_action: str = ""
    severity: str = ""

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["errors"] = [self.message] if self.status == "error" else []
        data["warnings"] = [self.message] if self.status == "warning" else []
        return data


def feedback_from_result(result: Any) -> ValidationFeedback:
    data = result.to_dict() if hasattr(result, "to_dict") else dict(result)
    status = str(data.get("outcome") or data.get("status") or "unknown")
    if status == "passed":
        status = "pass"
    details = data.get("details") if isinstance(data.get("details"), dict) else {}
    code = str(data.get("code") or data.get("check_id") or data.get("name") or "VALIDATION")
    return ValidationFeedback(
        status=status,
        code=code,
        path=str(data.get("path") or details.get("path") or ""),
        message=str(data.get("message") or ""),
        suggested_action=str(data.get("suggested_action") or _default_action(status)),
        severity=str(data.get("severity") or status),
    )


def feedback_list(results: list[Any]) -> list[dict[str, Any]]:
    return [feedback_from_result(result).to_dict() for result in results]


def _default_action(status: str) -> str:
    if status in {"error", "failed"}:
        return "Inspect the reported path and rerun validation."
    if status == "warning":
        return "Review the warning before release."
    return ""
