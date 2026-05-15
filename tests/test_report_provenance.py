from skilllogboard.reports.provenance import ReportProvenance, file_provenance


def test_report_provenance_serializes_sorted_files(tmp_path):
    a = tmp_path / "a.csv"
    b = tmp_path / "b.yaml"
    a.write_text("x", encoding="utf-8")
    b.write_text("y", encoding="utf-8")

    data = ReportProvenance(files=[str(b), str(a), str(a)], metrics=["val/acc"]).to_dict()

    assert data["files"] == sorted({str(a), str(b)})
    assert data["metrics"] == ["val/acc"]


def test_file_provenance_ignores_missing_files(tmp_path):
    existing = tmp_path / "manifest.yaml"
    existing.write_text("run_id: a", encoding="utf-8")

    data = file_provenance([existing, tmp_path / "missing.csv"])

    assert data["files"] == [existing.as_posix()]
