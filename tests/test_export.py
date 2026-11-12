import pytest

from gradebook.export import connect_to_results_db, export_csv, export_txt

STUDENTS = [
    {"name": " Ana ", "scores": [90, 100]},
    {"name": "Ben", "scores": [70, 75], "flag": True},
    {"name": "Cy", "scores": []},
]


def test_export_csv():
    assert export_csv(STUDENTS) == (
        "name,average,grade\n"
        "Ana,95.0,A\n"
        "Ben *,72.5,C\n"
        "Cy,0.0,F"
    )


def test_export_txt():
    lines = export_txt(STUDENTS).splitlines()
    assert lines[0] == "STUDENT REPORT"
    assert lines[1] == f"{'Ana':<20} {95.0:>6} A"
    assert lines[2] == f"{'Ben *':<20} {72.5:>6} C"
    assert lines[3] == f"{'Cy':<20} {0.0:>6} F"


@pytest.mark.parametrize("exporter", [export_csv, export_txt])
def test_exporters_reject_blank_name(exporter):
    with pytest.raises(ValueError, match="name must not be empty"):
        exporter([{"name": "  ", "scores": [50]}])


@pytest.mark.parametrize("exporter", [export_csv, export_txt])
def test_exporters_reject_out_of_range_score(exporter):
    with pytest.raises(ValueError, match="out of range for Ana: 120"):
        exporter([{"name": "Ana", "scores": [90, 120]}])


# ---- Added in v1.1.0: credential no longer hard-coded ----
def test_connection_string_uses_environment_password(monkeypatch):
    monkeypatch.setenv("GRADEBOOK_DB_PASSWORD", "from-env")
    assert connect_to_results_db("db.local") == (
        "postgresql://admin:from-env@db.local:5432/results"
    )


def test_connection_requires_environment_password(monkeypatch):
    monkeypatch.delenv("GRADEBOOK_DB_PASSWORD", raising=False)
    with pytest.raises(RuntimeError, match="GRADEBOOK_DB_PASSWORD"):
        connect_to_results_db("db.local")
