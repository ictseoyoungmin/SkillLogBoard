from skilllogboard.agent.decisions import append_agent_decision


def test_append_agent_decision_creates_and_appends(tmp_path):
    path = append_agent_decision(
        tmp_path,
        actor="codex",
        topic="Figure backend",
        decision="Use optional matplotlib",
        reason="Core install must stay light",
    )
    append_agent_decision(
        tmp_path,
        actor="codex",
        topic="Checks",
        decision="Use local files",
        reason="No cloud dependency",
        alternatives=["external service"],
        impact="portable",
    )

    text = path.read_text(encoding="utf-8")
    assert text.count("## ") == 2
    assert "Use optional matplotlib" in text
    assert "external service" in text
