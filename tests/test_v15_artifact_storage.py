from skilllogboard.artifacts.storage import store_artifact


def test_store_artifact_records_requested_and_effective_mode(tmp_path):
    source = tmp_path / "plot.txt"
    source.write_text("data", encoding="utf-8")

    result = store_artifact(source, tmp_path / "artifacts", mode="copy")

    assert result["storage_mode"] == "copy"
    assert result["effective_storage_mode"] == "copy"
    assert (tmp_path / "artifacts" / "plot.txt").read_text(encoding="utf-8") == "data"
