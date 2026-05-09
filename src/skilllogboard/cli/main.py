"""SkillLogBoard CLI skeleton."""

from __future__ import annotations

from argparse import ArgumentParser
from importlib import resources
from pathlib import Path

from skilllogboard._version import __version__


def _default_skills_text() -> str:
    try:
        return resources.files("skilllogboard.skills").joinpath("default_skills.md").read_text(
            encoding="utf-8"
        )
    except Exception:
        return (
            "# Experiment Skills\n\n"
            "## RULE-CONFIG-001\n"
            "- type: required_config\n"
            "- keys: [model_name, dataset_name, seed, optimizer, lr, batch_size]\n"
            "- severity: warning\n"
        )


def cmd_init(args) -> int:
    Path("runs").mkdir(exist_ok=True)
    skills = Path("Skills.md")
    if not skills.exists():
        skills.write_text(_default_skills_text(), encoding="utf-8")
    print("Initialized SkillLogBoard workspace: runs/, Skills.md")
    return 0


def cmd_inspect(args) -> int:
    run_dir = Path(args.run_dir)
    manifest = run_dir / "manifest.yaml"
    if not manifest.exists():
        print(f"Manifest not found: {manifest}")
        return 1
    print(manifest.read_text(encoding="utf-8"))
    return 0


def cmd_dashboard(args) -> int:
    from skilllogboard.dashboards.static_builder import build_dashboard

    out = build_dashboard(Path(args.run_dir))
    print(f"Dashboard written: {out}")
    return 0


def cmd_report(args) -> int:
    from skilllogboard.reports.markdown_report import build_summary

    out = build_summary(Path(args.run_dir))
    print(f"Summary written: {out}")
    return 0


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(prog="skilllog", description="SkillLogBoard CLI")
    parser.add_argument("--version", action="version", version=f"skilllog {__version__}")

    sub = parser.add_subparsers(dest="command")

    p_init = sub.add_parser("init", help="Create default runs/ and Skills.md")
    p_init.set_defaults(func=cmd_init)

    p_inspect = sub.add_parser("inspect", help="Print manifest for a run directory")
    p_inspect.add_argument("run_dir")
    p_inspect.set_defaults(func=cmd_inspect)

    p_dashboard = sub.add_parser("dashboard", help="Build placeholder dashboard for a run directory")
    p_dashboard.add_argument("run_dir")
    p_dashboard.set_defaults(func=cmd_dashboard)

    p_report = sub.add_parser("report", help="Build placeholder summary.md for a run directory")
    p_report.add_argument("run_dir")
    p_report.set_defaults(func=cmd_report)

    # Week 5 placeholders
    sub.add_parser("compare", help="Planned: compare multiple runs")
    sub.add_parser("export-table", help="Planned: export ablation table")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
