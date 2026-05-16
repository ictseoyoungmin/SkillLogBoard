"""Markdown backlog and alpha-test feedback writers."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path


SECTIONS = [
    "가설",
    "설계",
    "결과",
    "artifact 인사이트",
    "다음 실험",
    "SkillLog 좋았던 점",
    "불편한 점",
    "개선점",
]


def write_experiment_backlog(
    backlog_dir: str | Path,
    run_id: str,
    experiment_name: str,
    metrics: dict[str, float],
    notes: dict[str, str] | None = None,
) -> Path:
    notes = notes or {}
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = Path(backlog_dir) / f"{timestamp}_{run_id}_experiment.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# {experiment_name} / {run_id}", ""]
    for section in SECTIONS:
        lines.append(f"## {section}")
        if section == "결과":
            for key, value in sorted(metrics.items()):
                lines.append(f"- `{key}`: {value:.6f}")
        else:
            lines.append(notes.get(section, "- TBD"))
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def append_feedback(feedback_path: str | Path, run_id: str, metrics: dict[str, float]) -> None:
    path = Path(feedback_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now().isoformat(timespec="seconds")
    text = (
        f"\n## {now} / {run_id}\n"
        f"- 좋았던 점: RunLogger로 config/metric/artifact/backlog 연결 지점을 한 곳에 묶기 좋음.\n"
        f"- 불편한 점: contest 전용 submission gate와 OOF artifact convention은 사용자가 직접 구현해야 함.\n"
        f"- 개선점: threshold-gated submission writer와 fold-aware experiment template을 SkillLog template로 제공하면 좋음.\n"
        f"- 대표 점수: `{metrics.get('val/r_hit@1cm', 0.0):.6f}`\n"
    )
    with path.open("a", encoding="utf-8") as f:
        f.write(text)
