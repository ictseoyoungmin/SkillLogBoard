"""SkillLogBoard CLI skeleton."""

from __future__ import annotations

from argparse import ArgumentParser
from importlib import resources
from pathlib import Path
import sys

from skilllogboard._version import __version__
from skilllogboard.core.manifest import load_manifest


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
    run_dir = _validate_run_dir(args.run_dir)
    if run_dir is None:
        return 1
    manifest_path = run_dir / "manifest.yaml"
    if not manifest_path.exists():
        print(f"Manifest not found: {manifest_path}", file=sys.stderr)
        return 1
    manifest = load_manifest(manifest_path)
    print(f"Run: {manifest.get('run_name', run_dir.name)}")
    print(f"Run ID: {manifest.get('run_id', run_dir.name)}")
    print(f"Status: {manifest.get('status', 'unknown')}")
    if manifest.get("main_metric"):
        print(f"Main metric: {manifest['main_metric']}")
    if manifest.get("best_metric"):
        print(f"Best metric: {manifest['best_metric']}")
    files = manifest.get("files") or {}
    if files:
        print("Files:")
        for key, value in files.items():
            print(f"  {key}: {value}")
    return 0


def cmd_dashboard(args) -> int:
    from skilllogboard.dashboards.static_builder import build_dashboard

    run_dir = _validate_run_dir(args.run_dir)
    if run_dir is None:
        return 1
    if not (run_dir / "manifest.yaml").exists():
        print(f"Manifest not found: {run_dir / 'manifest.yaml'}", file=sys.stderr)
        return 1
    out = build_dashboard(run_dir)
    print(f"Dashboard written: {out}")
    return 0


def cmd_report(args) -> int:
    from skilllogboard.reports.markdown_report import build_summary

    run_dir = _validate_run_dir(args.run_dir)
    if run_dir is None:
        return 1
    if not (run_dir / "manifest.yaml").exists():
        print(f"Manifest not found: {run_dir / 'manifest.yaml'}", file=sys.stderr)
        return 1
    out = build_summary(run_dir)
    print(f"Summary written: {out}")
    return 0


def cmd_compare(args) -> int:
    from skilllogboard.compare.leaderboard import leaderboard_to_markdown
    from skilllogboard.compare.run_index import build_run_index
    from skilllogboard.dashboards.compare_builder import build_compare_report

    records = build_run_index(args.runs_dir)
    if not records:
        print(f"No run folders with manifest.yaml found under {args.runs_dir}", file=sys.stderr)
        return 1
    paths = build_compare_report(
        args.runs_dir,
        metric=args.metric,
        mode=args.mode,
        output_dir=args.output_dir,
    )
    from skilllogboard.compare.leaderboard import build_leaderboard

    rows = build_leaderboard(records, metric=args.metric, mode=args.mode)
    print(leaderboard_to_markdown(rows))
    print(f"compare.csv: {paths['csv']}")
    print(f"compare.md: {paths['md']}")
    print(f"compare.html: {paths['html']}")
    return 0


def cmd_export_table(args) -> int:
    from skilllogboard.compare.leaderboard import (
        build_leaderboard,
        leaderboard_to_markdown,
        rows_to_latex,
        write_leaderboard_csv,
    )
    from skilllogboard.compare.run_index import build_run_index

    records = build_run_index(args.runs_dir)
    if not records:
        print(f"No run folders with manifest.yaml found under {args.runs_dir}", file=sys.stderr)
        return 1
    rows = build_leaderboard(records, metric=args.metric, mode=args.mode)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    if args.format == "csv":
        write_leaderboard_csv(rows, output)
    elif args.format == "md":
        output.write_text(leaderboard_to_markdown(rows) + "\n", encoding="utf-8")
    else:
        output.write_text(rows_to_latex(rows) + "\n", encoding="utf-8")
    print(f"Table written: {output}")
    return 0


def cmd_planned(args) -> int:
    print(f"`skilllog {args.command}` is planned for Week 5 / v0.4 and is not implemented yet.")
    return 2


def _validate_run_dir(run_dir: str) -> Path | None:
    path = Path(run_dir)
    if not path.exists():
        print(f"Run directory not found: {path}", file=sys.stderr)
        return None
    if not path.is_dir():
        print(f"Run path is not a directory: {path}", file=sys.stderr)
        return None
    return path


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

    p_compare = sub.add_parser("compare", help="Compare multiple run folders")
    p_compare.add_argument("runs_dir")
    p_compare.add_argument("--metric", required=True)
    p_compare.add_argument("--mode", choices=["max", "min"], default="max")
    p_compare.add_argument("--output-dir")
    p_compare.set_defaults(func=cmd_compare)

    p_export = sub.add_parser("export-table", help="Export a compare leaderboard table")
    p_export.add_argument("runs_dir")
    p_export.add_argument("--metric", required=True)
    p_export.add_argument("--mode", choices=["max", "min"], default="max")
    p_export.add_argument("--format", choices=["csv", "md", "latex"], default="csv")
    p_export.add_argument("--output", required=True)
    p_export.set_defaults(func=cmd_export_table)

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
