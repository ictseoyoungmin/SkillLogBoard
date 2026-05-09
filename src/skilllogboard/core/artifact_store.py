"""Artifact storage and metadata index helpers."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any
import json
import re
import shutil


class ArtifactStore:
    def __init__(self, run_dir: str | Path):
        self.run_dir = Path(run_dir)
        self.artifact_dir = self.run_dir / "artifacts"
        self.index_path = self.run_dir / "artifact_index.json"
        self.artifact_dir.mkdir(parents=True, exist_ok=True)
        if not self.index_path.exists():
            self._write_index({"artifacts": []})

    def log_artifact(self, name: str, path: str | Path, copy: bool = True) -> dict[str, Any]:
        return self.record_file(name=name, path=path, copy=copy, kind="artifact", subdir="artifacts")

    def record_file(
        self,
        name: str,
        path: str | Path,
        copy: bool = True,
        kind: str = "artifact",
        subdir: str = "artifacts",
    ) -> dict[str, Any]:
        src = Path(path)
        rel_path: str | None = None
        size: int | None = None
        if copy:
            if not src.exists() or not src.is_file():
                raise FileNotFoundError(f"Artifact source does not exist or is not a file: {src}")
            target_dir = self.run_dir / subdir
            target_dir.mkdir(parents=True, exist_ok=True)
            dst = self._unique_path(target_dir, self._safe_filename(src.name or name))
            self._assert_inside_run(dst)
            shutil.copy2(src, dst)
            rel_path = dst.relative_to(self.run_dir).as_posix()
            size = dst.stat().st_size
        elif src.exists() and src.is_file():
            size = src.stat().st_size

        record = {
            "name": name,
            "type": kind,
            "source": str(src),
            "path": rel_path,
            "copy": copy,
            "size": size,
            "timestamp": datetime.now().astimezone().isoformat(),
        }
        self.add_record(record)
        return record

    def add_record(self, record: dict[str, Any]) -> dict[str, Any]:
        data = self._read_index()
        data.setdefault("artifacts", []).append(record)
        self._write_index(data)
        return record

    def _read_index(self) -> dict[str, Any]:
        if not self.index_path.exists():
            return {"artifacts": []}
        with self.index_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _write_index(self, data: dict[str, Any]) -> None:
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        with self.index_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _safe_filename(self, value: str) -> str:
        path = Path(value)
        stem = path.stem.strip().lower()
        suffix = path.suffix.lower()
        stem = re.sub(r"[^a-z0-9가-힣._-]+", "_", stem)
        stem = re.sub(r"_+", "_", stem).strip("._-") or "artifact"
        suffix = re.sub(r"[^a-z0-9.]+", "", suffix)
        return f"{stem}{suffix}"

    def _unique_path(self, directory: Path, filename: str) -> Path:
        candidate = directory / filename
        if not candidate.exists():
            return candidate
        stem = candidate.stem
        suffix = candidate.suffix
        for idx in range(1, 1000):
            suffixed = directory / f"{stem}_{idx:03d}{suffix}"
            if not suffixed.exists():
                return suffixed
        raise RuntimeError(f"Could not create unique artifact path for {filename!r}")

    def _assert_inside_run(self, path: Path) -> None:
        path.resolve().relative_to(self.run_dir.resolve())
