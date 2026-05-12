from skilllogboard.agent.skills import load_agent_template


def test_agent_templates_are_package_accessible():
    for name in [
        "agent_skills.md",
        "experiment_plan.md",
        "skilllog_readme.md",
        "rules.md",
        "report_spec.md",
    ]:
        text = load_agent_template(name)
        assert text.strip()
    assert "built-in LLM" in load_agent_template("agent_skills.md")
