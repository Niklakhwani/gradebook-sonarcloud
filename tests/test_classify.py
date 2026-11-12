"""Characterisation tests: pin current behaviour of classify_students
before refactoring it, so the refactor can be proven behaviour-preserving."""

import pytest

from gradebook.grades import classify_students


def bucket_of(student):
    groups = classify_students([dict(student, name="s")])
    return next(k for k, names in groups.items() if "s" in names)


@pytest.mark.parametrize(
    "scores, attendance, expected",
    [
        ([], None, "fail"),
        ([85], None, "pass"),
        ([85], 95, "honours"),
        ([85], 90, "honours"),
        ([85], 80, "pass"),
        ([85], 75, "pass"),
        ([85], 60, "probation"),
        ([65], None, "pass"),
        ([65], 80, "pass"),
        ([65], 70, "probation"),
        ([40], None, "fail"),
        ([40], 95, "probation"),
        ([40], 80, "fail"),
        ([80], 74, "probation"),
        ([50], 75, "pass"),
    ],
)
def test_classification_matrix(scores, attendance, expected):
    student = {"scores": scores}
    if attendance is not None:
        student["attendance"] = attendance
    assert bucket_of(student) == expected


def test_all_groups_present_for_empty_input():
    assert classify_students([]) == {
        "honours": [], "pass": [], "probation": [], "fail": []
    }
