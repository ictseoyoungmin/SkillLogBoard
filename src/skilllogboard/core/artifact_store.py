"""Artifact store placeholder.

Week 2 will expand this module with:
- copy/link modes
- hash/size metadata
- safe path handling
- artifact_index.json
"""

from __future__ import annotations

from pathlib import Path
import shutil


class ArtifactStore:
    def __init__(self, run_dir: str | Path):
        self.run_dir = Path(run_dir)
        self.artifact_dir = self.run_dir / "artifacts"
        self.artifact_dir.mkdir(parents=True, exist_ok=True)

    def log_artifact(self, name: str, path: str | Path, copy: bool = True) -> str:
        src = Path(path)
        dst = self.artifact_dir / src.name
        if copy:
            if src.exists() and src.is_file():
                shutil.copy2(src, dst)
            else:
                dst.write_text(f"Placeholder artifact for {name}: source not found: {src}\n", encoding="utf-8")
        else:
            dst.write_text(f"Linked artifact placeholder: {src}\n", encoding="utf-8")
        return str(dst.relative_to(self.run_dir))
