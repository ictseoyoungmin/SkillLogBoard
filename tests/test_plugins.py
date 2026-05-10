from skilllogboard import RunLogger
from skilllogboard.plugins.base import SkillLogTemplate
from skilllogboard.plugins.registry import TemplateRegistry, get_template, list_templates


def test_default_registry_lists_implemented_and_planned_templates():
    templates = {template.name: template for template in list_templates()}

    assert templates["ir-drop"].is_implemented
    assert templates["trajectory"].is_implemented
    assert templates["classification"].status == "Planned"
    assert templates["segmentation"].status == "Planned"
    assert templates["finance-dashboard"].status == "Planned"
    assert "val/high_drop_f1" in templates["ir-drop"].metric_names
    assert "val/pb_score" in templates["trajectory"].metric_names


def test_registry_register_get_list_round_trip():
    registry = TemplateRegistry()
    template = SkillLogTemplate(
        name="demo-template",
        status="Implemented",
        description="Demo template",
        default_config={"seed": 1},
        metric_names=("demo/score",),
    )

    registry.register(template)

    assert registry.get("demo-template") is template
    assert registry.list() == [template]


def test_core_import_remains_runlogger_only_public_api():
    import skilllogboard

    assert skilllogboard.RunLogger is RunLogger
    assert skilllogboard.__all__ == ["RunLogger", "__version__"]
    assert get_template("ir-drop").default_config["template"] == "ir-drop"
