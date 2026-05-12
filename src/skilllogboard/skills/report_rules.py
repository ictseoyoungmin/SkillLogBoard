"""Validation rules for generated report artifact packages."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from skilllogboard.reports.report_manifest import read_report_manifest
from skilllogboard.skills.parser import RuleSpec
from skilllogboard.skills.rules import OUTCOME_PASSED, RuleResult


def report_manifest_required(report_dir: str | Path, severity: str = "error") -> RuleResult:
    spec = RuleSpec("REPORT-MANIFEST-REQUIRED", "report_manifest_required", severity=severity)
    path = _report_dir(report_dir) / "report_manifest.yaml"
    if not path.exists():
        return _failure(spec, f"Missing report manifest: {path}", {"path": str(path)})
    return _passed(spec, "Report manifest found.", {"path": str(path)})


def required_table(report_dir: str | Path, table: str, severity: str = "error") -> RuleResult:
    spec = RuleSpec("REPORT-REQUIRED-TABLE", "required_table", severity=severity)
    report = _report_dir(report_dir)
    candidates = [report / "tables" / table, report / "tables" / f"{table}.md", report / table]
    if any(path.exists() for path in candidates):
        return _passed(spec, f"Required table found: {table}", {"table": table})
    manifest_match = _manifest_has_output(report, "table", table)
    if manifest_match:
        return _passed(spec, f"Required table found in manifest: {table}", {"table": table})
    return _failure(spec, f"Missing required table: {table}", {"table": table})


def required_figure(report_dir: str | Path, figure: str, severity: str = "warning") -> RuleResult:
    spec = RuleSpec("REPORT-REQUIRED-FIGURE", "required_figure", severity=severity)
    report = _report_dir(report_dir)
    candidates = [report / "figures" / figure, report / "figures" / f"{figure}.png", report / figure]
    if any(path.exists() for path in candidates):
        return _passed(spec, f"Required figure found: {figure}", {"figure": figure})
    manifest_match = _manifest_has_output(report, "figure", figure)
    if manifest_match:
        return _passed(spec, f"Required figure found in manifest: {figure}", {"figure": figure})
    return _failure(spec, f"Missing required figure: {figure}", {"figure": figure})


def report_section_required(report_dir: str | Path, section: str, severity: str = "warning") -> RuleResult:
    spec = RuleSpec("REPORT-SECTION-REQUIRED", "report_section_required", severity=severity)
    report_md = _report_dir(report_dir) / "report.md"
    if not report_md.exists():
        return _failure(spec, f"Missing report.md: {report_md}", {"section": section})
    text = report_md.read_text(encoding="utf-8")
    if f"## {section}" in text or f"# {section}" in text:
        return _passed(spec, f"Required report section found: {section}", {"section": section})
    return _failure(spec, f"Missing required report section: {section}", {"section": section})


def check_report_artifacts(
    report_dir: str | Path,
    required_tables: list[str] | None = None,
    required_figures: list[str] | None = None,
) -> list[RuleResult]:
    results = [report_manifest_required(report_dir)]
    for table in required_tables or []:
        results.append(required_table(report_dir, table))
    for figure in required_figures or []:
        results.append(required_figure(report_dir, figure))
    return results


def _report_dir(path: str | Path) -> Path:
    candidate = Path(path)
    if (candidate / "report_manifest.yaml").exists() or (candidate / "tables").exists():
        return candidate
    if (candidate / "report").exists():
        return candidate / "report"
    return candidate


def _manifest_has_output(report_dir: Path, artifact_type: str, name: str) -> bool:
    path = report_dir / "report_manifest.yaml"
    if not path.exists():
        return False
    manifest = read_report_manifest(path)
    stem = Path(name).stem
    for output in manifest.get("outputs", []):
        if output.get("type") != artifact_type:
            continue
        output_id = str(output.get("id", ""))
        output_path = Path(str(output.get("path", ""))).stem
        if name in {output_id, output_path} or stem in {output_id, output_path}:
            return True
    return False


def _passed(spec: RuleSpec, message: str, details: dict[str, Any]) -> RuleResult:
    return RuleResult(spec.rule_id, spec.rule_type, spec.severity, spec.status, OUTCOME_PASSED, message, details)


def _failure(spec: RuleSpec, message: str, details: dict[str, Any]) -> RuleResult:
    outcome = "error" if spec.severity == "error" else "warning"
    return RuleResult(spec.rule_id, spec.rule_type, spec.severity, spec.status, outcome, message, details)
