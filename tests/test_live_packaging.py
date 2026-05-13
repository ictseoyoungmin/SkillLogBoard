from importlib import resources


def test_live_template_is_packaged():
    text = resources.files("skilllogboard.live.templates").joinpath("live.html").read_text(
        encoding="utf-8"
    )

    assert "SkillLogBoard Live" in text
