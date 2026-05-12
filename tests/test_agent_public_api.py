def test_agent_public_api_imports_are_available():
    import skilllogboard.agent as agent

    expected = [
        "AgentAction",
        "AgentCheckResult",
        "ControlPlaneResult",
        "HandoffEvidence",
        "append_agent_action",
        "append_agent_decision",
        "build_agent_handoff",
        "check_agent_completion",
        "collect_handoff_evidence",
        "ensure_skilllog_control_plane",
        "load_agent_template",
        "read_agent_actions",
    ]

    for name in expected:
        assert hasattr(agent, name)
        assert name in agent.__all__


def test_agent_public_api_import_boundary_stays_lightweight():
    from skilllogboard.agent import AgentAction, check_agent_completion

    action = AgentAction(actor="codex", action="inspect", status="completed")

    assert action.actor == "codex"
    assert callable(check_agent_completion)
