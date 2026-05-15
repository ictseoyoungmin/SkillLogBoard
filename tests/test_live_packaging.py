from importlib import resources


def test_live_template_is_packaged():
    text = resources.files("skilllogboard.live.templates").joinpath("live.html").read_text(
        encoding="utf-8"
    )

    assert "SkillLogBoard Live" in text


def test_live_ui_tokens_are_packaged():
    text = resources.files("skilllogboard.live.templates").joinpath("ui_tokens.css").read_text(
        encoding="utf-8"
    )

    assert "--slb-bg" in text
    assert "--slb-cyan" in text


def test_live_static_package_exists_for_built_app_assets():
    static_root = resources.files("skilllogboard.live.static")

    assert static_root.joinpath("__init__.py").is_file()
