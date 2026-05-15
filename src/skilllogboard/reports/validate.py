"""Validation helpers for portable report packages."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from skilllogboard.reports.assets import check_static_html_safety, resolve_asset_path
from skilllogboard.reports.report_manifest import read_report_manifest, validate_report_manifest_schema


@dataclass
class ReportValidationResult:
    outcome: str
    name: str
    message: str
    path: str = ""

    def to_dict(self) -> dict[str, str]:
        return {
            "outcome": self.outcome,
            "name": self.name,
            "message": self.message,
            "path": self.path,
        }


def validate_report_package(report_dir: str | Path) -> list[ReportValidationResult]:
    root = Path(report_dir)
    manifest_path = root / "report_manifest.yaml"
    results: list[ReportValidationResult] = []
    if not manifest_path.exists():
        return [
            ReportValidationResult(
                "error",
                "manifest-present",
                "report_manifest.yaml is required",
                manifest_path.as_posix(),
            )
        ]

    manifest = read_report_manifest(manifest_path)
    schema_errors = validate_report_manifest_schema(manifest)
    if schema_errors:
        for error in schema_errors:
            results.append(ReportValidationResult("error", "manifest-schema", error, manifest_path.as_posix()))
    else:
        results.append(ReportValidationResult("pass", "manifest-schema", "manifest schema is valid", manifest_path.as_posix()))

    for output in manifest.get("outputs", []):
        if not isinstance(output, dict) or not output.get("path"):
            continue
        if (output.get("metadata") or {}).get("status") == "skipped":
            results.append(
                ReportValidationResult(
                    "warning",
                    "output-skipped",
                    f"{output['path']} was recorded as skipped",
                    str(output["path"]),
                )
            )
            continue
        path = resolve_asset_path(root, str(output["path"]))
        if path.exists():
            results.append(ReportValidationResult("pass", "output-present", f"{output['path']} exists", path.as_posix()))
        else:
            results.append(ReportValidationResult("error", "output-present", f"{output['path']} is missing", path.as_posix()))

    html_path = root / "report.html"
    if html_path.exists():
        issues = check_static_html_safety(html_path.read_text(encoding="utf-8"))
        if issues:
            for issue in issues:
                results.append(ReportValidationResult(issue.severity, "offline-html", issue.message, issue.value))
        else:
            results.append(ReportValidationResult("pass", "offline-html", "no external HTML references found", html_path.as_posix()))
    return results


def validation_summary(results: list[ReportValidationResult]) -> dict[str, Any]:
    return {
        "ok": not any(result.outcome == "error" for result in results),
        "results": [result.to_dict() for result in results],
    }
