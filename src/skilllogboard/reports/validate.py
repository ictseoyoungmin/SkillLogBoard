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
    code: str = ""
    severity: str = ""
    suggested_action: str = ""

    def to_dict(self) -> dict[str, str]:
        code = self.code or _default_code(self.name, self.outcome)
        severity = self.severity or self.outcome
        return {
            "outcome": self.outcome,
            "name": self.name,
            "message": self.message,
            "path": self.path,
            "code": code,
            "severity": severity,
            "suggested_action": self.suggested_action or _suggested_action(code, severity),
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
                "MISSING_MANIFEST",
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


def _default_code(name: str, outcome: str) -> str:
    if name == "output-present" and outcome == "error":
        return "MISSING_OUTPUT"
    if name == "manifest-schema" and outcome == "error":
        return "MANIFEST_SCHEMA_ERROR"
    if name == "offline-html" and outcome == "error":
        return "OFFLINE_HTML_EXTERNAL_REFERENCE"
    codes = {
        "manifest-present": "MISSING_MANIFEST",
        "manifest-schema": "MANIFEST_SCHEMA",
        "output-present": "OUTPUT_PRESENT",
        "output-skipped": "OUTPUT_SKIPPED",
        "offline-html": "OFFLINE_HTML",
    }
    return codes.get(name, name.upper().replace("-", "_"))


def _suggested_action(code: str, severity: str) -> str:
    if severity == "pass":
        return ""
    actions = {
        "MISSING_MANIFEST": "Build the report package again or restore report_manifest.yaml.",
        "MANIFEST_SCHEMA": "Inspect report_manifest.yaml and add the required schema fields.",
        "MANIFEST_SCHEMA_ERROR": "Inspect report_manifest.yaml and add the required schema fields.",
        "OUTPUT_PRESENT": "Regenerate the report package or restore the missing output file.",
        "MISSING_OUTPUT": "Regenerate the report package or restore the missing output file.",
        "OUTPUT_SKIPPED": "Review the skipped output metadata and install optional dependencies if needed.",
        "OFFLINE_HTML": "Remove external references or rebuild with an offline render mode.",
        "OFFLINE_HTML_EXTERNAL_REFERENCE": "Remove external references or rebuild with an offline render mode.",
    }
    return actions.get(code, "Inspect the validation message and rebuild the report package if needed.")
