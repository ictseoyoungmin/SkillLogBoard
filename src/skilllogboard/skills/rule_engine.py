"""Skills.md rule engine."""

from __future__ import annotations

from pathlib import Path

from skilllogboard.core.manifest import load_manifest
from skilllogboard.dashboards.components import group_metrics, load_json, load_metrics, load_yaml
from skilllogboard.skills.parser import RuleSpec, parse_skills
from skilllogboard.skills.rules import RuleResult, execute_rule
from skilllogboard.writers.jsonl_writer import JsonlWriter


class RuleEngine:
    def __init__(self, rules: list[RuleSpec] | None = None, load_error: str | None = None):
        self.rules = rules or []
        self.load_error = load_error

    @classmethod
    def from_file(cls, path: str | Path) -> "RuleEngine":
        path = Path(path)
        if not path.exists():
            return cls(load_error=f"Skills.md not found: {path}")
        return cls(parse_skills(path))

    def run(
        self,
        run_dir: str | Path,
        write_trace: bool = False,
        stage: str | None = None,
    ) -> list[RuleResult]:
        run_dir = Path(run_dir)
        if self.load_error:
            results = [
                RuleResult(
                    rule_id="SKILLS-NOT-FOUND",
                    rule_type="skills_file",
                    severity="warning",
                    status="MVP",
                    outcome="skipped",
                    message=self.load_error,
                    details={"stage": stage},
                )
            ]
        else:
            context = self._load_context(run_dir)
            results = [execute_rule(rule, context) for rule in self.rules]
            if stage is not None:
                for result in results:
                    result.details.setdefault("stage", stage)
        if write_trace:
            self.write_trace(run_dir, results)
        return results

    def write_trace(self, run_dir: str | Path, results: list[RuleResult]) -> Path:
        run_dir = Path(run_dir)
        path = run_dir / "skill_trace.jsonl"
        writer = JsonlWriter(path)
        for result in results:
            writer.write(result)
        self._update_manifest_file_map(run_dir)
        return path

    def _load_context(self, run_dir: Path) -> dict:
        metrics = load_metrics(run_dir / "metrics.csv")
        artifact_index = load_json(run_dir / "artifact_index.json")
        return {
            "manifest": load_yaml(run_dir / "manifest.yaml"),
            "config": load_yaml(run_dir / "config.yaml"),
            "metrics": metrics,
            "metric_series": group_metrics(metrics),
            "artifacts": list(artifact_index.get("artifacts", [])),
        }

    def _update_manifest_file_map(self, run_dir: Path) -> None:
        manifest_path = run_dir / "manifest.yaml"
        if not manifest_path.exists():
            return
        data = load_manifest(manifest_path)
        data.setdefault("files", {})["skill_trace"] = "skill_trace.jsonl"
        from skilllogboard.core.manifest import Manifest

        manifest = Manifest(
            project=data.get("project", ""),
            run_name=data.get("run_name", ""),
            run_id=data.get("run_id", ""),
            run_dir=data.get("run_dir", str(run_dir)),
        )
        for key, value in data.items():
            if hasattr(manifest, key):
                setattr(manifest, key, value)
        manifest.save(manifest_path)
