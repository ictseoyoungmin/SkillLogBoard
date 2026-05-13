from importlib import resources


def test_template_forge_harness_assets_are_packaged():
    package = resources.files("skilllogboard.template_forge.harness")
    names = {
        "research_brief_template.md",
        "template_spec_template.md",
        "template_harness.md",
        "agent_template_creation_guide.md",
        "plugin_template.py.txt",
        "example_template.py.txt",
        "test_template.py.txt",
        "docs_template.md",
    }

    for name in names:
        text = package.joinpath(name).read_text(encoding="utf-8")
        assert text.strip()


def test_harness_and_scaffold_templates_state_safety_policy():
    package = resources.files("skilllogboard.template_forge.harness")
    harness = package.joinpath("template_harness.md").read_text(encoding="utf-8")
    plugin = package.joinpath("plugin_template.py.txt").read_text(encoding="utf-8")
    example = package.joinpath("example_template.py.txt").read_text(encoding="utf-8")
    docs = package.joinpath("docs_template.md").read_text(encoding="utf-8")

    assert "does not call LLMs" in harness
    assert "TODO" in plugin
    assert "RunLogger" in example
    assert "synthetic" in example
    assert "Overview" in docs
    assert "Implemented" not in plugin
