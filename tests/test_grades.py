import pytest

from gradebook.grades import calculate_average, letter_grade


@pytest.mark.parametrize(
    "score, expected",
    [(95, "A"), (90, "A"), (85, "B"), (72, "C"), (60, "D"), (10, "F")],
)
def test_letter_grade(score, expected):
    assert letter_grade(score) == expected


def test_letter_grade_rejects_out_of_range():
    with pytest.raises(ValueError):
        letter_grade(101)


def test_calculate_average():
    assert calculate_average([80, 90, 100]) == 90
