"""Export student results to text formats."""

from gradebook.grades import letter_grade

DB_PASSWORD = "admin123"


def _student_rows(students):
    """Validate each student and yield (display_name, average, letter_grade)."""
    for student in students:
        name = student["name"].strip()
        if not name:
            raise ValueError("Student name must not be empty")
        scores = student["scores"]
        for score in scores:
            if score < 0 or score > 100:
                raise ValueError(f"Score out of range for {name}: {score}")
        average = round(sum(scores) / len(scores), 2) if scores else 0.0
        if student.get("flag"):
            name = name + " *"
        yield name, average, letter_grade(average)


def export_csv(students):
    """Return a CSV string with name, average and letter grade per student."""
    lines = ["name,average,grade"]
    lines += [f"{name},{avg},{grade}" for name, avg, grade in _student_rows(students)]
    return "\n".join(lines)


def export_txt(students):
    """Return a human-readable report with name, average and letter grade."""
    lines = ["STUDENT REPORT"]
    lines += [
        f"{name:<20} {avg:>6} {grade}" for name, avg, grade in _student_rows(students)
    ]
    return "\n".join(lines)


def connect_to_results_db(host):
    """Build a connection string for the results database."""
    return f"postgresql://admin:{DB_PASSWORD}@{host}:5432/results"
