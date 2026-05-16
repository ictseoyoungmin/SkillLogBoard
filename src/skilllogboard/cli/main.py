"""SkillLogBoard CLI skeleton."""

from __future__ import annotations

from argparse import ArgumentParser, RawDescriptionHelpFormatter, REMAINDER
from importlib import resources
from pathlib import Path
import json
import sys
import webbrowser

from skilllogboard._version import __version__
from skilllogboard.core.manifest import load_manifest
from skilllogboard.core.config_capture import save_config


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
    if args.template:
        return _init_template(args.template)
    skills = Path("Skills.md")
    if not skills.exists():
        skills.write_text(_default_skills_text(), encoding="utf-8")
    print("Initialized SkillLogBoard workspace: runs/, Skills.md")
    return 0


def _init_template(template_name: str) -> int:
    from skilllogboard.plugins.registry import get_template

    try:
        template = get_template(template_name)
    except KeyError:
        print(f"Unknown template: {template_name}", file=sys.stderr)
        return 1
    if not template.is_implemented:
        print(f"Template '{template.name}' is {template.status}; no files were generated.")
        return 2

    written = []
    skipped = []
    skills = Path("Skills.md")
    if skills.exists():
        skipped.append(str(skills))
    else:
        skills.write_text(template.default_skills or _default_skills_text(), encoding="utf-8")
        written.append(str(skills))

    if template.default_config:
        config_path = Path("template_config.yaml")
        if config_path.exists():
            skipped.append(str(config_path))
        else:
            save_config(template.default_config, config_path)
            written.append(str(config_path))

    Path("runs").mkdir(exist_ok=True)
    print(f"Initialized SkillLogBoard workspace for template '{template.name}'.")
    if written:
        print("Written:")
        for path in written:
            print(f"  {path}")
    if skipped:
        print("Skipped existing files:")
        for path in skipped:
            print(f"  {path}")
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
    report_args = list(args.report_args)
    if report_args and report_args[0] == "build":
        return _cmd_report_build(args, report_args[1:])
    if report_args and report_args[0] == "check":
        return _cmd_report_check(args, report_args[1:])
    if report_args and report_args[0] == "validate":
        return _cmd_report_validate(args, report_args[1:])
    if report_args and report_args[0] == "open":
        return _cmd_report_open(args, report_args[1:])
    if report_args and report_args[0] == "bundle":
        return _cmd_report_bundle(args, report_args[1:])
    return _cmd_report_summary(report_args)


def _cmd_report_summary(report_args: list[str]) -> int:
    from skilllogboard.reports.markdown_report import build_summary

    if not report_args:
        print("Usage: skilllog report RUN_DIR | skilllog report build ROOT_OR_RUN_DIR", file=sys.stderr)
        return 2
    run_dir = _validate_run_dir(report_args[0])
    if run_dir is None:
        return 1
    if not (run_dir / "manifest.yaml").exists():
        print(f"Manifest not found: {run_dir / 'manifest.yaml'}", file=sys.stderr)
        return 1
    out = build_summary(run_dir)
    print(f"Summary written: {out}")
    return 0


def _cmd_report_build(parent_args, report_args: list[str]) -> int:
    parser = ArgumentParser(prog="skilllog report build")
    parser.add_argument("root_or_run_dir")
    parser.add_argument("--metric", required=True)
    parser.add_argument("--mode", choices=["max", "min"], default="max")
    parser.add_argument("--spec")
    parser.add_argument("--output-dir")
    parser.add_argument("--group-by", action="append")
    parser.add_argument(
        "--render-mode",
        choices=["minimal", "portable_interactive", "package"],
        default="minimal",
    )
    parsed = parser.parse_args(report_args)

    from skilllogboard.reports.report_builder import build_report_package

    try:
        result = build_report_package(
            parsed.root_or_run_dir,
            metric=parsed.metric,
            mode=parsed.mode,
            output_dir=parsed.output_dir,
            group_by=parsed.group_by,
            spec_path=parsed.spec,
            render_mode=parsed.render_mode,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"Report directory: {result.report_dir}")
    print(f"report.md: {result.report_md}")
    print(f"report.html: {result.report_html}")
    print(f"report_manifest.yaml: {result.report_manifest}")
    for warning in result.warnings:
        print(f"Warning: {warning}")
    return 0


def _cmd_report_check(parent_args, report_args: list[str]) -> int:
    parser = ArgumentParser(prog="skilllog report check")
    parser.add_argument("root_or_report_dir")
    parser.add_argument("--required-table", action="append", default=[])
    parser.add_argument("--required-figure", action="append", default=[])
    parser.add_argument("--json", action="store_true")
    parsed = parser.parse_args(report_args)

    from skilllogboard.skills.report_rules import check_report_artifacts

    results = check_report_artifacts(
        parsed.root_or_report_dir,
        required_tables=parsed.required_table,
        required_figures=parsed.required_figure,
    )
    if parsed.json:
        print(json.dumps([result.to_dict() for result in results], indent=2, sort_keys=True))
    else:
        for result in results:
            print(f"{result.outcome}: {result.rule_type}: {result.message}")
    return 1 if any(result.outcome == "error" for result in results) else 0


def _cmd_report_validate(parent_args, report_args: list[str]) -> int:
    parser = ArgumentParser(prog="skilllog report validate")
    parser.add_argument("report_dir")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--feedback-json", action="store_true")
    parsed = parser.parse_args(report_args)

    from skilllogboard.reports.validate import validate_report_package, validation_summary
    from skilllogboard.agent.feedback import feedback_list

    results = validate_report_package(parsed.report_dir)
    if parsed.feedback_json:
        print(json.dumps(feedback_list(results), indent=2, sort_keys=True))
    elif parsed.json:
        print(json.dumps(validation_summary(results), indent=2, sort_keys=True))
    else:
        for result in results:
            print(f"{result.outcome}: {result.name}: {result.message}")
    return 1 if any(result.outcome == "error" for result in results) else 0


def _cmd_report_open(parent_args, report_args: list[str]) -> int:
    parser = ArgumentParser(prog="skilllog report open")
    parser.add_argument("report_dir")
    parser.add_argument("--dry-run", action="store_true")
    parsed = parser.parse_args(report_args)

    html = Path(parsed.report_dir) / "report.html"
    if not html.exists():
        print(f"Report HTML not found: {html}", file=sys.stderr)
        return 1
    url = html.resolve().as_uri()
    print(f"Report HTML: {url}")
    if not parsed.dry_run:
        webbrowser.open(url)
    return 0


def _cmd_report_bundle(parent_args, report_args: list[str]) -> int:
    parser = ArgumentParser(prog="skilllog report bundle")
    parser.add_argument("report_dir")
    parser.add_argument("--output")
    parsed = parser.parse_args(report_args)

    from skilllogboard.reports.package import bundle_report_zip

    try:
        out = bundle_report_zip(parsed.report_dir, parsed.output)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"Report bundle: {out}")
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
    from skilllogboard.reports.table_builder import (
        build_report_table,
        table_to_csv_string,
        table_to_html,
        table_to_latex,
        table_to_markdown,
    )

    try:
        table = build_report_table(
            args.table,
            args.runs_dir,
            metric=args.metric or "",
            mode=args.mode,
            group_by=args.group_by,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    if not table.rows and args.table not in {"rule-audit", "config-diff"}:
        print(f"No rows generated for table: {args.table}", file=sys.stderr)
        return 1
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    if args.format == "csv":
        output.write_text(table_to_csv_string(table), encoding="utf-8")
    elif args.format == "md":
        output.write_text(table_to_markdown(table) + "\n", encoding="utf-8")
    elif args.format == "latex":
        output.write_text(table_to_latex(table) + "\n", encoding="utf-8")
    elif args.format == "html":
        output.write_text(table_to_html(table) + "\n", encoding="utf-8")
    else:
        import json

        output.write_text(json.dumps(table.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    print(f"Table written: {output}")
    return 0


def cmd_export_figure(args) -> int:
    from skilllogboard.reports.figure_builder import (
        OptionalFigureDependencyError,
        build_ablation_bar_figure,
        build_metric_curve_figure,
        build_metric_curve_overlay_figure,
        build_seed_errorbar_figure,
    )
    from skilllogboard.reports.table_builder import (
        build_ablation_summary_table,
        build_seed_summary_table,
    )

    output = Path(args.output)
    try:
        if args.type == "metric-curve":
            metrics = args.metrics or ([args.metric] if args.metric else [])
            if not metrics:
                print("--metric or --metrics is required for metric-curve", file=sys.stderr)
                return 2
            build_metric_curve_figure(args.root_or_run_dir, metrics, output, format=args.format)
        elif args.type == "metric-curve-overlay":
            if not args.metric:
                print("--metric is required for metric-curve-overlay", file=sys.stderr)
                return 2
            build_metric_curve_overlay_figure(args.root_or_run_dir, args.metric, output, mode=args.mode)
        elif args.type == "seed-errorbar":
            if not args.metric:
                print("--metric is required for seed-errorbar", file=sys.stderr)
                return 2
            table = build_seed_summary_table(
                args.root_or_run_dir,
                metric=args.metric,
                mode=args.mode,
                group_by=args.group_by,
            )
            build_seed_errorbar_figure(table.rows, output)
        else:
            if not args.metric:
                print("--metric is required for ablation-bar", file=sys.stderr)
                return 2
            table = build_ablation_summary_table(args.root_or_run_dir, metric=args.metric, mode=args.mode)
            build_ablation_bar_figure(table.rows, output)
    except OptionalFigureDependencyError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"Figure written: {output}")
    return 0


def cmd_agent(args) -> int:
    agent_args = list(args.agent_args)
    if not agent_args:
        print("Usage: skilllog agent init|log-action|handoff|check|inspect ...", file=sys.stderr)
        return 2
    command = agent_args[0]
    rest = agent_args[1:]
    if command == "init":
        return _cmd_agent_init(rest)
    if command == "log-action":
        return _cmd_agent_log_action(rest)
    if command == "handoff":
        return _cmd_agent_handoff(rest)
    if command == "check":
        return _cmd_agent_check(rest)
    if command == "inspect":
        return _cmd_agent_inspect(rest)
    print(f"Unknown agent command: {command}", file=sys.stderr)
    return 2


def _cmd_agent_init(agent_args: list[str]) -> int:
    parser = ArgumentParser(prog="skilllog agent init")
    parser.add_argument("--root-dir", default=".")
    parser.add_argument("--template")
    parser.add_argument("--force", action="store_true")
    parsed = parser.parse_args(agent_args)

    from skilllogboard.agent.skills import ensure_skilllog_control_plane

    result = ensure_skilllog_control_plane(parsed.root_dir, template=parsed.template, force=parsed.force)
    print(f"Initialized agent control plane: {result.skilllog_dir}")
    if result.created:
        print("Created:")
        for path in result.created:
            print(f"  {path}")
    if result.skipped:
        print("Skipped existing:")
        for path in result.skipped:
            print(f"  {path}")
    return 0


def _cmd_agent_log_action(agent_args: list[str]) -> int:
    parser = ArgumentParser(prog="skilllog agent log-action")
    parser.add_argument("run_dir")
    parser.add_argument("--actor", default="agent")
    parser.add_argument("--action", required=True)
    parser.add_argument("--status", default="completed")
    parser.add_argument("--target", default="")
    parser.add_argument("--command", default="")
    parser.add_argument("--output", action="append", default=[])
    parser.add_argument("--file-changed", action="append", default=[])
    parser.add_argument("--metadata-json", default="{}")
    parsed = parser.parse_args(agent_args)

    from skilllogboard.agent.action_log import append_agent_action

    try:
        metadata = json.loads(parsed.metadata_json)
    except json.JSONDecodeError as exc:
        print(f"Invalid --metadata-json: {exc}", file=sys.stderr)
        return 2
    if parsed.file_changed:
        existing_files = metadata.get("files_changed", [])
        if isinstance(existing_files, str):
            existing_files = [existing_files]
        metadata["files_changed"] = [*list(existing_files or []), *parsed.file_changed]
    path = append_agent_action(
        parsed.run_dir,
        {
            "actor": parsed.actor,
            "action": parsed.action,
            "status": parsed.status,
            "target": parsed.target,
            "command": parsed.command,
            "outputs": parsed.output,
            "metadata": metadata,
        },
    )
    print(f"Agent action logged: {path}")
    return 0


def _cmd_agent_handoff(agent_args: list[str]) -> int:
    parser = ArgumentParser(prog="skilllog agent handoff")
    parser.add_argument("run_dir")
    parser.add_argument("--actor")
    parser.add_argument("--task")
    parser.add_argument("--next", dest="next_steps")
    parser.add_argument("--output")
    parsed = parser.parse_args(agent_args)

    from skilllogboard.agent.handoff import build_agent_handoff

    out = build_agent_handoff(
        parsed.run_dir,
        actor=parsed.actor,
        task=parsed.task,
        next_steps=parsed.next_steps,
        output_path=parsed.output,
    )
    print(f"Agent handoff written: {out}")
    return 0


def _cmd_agent_check(agent_args: list[str]) -> int:
    parser = ArgumentParser(prog="skilllog agent check")
    parser.add_argument("run_dir")
    parser.add_argument("--require-report", action="store_true")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json", action="store_true")
    parsed = parser.parse_args(agent_args)

    from skilllogboard.agent.checks import check_agent_completion

    results = check_agent_completion(parsed.run_dir, require_report=parsed.require_report)
    data = [result.to_dict() for result in results]
    if parsed.json:
        print(json.dumps(data, indent=2, sort_keys=True))
    else:
        for result in results:
            print(f"{result.outcome}: {result.name}: {result.message}")
    failure_outcomes = {"error", "warning"} if parsed.strict else {"error"}
    return 1 if any(result.outcome in failure_outcomes for result in results) else 0


def _cmd_agent_inspect(agent_args: list[str]) -> int:
    parser = ArgumentParser(prog="skilllog agent inspect")
    parser.add_argument("run_dir")
    parsed = parser.parse_args(agent_args)

    from skilllogboard.agent.action_log import read_agent_actions
    from skilllogboard.agent.checks import check_agent_completion

    run_dir = Path(parsed.run_dir)
    actions = read_agent_actions(run_dir)
    print(f"Agent actions: {len(actions)}")
    if actions:
        latest = actions[-1]
        print(f"Latest action: {latest.get('action')} ({latest.get('status')})")
    print(f"Handoff: {'yes' if (run_dir / 'agent' / 'handoff.md').exists() else 'no'}")
    print(f"Decisions: {'yes' if (run_dir / 'agent' / 'decisions.md').exists() else 'no'}")
    errors = [result for result in check_agent_completion(run_dir) if result.outcome == "error"]
    print(f"Check errors: {len(errors)}")
    return 0


def cmd_forge(args) -> int:
    forge_args = list(args.forge_args)
    if not forge_args or forge_args[0] in {"-h", "--help"}:
        print(
            "Usage: skilllog forge COMMAND [options]\n\n"
            "Commands:\n"
            "  init-brief   Write a ResearchBrief.md starter file.\n"
            "  plan         Create a reviewable TemplateSpec.md from a brief.\n"
            "  scaffold     Create plugin/example/test/docs scaffold files.\n"
            "  validate     Validate scaffolded or filled template files.\n\n"
            "Run `skilllog forge COMMAND --help` for command options."
        )
        return 0 if forge_args else 2
    command = forge_args[0]
    rest = forge_args[1:]
    if command == "init-brief":
        return _cmd_forge_init_brief(rest)
    if command == "plan":
        return _cmd_forge_plan(rest)
    if command == "scaffold":
        return _cmd_forge_scaffold(rest)
    if command == "validate":
        return _cmd_forge_validate(rest)
    print(f"Unknown forge command: {command}", file=sys.stderr)
    return 2


def _cmd_forge_init_brief(forge_args: list[str]) -> int:
    parser = ArgumentParser(
        prog="skilllog forge init-brief",
        description="Create a ResearchBrief.md starter file.",
    )
    parser.add_argument("--output", default="ResearchBrief.md", help="Output path.")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing output file.")
    parsed = parser.parse_args(forge_args)

    from skilllogboard.template_forge import load_research_brief_template

    output = Path(parsed.output)
    if output.exists() and not parsed.force:
        print(f"Skipped existing file: {output}")
        return 0
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(load_research_brief_template(), encoding="utf-8")
    print(f"Research brief written: {output}")
    return 0


def _cmd_forge_plan(forge_args: list[str]) -> int:
    parser = ArgumentParser(
        prog="skilllog forge plan",
        description="Create a deterministic TemplateSpec.md draft from ResearchBrief.md.",
    )
    parser.add_argument("--brief", default="ResearchBrief.md", help="Input ResearchBrief.md path.")
    parser.add_argument("--name", help="Template name override, for example custom-task.")
    parser.add_argument("--output", default="TemplateSpec.md", help="Output TemplateSpec.md path.")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing output file.")
    parsed = parser.parse_args(forge_args)

    from skilllogboard.template_forge import (
        draft_template_spec_from_brief,
        parse_research_brief,
        render_template_spec,
    )

    output = Path(parsed.output)
    if output.exists() and not parsed.force:
        print(f"Skipped existing file: {output}")
        return 0
    try:
        brief = parse_research_brief(parsed.brief)
        spec = draft_template_spec_from_brief(brief, template_name=parsed.name)
    except OSError as exc:
        print(f"Could not read research brief {parsed.brief!r}: {exc.strerror}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"Could not create template spec: {exc}", file=sys.stderr)
        return 1
    output.parent.mkdir(parents=True, exist_ok=True)
    text = render_template_spec(spec)
    output.write_text(text, encoding="utf-8")
    print(f"Template spec written: {output}")
    print(f"TODO count: {text.count('TODO')}")
    return 0


def _cmd_forge_scaffold(forge_args: list[str]) -> int:
    parser = ArgumentParser(
        prog="skilllog forge scaffold",
        description="Create plugin, example, test, docs, and .skilllog scaffold files.",
    )
    parser.add_argument("--spec", default="TemplateSpec.md", help="Input TemplateSpec.md path.")
    parser.add_argument("--brief", help="Optional ResearchBrief.md path; creates a draft spec in memory.")
    parser.add_argument("--name", help="Template name override.")
    parser.add_argument("--root-dir", default=".", help="Project root where files will be created.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing scaffold files.")
    parsed = parser.parse_args(forge_args)

    from skilllogboard.template_forge import (
        draft_template_spec_from_brief,
        parse_research_brief,
        parse_template_spec,
        scaffold_template_from_spec,
    )

    try:
        if parsed.brief:
            spec = draft_template_spec_from_brief(
                parse_research_brief(parsed.brief),
                template_name=parsed.name,
            )
        else:
            spec = parse_template_spec(parsed.spec)
            if parsed.name:
                spec.template_name = parsed.name
        result = scaffold_template_from_spec(spec, root_dir=parsed.root_dir, force=parsed.force)
    except OSError as exc:
        source = parsed.brief or parsed.spec
        print(f"Could not read template input {source!r}: {exc.strerror}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"Could not scaffold template: {exc}", file=sys.stderr)
        return 1
    print(f"Template scaffold: {result.template_name}")
    if result.created:
        print("Created:")
        for path in result.created:
            print(f"  {path}")
    if result.skipped:
        print("Skipped existing:")
        for path in result.skipped:
            print(f"  {path}")
    return 0


def _cmd_forge_validate(forge_args: list[str]) -> int:
    parser = ArgumentParser(
        prog="skilllog forge validate",
        description="Validate scaffolded or filled template files without running example training.",
    )
    parser.add_argument("template_name", help="Template name, for example custom-task.")
    parser.add_argument("--root-dir", default=".", help="Project root containing scaffold files.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable validation results.")
    parser.add_argument("--feedback-json", action="store_true", help="Print agent feedback records.")
    parsed = parser.parse_args(forge_args)

    from skilllogboard.template_forge import validate_template

    try:
        results = validate_template(parsed.template_name, root_dir=parsed.root_dir)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    data = [result.to_dict() for result in results]
    if parsed.feedback_json:
        from skilllogboard.agent.feedback import feedback_list

        print(json.dumps(feedback_list(results), indent=2, sort_keys=True))
    elif parsed.json:
        print(json.dumps(data, indent=2, sort_keys=True))
    else:
        for result in results:
            print(f"{result.outcome}: {result.name}: {result.message}")
    return 1 if any(result.outcome == "error" for result in results) else 0


def cmd_watch(args) -> int:
    target = Path(args.target_dir)
    if not target.exists():
        print(f"Watch target not found: {target}", file=sys.stderr)
        return 1
    project_mode = args.project
    if not project_mode and not (target / "manifest.yaml").exists():
        from skilllogboard.live.project import find_run_dirs

        if find_run_dirs(target):
            project_mode = True
            print("No manifest.yaml at target; detected run folders below it and enabled project mode.")
    from skilllogboard.live.server import (
        LiveDependencyError,
        LiveServerOptions,
        require_live_dependencies,
        run_live_server,
    )

    options = LiveServerOptions(
        project=project_mode,
        latest=args.latest,
        log_file=args.log_file,
        poll_interval=args.poll_interval,
        monitor_system=args.monitor_system,
        monitor_gpu=args.monitor_gpu,
    )
    url = f"http://{args.host}:{args.port}"
    print(f"SkillLogBoard Live Board: {url}")
    print(f"Watching: {target}")
    print(f"Mode: {'project' if project_mode else 'run'}")
    print(f"Default view: {'Overview' if project_mode else 'Metric Lab'}")
    try:
        require_live_dependencies()
        if not args.no_open:
            webbrowser.open(url)
        run_live_server(target, host=args.host, port=args.port, options=options)
    except LiveDependencyError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


def cmd_templates(args) -> int:
    from skilllogboard.plugins.registry import list_templates

    print("Templates:")
    for template in list_templates():
        print(f"- {template.name}: {template.status} - {template.description}")
    return 0


def cmd_index(args) -> int:
    index_args = list(args.index_args)
    if index_args and index_args[0] == "rebuild":
        return _cmd_index_rebuild(index_args[1:])
    print("Usage: skilllog index rebuild PROJECT_DIR [--dry-run] [--json]", file=sys.stderr)
    return 2


def _cmd_index_rebuild(index_args: list[str]) -> int:
    parser = ArgumentParser(prog="skilllog index rebuild")
    parser.add_argument("project_dir")
    parser.add_argument("--output")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    parsed = parser.parse_args(index_args)

    from skilllogboard.index.builder import rebuild_project_index

    index, output = rebuild_project_index(parsed.project_dir, output_path=parsed.output, dry_run=parsed.dry_run)
    data = index.to_dict()
    data["output_path"] = str(output)
    data["dry_run"] = parsed.dry_run
    if parsed.json:
        print(json.dumps(data, indent=2, sort_keys=True))
    else:
        action = "Previewed" if parsed.dry_run else "Rebuilt"
        print(f"{action} project index: {output}")
        print(f"Runs: {data['run_count']}")
        print(f"Warnings: {len(data['warnings'])}")
    return 0


def cmd_runs(args) -> int:
    run_args = list(args.run_args)
    if run_args and run_args[0] == "list":
        return _cmd_runs_list(run_args[1:])
    print("Usage: skilllog runs list PROJECT_DIR [--filter EXPR] [--json]", file=sys.stderr)
    return 2


def _cmd_runs_list(run_args: list[str]) -> int:
    parser = ArgumentParser(prog="skilllog runs list")
    parser.add_argument("project_dir")
    parser.add_argument("--filter", default="")
    parser.add_argument("--json", action="store_true")
    parsed = parser.parse_args(run_args)

    from skilllogboard.index.builder import build_project_index
    from skilllogboard.query import filter_runs

    index = build_project_index(parsed.project_dir)
    rows = [run.to_dict() for run in index.runs]
    filtered, parse_result = filter_runs(rows, parsed.filter)
    if parse_result.errors:
        print(json.dumps(parse_result.to_dict(), indent=2, sort_keys=True) if parsed.json else parse_result.errors[0].message, file=sys.stderr)
        return 2
    if parsed.json:
        print(json.dumps({"count": len(filtered), "runs": filtered}, indent=2, sort_keys=True))
    else:
        print("run_id\tstatus\tgroup\ttags\tupdated_at")
        for run in filtered:
            print(
                f"{run['run_id']}\t{run['status']}\t{run.get('group') or ''}\t"
                f"{','.join(run.get('tags') or [])}\t{run.get('updated_at') or 0}"
            )
        print(f"Count: {len(filtered)}")
    return 0


def cmd_prune(args) -> int:
    from skilllogboard.retention.planner import plan_prune
    from skilllogboard.retention.policy import RetentionPolicy

    policy = RetentionPolicy(
        keep_best=args.keep_best,
        keep_latest=args.keep_latest,
        older_than_days=args.older_than_days,
        exclude_tags=args.exclude_tag or [],
        dry_run=not args.execute,
        archive_before_delete=not args.no_archive,
    )
    plan = plan_prune(args.project_dir, policy)
    if args.json:
        print(json.dumps(plan, indent=2, sort_keys=True))
    else:
        mode = "DRY RUN" if plan["dry_run"] else "EXECUTION PLAN"
        print(f"Prune {mode}: {args.project_dir}")
        for action in plan["actions"]:
            print(f"{action['action']}\t{action['run_id']}\t{action['reason']}")
        if not plan["dry_run"]:
            print("Destructive deletion is guarded; archive/delete must be performed by an explicit retention runner.")
    return 0


def cmd_rotate(args) -> int:
    from skilllogboard.retention.jsonl import rotate_jsonl

    run_dir = Path(args.run_dir)
    path = run_dir if run_dir.suffix == ".jsonl" else run_dir / (args.file or "events.jsonl")
    plan = rotate_jsonl(
        path,
        max_lines=args.max_lines,
        max_bytes=args.max_bytes,
        compressed=args.compressed,
        dry_run=not args.execute,
    )
    data = plan.to_dict()
    if args.json:
        print(json.dumps(data, indent=2, sort_keys=True))
    else:
        print(f"Rotation {'preview' if plan.dry_run else 'result'}: {plan.path}")
        print(f"Should rotate: {plan.should_rotate}")
        print(f"Reason: {plan.reason}")
        print(f"Rotated path: {plan.rotated_path}")
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
    p_init.add_argument("--template", help="Initialize Skills.md and config for a template")
    p_init.set_defaults(func=cmd_init)

    p_templates = sub.add_parser("templates", help="List available research templates")
    p_templates.set_defaults(func=cmd_templates)

    p_agent = sub.add_parser("agent", help="Manage local agent research workflow files")
    p_agent.add_argument("agent_args", nargs=REMAINDER)
    p_agent.set_defaults(func=cmd_agent)

    p_index = sub.add_parser("index", help="Build or inspect the derived project index")
    p_index.add_argument("index_args", nargs=REMAINDER)
    p_index.set_defaults(func=cmd_index)

    p_runs = sub.add_parser("runs", help="List project runs with filters")
    p_runs.add_argument("run_args", nargs=REMAINDER)
    p_runs.set_defaults(func=cmd_runs)

    p_watch = sub.add_parser(
        "watch",
        help="Start local-first Live Board for a run or project",
        description=(
            "Start the local-first Live Board. Project mode opens Overview by default; "
            "single-run mode opens Metric Lab by default."
        ),
    )
    p_watch.add_argument("target_dir")
    p_watch.add_argument("--host", default="127.0.0.1")
    p_watch.add_argument("--port", type=int, default=8765)
    p_watch.add_argument("--poll-interval", type=float, default=1.0)
    p_watch.add_argument("--project", action="store_true")
    p_watch.add_argument("--latest", action="store_true")
    p_watch.add_argument("--monitor-system", action="store_true")
    p_watch.add_argument("--monitor-gpu", action="store_true")
    p_watch.add_argument("--log-file")
    p_watch.add_argument("--no-open", action="store_true")
    p_watch.set_defaults(func=cmd_watch)

    p_forge = sub.add_parser(
        "forge",
        help="Create and validate custom template scaffolds",
        description="Create and validate custom template scaffolds.",
        formatter_class=RawDescriptionHelpFormatter,
        epilog=(
            "Commands:\n"
            "  init-brief   Write a ResearchBrief.md starter file\n"
            "  plan         Create a TemplateSpec.md draft from a brief\n"
            "  scaffold     Create plugin/example/test/docs scaffold files\n"
            "  validate     Validate scaffolded or filled template files\n\n"
            "Examples:\n"
            "  skilllog forge init-brief --output ResearchBrief.md\n"
            "  skilllog forge plan --brief ResearchBrief.md --name custom-task\n"
            "  skilllog forge scaffold --spec TemplateSpec.md --root-dir .\n"
            "  skilllog forge validate custom-task --root-dir ."
        ),
    )
    p_forge.add_argument("forge_args", nargs=REMAINDER)
    p_forge.set_defaults(func=cmd_forge)

    p_inspect = sub.add_parser("inspect", help="Print manifest for a run directory")
    p_inspect.add_argument("run_dir")
    p_inspect.set_defaults(func=cmd_inspect)

    p_dashboard = sub.add_parser("dashboard", help="Build placeholder dashboard for a run directory")
    p_dashboard.add_argument("run_dir")
    p_dashboard.set_defaults(func=cmd_dashboard)

    p_report = sub.add_parser(
        "report",
        help="Build summary.md, or use report build/check/validate/open/bundle",
    )
    p_report.add_argument("report_args", nargs=REMAINDER)
    p_report.set_defaults(func=cmd_report)

    p_compare = sub.add_parser("compare", help="Compare multiple run folders")
    p_compare.add_argument("runs_dir")
    p_compare.add_argument("--metric", required=True)
    p_compare.add_argument("--mode", choices=["max", "min"], default="max")
    p_compare.add_argument("--output-dir")
    p_compare.set_defaults(func=cmd_compare)

    p_prune = sub.add_parser("prune", help="Plan retention pruning; dry-run by default")
    p_prune.add_argument("project_dir")
    p_prune.add_argument("--keep-best", type=int, default=1)
    p_prune.add_argument("--keep-latest", type=int, default=3)
    p_prune.add_argument("--older-than-days", type=int)
    p_prune.add_argument("--exclude-tag", action="append")
    p_prune.add_argument("--no-archive", action="store_true")
    p_prune.add_argument("--dry-run", action="store_true", help="Preview only; this is the default")
    p_prune.add_argument("--execute", action="store_true")
    p_prune.add_argument("--json", action="store_true")
    p_prune.set_defaults(func=cmd_prune)

    p_rotate = sub.add_parser("rotate", help="Rotate a run JSONL file; dry-run by default")
    p_rotate.add_argument("run_dir")
    p_rotate.add_argument("--file", default="events.jsonl")
    p_rotate.add_argument("--max-lines", type=int)
    p_rotate.add_argument("--max-bytes", type=int)
    p_rotate.add_argument("--compressed", action="store_true")
    p_rotate.add_argument("--dry-run", action="store_true", help="Preview only; this is the default")
    p_rotate.add_argument("--execute", action="store_true")
    p_rotate.add_argument("--json", action="store_true")
    p_rotate.set_defaults(func=cmd_rotate)

    p_export = sub.add_parser("export-table", help="Export a compare/report table")
    p_export.add_argument("runs_dir")
    p_export.add_argument("--table", default="leaderboard", choices=[
        "leaderboard",
        "seed-summary",
        "ablation-summary",
        "config-diff",
        "rule-audit",
    ])
    p_export.add_argument("--metric")
    p_export.add_argument("--mode", choices=["max", "min"], default="max")
    p_export.add_argument("--group-by", action="append")
    p_export.add_argument("--format", choices=["csv", "md", "latex", "html", "json"], default="csv")
    p_export.add_argument("--output", required=True)
    p_export.set_defaults(func=cmd_export_table)

    p_figure = sub.add_parser("export-figure", help="Export an optional report figure")
    p_figure.add_argument("root_or_run_dir")
    p_figure.add_argument(
        "--type",
        choices=["metric-curve", "metric-curve-overlay", "seed-errorbar", "ablation-bar"],
        default="metric-curve-overlay",
    )
    p_figure.add_argument("--metric")
    p_figure.add_argument("--metrics", action="append")
    p_figure.add_argument("--mode", choices=["max", "min"], default="max")
    p_figure.add_argument("--group-by", action="append")
    p_figure.add_argument("--format", default="png")
    p_figure.add_argument("--output", required=True)
    p_figure.set_defaults(func=cmd_export_figure)

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
