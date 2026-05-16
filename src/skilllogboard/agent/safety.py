"""Agent safety gate rules."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
import fnmatch


@dataclass
class SafetyGateResult:
    allowed: bool
    target: str
    reason: str
    code: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentSafetyGate:
    allowed_paths: list[str] = field(default_factory=lambda: ["runs/**", "docs/**", "examples/**", ".devmd/**", "tests/**"])
    denied_paths: list[str] = field(
        default_factory=lambda: [
            "src/skilllogboard/core/**",
            "src/skilllogboard/_version.py",
            "pyproject.toml",
            "**/manifest.yaml",
        ]
    )
    allowed_commands: list[str] = field(default_factory=lambda: ["pytest", "ruff", "skilllog", "python", ".venv/bin/python"])
    denied_commands: list[str] = field(default_factory=lambda: ["rm", "git reset", "git checkout --", "sudo"])

    def evaluate_path(self, path: str | Path) -> SafetyGateResult:
        value = Path(path).as_posix()
        if _matches(value, self.denied_paths):
            return SafetyGateResult(False, value, "path is protected by the default deny list", "PATH_DENIED")
        if _matches(value, self.allowed_paths):
            return SafetyGateResult(True, value, "path is explicitly allowed", "PATH_ALLOWED")
        return SafetyGateResult(False, value, "path is not in allowed_paths", "PATH_NOT_ALLOWED")

    def evaluate_command(self, command: str) -> SafetyGateResult:
        value = command.strip()
        if any(value == denied or value.startswith(denied + " ") for denied in self.denied_commands):
            return SafetyGateResult(False, value, "command is denied by safety policy", "COMMAND_DENIED")
        head = value.split()[0] if value else ""
        if head in self.allowed_commands:
            return SafetyGateResult(True, value, "command is allowed", "COMMAND_ALLOWED")
        return SafetyGateResult(False, value, "command is not in allowed_commands", "COMMAND_NOT_ALLOWED")


def _matches(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)
