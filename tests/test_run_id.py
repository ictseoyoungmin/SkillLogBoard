from skilllogboard.core.run_id import slugify


def test_slugify():
    assert slugify("Hello World!") == "hello_world"
