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


def test_compiled_live_app_assets_are_packaged():
    app_root = resources.files("skilllogboard.live.static").joinpath("app")
    html = app_root.joinpath("index.html").read_text(encoding="utf-8")
    asset_names = [path.name for path in app_root.joinpath("assets").iterdir()]

    assert 'data-skilllogboard-ui="v1.3-react"' in html
    assert any(name.endswith(".js") for name in asset_names)
    assert any(name.endswith(".css") for name in asset_names)
