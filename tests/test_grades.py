import pytest

from gradebook.grades import (
    calculate_average,
    letter_grade,
    parse_score,
    weighted_average,
)


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


# ---- Added in v1.1.0: independently tested risks + coverage ----
def test_calculate_average_empty_list_raises_value_error():
    # Baseline crashed with ZeroDivisionError; static analysis did not flag it.
    with pytest.raises(ValueError, match="empty"):
        calculate_average([])


def test_letter_grade_rejects_negative():
    with pytest.raises(ValueError, match="between 0 and 100"):
        letter_grade(-1)


def test_weighted_average():
    assert weighted_average([80, 90], [1, 3]) == 87.5


def test_weighted_average_length_mismatch():
    with pytest.raises(ValueError, match="length differ"):
        weighted_average([80, 90], [1])


def test_weighted_average_rejects_out_of_range_score():
    with pytest.raises(ValueError, match="between 0 and 100"):
        weighted_average([80, 120], [1, 1])


def test_weighted_average_zero_weights_raises_value_error():
    with pytest.raises(ValueError, match="positive"):
        weighted_average([80, 90], [0, 0])


@pytest.mark.parametrize("raw, expected", [("87.5", 87.5), ("0", 0.0), (100, 100.0)])
def test_parse_score_valid(raw, expected):
    assert parse_score(raw) == expected


@pytest.mark.parametrize("raw", ["abc", None, "", "101", "-5"])
def test_parse_score_invalid(raw):
    with pytest.raises(ValueError, match="Invalid score"):
        parse_score(raw)


def test_parse_score_chains_original_exception():
    with pytest.raises(ValueError) as info:
        parse_score("abc")
    assert isinstance(info.value.__cause__, ValueError)
