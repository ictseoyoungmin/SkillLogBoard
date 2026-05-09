"""Static dashboard placeholder.

Week 3 will replace this with a Jinja2/Plotly dashboard builder.
"""

from __future__ import annotations

from pathlib import Path
import html


def build_dashboard(run_dir: str | Path) -> Path:
    run_dir = Path(run_dir)
    out = run_dir / "dashboard.html"
    title = html.escape(run_dir.name)
    out.write_text(
        f"""<!doctype html>
<html lang="ko">
<head><meta charset="utf-8"><title>SkillLogBoard Dashboard - {title}</title></head>
<body>
  <h1>SkillLogBoard Dashboard</h1>
  <p>Placeholder dashboard for <code>{title}</code>.</p>
  <ul>
    <li><a href="manifest.yaml">manifest.yaml</a></li>
    <li><a href="metrics.csv">metrics.csv</a></li>
    <li><a href="events.jsonl">events.jsonl</a></li>
    <li><a href="summary.md">summary.md</a></li>
  </ul>
</body>
</html>
""",
        encoding="utf-8",
    )
    return out
