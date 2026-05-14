"""Config, git, and system snapshot helpers.

Week 1 goal:
- provide small, dependency-light snapshot helpers
- keep torch/pandas out of core
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
import json
import platform
import subprocess

import yaml

GIT_CAPTURE_TIMEOUT_SECONDS = 0.5


def save_config(config: dict[str, Any], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(config or {}, f, sort_keys=False, allow_unicode=True)


def capture_system() -> dict[str, Any]:
    return {
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
    }


def capture_git(repo_dir: str | Path = ".") -> dict[str, Any]:
    repo_dir = Path(repo_dir)
    result: dict[str, Any] = {"available": False}
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_dir,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=GIT_CAPTURE_TIMEOUT_SECONDS,
        ).strip()
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_dir,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=GIT_CAPTURE_TIMEOUT_SECONDS,
        ).strip()
        result.update({"available": True, "commit": commit, "branch": branch})
        try:
            dirty_result = subprocess.run(
                ["git", "diff", "--quiet"],
                cwd=repo_dir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
                timeout=GIT_CAPTURE_TIMEOUT_SECONDS,
            )
            result["dirty"] = dirty_result.returncode != 0
        except subprocess.TimeoutExpired:
            result["dirty"] = None
            result["warning"] = "git dirty check timed out"
    except subprocess.TimeoutExpired:
        result.update({"error": "git capture timed out"})
    except Exception as exc:
        result.update({"error": str(exc)})
    return result


def save_json(data: dict[str, Any], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
