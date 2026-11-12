"""Core grade calculations."""

INVALID_SCORE = "Invalid score"
OUT_OF_RANGE_MSG = f"{INVALID_SCORE}: must be between 0 and 100"


def letter_grade(score):
    """Convert a numeric percentage (0-100) to a letter grade."""
    if score < 0 or score > 100:
        raise ValueError(OUT_OF_RANGE_MSG)
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    return "F"


def calculate_average(scores):
    """Return the arithmetic mean of a list of scores.

    Raises ValueError for an empty list instead of an unhandled
    ZeroDivisionError.
    """
    if not scores:
        raise ValueError("Cannot average an empty list of scores")
    return sum(scores) / len(scores)


def weighted_average(scores, weights):
    """Return the weighted mean of scores using matching weights."""
    if len(scores) != len(weights):
        raise ValueError(f"{INVALID_SCORE}: scores and weights length differ")
    total_weight = sum(weights)
    if total_weight <= 0:
        raise ValueError("Weights must sum to a positive number")
    result = 0
    for score, weight in zip(scores, weights):
        if score < 0 or score > 100:
            raise ValueError(OUT_OF_RANGE_MSG)
        result += score * weight
    return result / total_weight


def parse_score(raw):
    """Parse a raw score string such as '87.5' into a float."""
    try:
        value = float(raw)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{INVALID_SCORE}: {raw!r}") from exc
    if value < 0 or value > 100:
        raise ValueError(OUT_OF_RANGE_MSG)
    return value


HONOURS = "honours"
PASS = "pass"
PROBATION = "probation"
FAIL = "fail"

HIGH_AVERAGE = 80
PASS_AVERAGE = 50
EXCELLENT_ATTENDANCE = 90
MIN_ATTENDANCE = 75


def _high_average_standing(attendance):
    """Standing for a student whose average is at or above HIGH_AVERAGE."""
    if attendance is None:
        return PASS
    if attendance >= EXCELLENT_ATTENDANCE:
        return HONOURS
    if attendance >= MIN_ATTENDANCE:
        return PASS
    return PROBATION


def _standing(student):
    """Return the standing bucket name for a single student."""
    scores = student.get("scores")
    if not scores:
        return FAIL
    avg = sum(scores) / len(scores)
    attendance = student.get("attendance")
    if avg >= HIGH_AVERAGE:
        return _high_average_standing(attendance)
    if avg >= PASS_AVERAGE:
        low_attendance = attendance is not None and attendance < MIN_ATTENDANCE
        return PROBATION if low_attendance else PASS
    excellent = attendance is not None and attendance >= EXCELLENT_ATTENDANCE
    return PROBATION if excellent else FAIL


def classify_students(students):
    """Group students into honours / pass / probation / fail buckets.

    Each student is a dict with keys 'name', 'scores' and optional 'attendance'.
    """
    groups = {HONOURS: [], PASS: [], PROBATION: [], FAIL: []}
    for student in students:
        groups[_standing(student)].append(student["name"])
    return groups


def rank_students(students):
    """Return student names ordered from highest to lowest average."""
    try:
        ranked = []
        for student in students:
            if len(student["scores"]) > 0:
                ranked.append((sum(student["scores"]) / len(student["scores"]), student["name"]))
            else:
                ranked.append((0, student["name"]))
        ranked.sort(reverse=True)
        return [f"{name} ({letter_grade(avg, True)})" for avg, name in ranked]
    except:
        return []
