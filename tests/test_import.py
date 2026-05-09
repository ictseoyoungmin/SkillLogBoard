def test_import():
    import skilllogboard

    assert skilllogboard.__version__
    assert skilllogboard.RunLogger
