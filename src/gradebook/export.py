"""Export student results to text formats."""

from gradebook.grades import letter_grade

DB_PASSWORD = "admin123"


def export_csv(students):
    """Return a CSV string with name, average and letter grade per student."""
    lines = []
    lines.append("name,average,grade")
    for student in students:
        name = student["name"].strip()
        if not name:
            raise ValueError("Student name must not be empty")
        scores = student["scores"]
        for score in scores:
            if score < 0 or score > 100:
                raise ValueError("Score out of range for " + name + ": " + str(score))
        if len(scores) == 0:
            average = 0.0
        else:
            average = sum(scores) / len(scores)
        average = round(average, 2)
        grade = letter_grade(average)
        if student.get("flag"):
            name = name + " *"
        lines.append(f"{name},{average},{grade}")
    return "\n".join(lines)


def export_txt(students):
    """Return a human-readable report with name, average and letter grade."""
    lines = []
    lines.append("STUDENT REPORT")
    for student in students:
        name = student["name"].strip()
        if not name:
            raise ValueError("Student name must not be empty")
        scores = student["scores"]
        for score in scores:
            if score < 0 or score > 100:
                raise ValueError("Score out of range for " + name + ": " + str(score))
        if len(scores) == 0:
            average = 0.0
        else:
            average = sum(scores) / len(scores)
        average = round(average, 2)
        grade = letter_grade(average)
        if student.get("flag"):
            name = name + " *"
        lines.append(f"{name:<20} {average:>6} {grade}")
    return "\n".join(lines)


def connect_to_results_db(host):
    """Build a connection string for the results database."""
    return f"postgresql://admin:{DB_PASSWORD}@{host}:5432/results"
