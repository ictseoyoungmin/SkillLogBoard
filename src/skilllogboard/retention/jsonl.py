"""JSONL rotation planning and execution."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
import gzip
import json
import shutil


@dataclass
class JsonlRotationPlan:
    path: str
    should_rotate: bool
    reason: str
    rotated_path: str
    summary_path: str
    line_count: int = 0
    byte_count: int = 0
    dry_run: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def plan_jsonl_rotation(
    path: str | Path,
    max_lines: int | None = None,
    max_bytes: int | None = None,
    compressed: bool = False,
    dry_run: bool = True,
) -> JsonlRotationPlan:
    target = Path(path)
    line_count = _line_count(target) if target.exists() else 0
    byte_count = target.stat().st_size if target.exists() else 0
    should_rotate = False
    reason = "below thresholds"
    if max_lines is not None and line_count > max_lines:
        should_rotate = True
        reason = f"line_count>{max_lines}"
    if max_bytes is not None and byte_count > max_bytes:
        should_rotate = True
        reason = f"byte_count>{max_bytes}"
    suffix = ".1.jsonl.gz" if compressed else ".1.jsonl"
    return JsonlRotationPlan(
        path=str(target),
        should_rotate=should_rotate,
        reason=reason,
        rotated_path=str(target.with_name(target.name + suffix)),
        summary_path=str(target.with_name(target.name + ".summary.json")),
        line_count=line_count,
        byte_count=byte_count,
        dry_run=dry_run,
    )


def rotate_jsonl(
    path: str | Path,
    max_lines: int | None = None,
    max_bytes: int | None = None,
    compressed: bool = False,
    dry_run: bool = True,
) -> JsonlRotationPlan:
    plan = plan_jsonl_rotation(path, max_lines=max_lines, max_bytes=max_bytes, compressed=compressed, dry_run=dry_run)
    if dry_run or not plan.should_rotate:
        return plan
    source = Path(plan.path)
    summary = _summary_snapshot(source)
    Path(plan.summary_path).write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if compressed:
        with source.open("rb") as src, gzip.open(plan.rotated_path, "wb") as dst:
            shutil.copyfileobj(src, dst)
        source.write_text("", encoding="utf-8")
    else:
        source.replace(plan.rotated_path)
        source.write_text("", encoding="utf-8")
    return plan


def _summary_snapshot(path: Path) -> dict[str, Any]:
    counts: dict[str, int] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            counts["invalid"] = counts.get("invalid", 0) + 1
            continue
        key = str(record.get("type") or record.get("event") or record.get("outcome") or "record")
        counts[key] = counts.get(key, 0) + 1
    return {"path": str(path), "counts": counts}


def _line_count(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8") as f:
        return sum(1 for _ in f)
