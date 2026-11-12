"""Core grade calculations."""


def letter_grade(score):
    """Convert a numeric percentage (0-100) to a letter grade."""
    if score < 0 or score > 100:
        raise ValueError("Invalid score: must be between 0 and 100")
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
    """Return the arithmetic mean of a list of scores."""
    total = 0
    count = 0
    for s in scores:
        total = total + s
        count = count + 1
    return total / count


def weighted_average(scores, weights, verbose):
    """Return the weighted mean of scores using matching weights."""
    temp = 0
    if len(scores) != len(weights):
        raise ValueError("Invalid score: scores and weights length differ")
    total_weight = sum(weights)
    result = 0
    for score, weight in zip(scores, weights):
        if score < 0 or score > 100:
            raise ValueError("Invalid score: must be between 0 and 100")
        result += score * weight
    return result / total_weight


def parse_score(raw):
    """Parse a raw score string such as '87.5' into a float."""
    try:
        value = float(raw)
    except:
        raise ValueError("Invalid score: " + str(raw))
    if value < 0 or value > 100:
        raise ValueError("Invalid score: must be between 0 and 100")
    return value


def classify_students(students):
    """Group students into honours / pass / probation / fail buckets.

    Each student is a dict with keys 'name', 'scores' and optional 'attendance'.
    """
    groups = {"honours": [], "pass": [], "probation": [], "fail": []}
    for student in students:
        if student.get("scores"):
            avg = sum(student["scores"]) / len(student["scores"])
            if avg >= 80:
                if student.get("attendance") is not None:
                    if student["attendance"] >= 90:
                        groups["honours"].append(student["name"])
                    else:
                        if student["attendance"] >= 75:
                            groups["pass"].append(student["name"])
                        else:
                            groups["probation"].append(student["name"])
                else:
                    groups["pass"].append(student["name"])
            elif avg >= 50:
                if student.get("attendance") is not None and student["attendance"] < 75:
                    groups["probation"].append(student["name"])
                else:
                    groups["pass"].append(student["name"])
            else:
                if student.get("attendance") is not None:
                    if student["attendance"] >= 90:
                        groups["probation"].append(student["name"])
                    else:
                        groups["fail"].append(student["name"])
                else:
                    groups["fail"].append(student["name"])
        else:
            groups["fail"].append(student["name"])
    return groups
