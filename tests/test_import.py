def test_import():
    import skilllogboard
    from skilllogboard import RunLogger, __version__

    assert skilllogboard.__version__
    assert skilllogboard.RunLogger
    assert RunLogger is skilllogboard.RunLogger
    assert __version__ == skilllogboard.__version__
    assert "RunLogger" in skilllogboard.__all__
    assert "__version__" in skilllogboard.__all__
