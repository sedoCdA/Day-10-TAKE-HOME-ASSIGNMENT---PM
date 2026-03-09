# student_analytics.py
# Day 10 PM - Student Performance Analytics Module

from collections import defaultdict


# -----------------------------------------
# 1. create_student
# -----------------------------------------
def create_student(name: str, roll: str, **marks) -> dict:
    """
    Creates a student record as a dict.

    Args:
        name: Full name of the student.
        roll: Unique roll number.
        **marks: Subject names and marks as keyword arguments.
                 Example: math=85, python=92, ml=78

    Returns:
        A dict with keys: name, roll, marks, attendance.

    Raises:
        ValueError: If name or roll is empty.
        ValueError: If any mark is outside the range 0-100.

    Example:
        >>> create_student('Amit', 'R001', math=85, python=92)
        {'name': 'Amit', 'roll': 'R001', 'marks': {'math': 85, 'python': 92}, 'attendance': 100.0}
    """
    if not name or not name.strip():
        raise ValueError("Student name cannot be empty.")
    if not roll or not roll.strip():
        raise ValueError("Roll number cannot be empty.")
    for subject, mark in marks.items():
        if not (0 <= mark <= 100):
            raise ValueError(f"Mark for '{subject}' must be between 0 and 100.")

    return {
        "name":       name.strip(),
        "roll":       roll.strip(),
        "marks":      marks,
        "attendance": 100.0,
    }


# -----------------------------------------
# 2. calculate_gpa
# -----------------------------------------
def calculate_gpa(*marks: float, scale: float = 10.0) -> float:
    """
    Calculates GPA from any number of subject marks.

    Args:
        *marks: Variable number of marks (0-100 scale).
        scale: The GPA scale to convert to. Defaults to 10.0.

    Returns:
        GPA as a float rounded to 2 decimal places.
        Returns 0.0 if no marks are provided.

    Example:
        >>> calculate_gpa(85, 92, 78)
        8.5
    """
    if not marks:
        return 0.0
    average = sum(marks) / len(marks)
    return round((average / 100) * scale, 2)


# -----------------------------------------
# 3. get_top_performers
# -----------------------------------------
def get_top_performers(
    students: list[dict],
    n: int = 5,
    subject: str = None
) -> list[dict]:
    """
    Returns the top n students by overall average or by a specific subject.

    Args:
        students: List of student dicts.
        n: Number of top students to return. Defaults to 5.
        subject: If provided, rank by this subject's marks.
                 If None, rank by overall average across all subjects.

    Returns:
        List of top n student dicts sorted in descending order.
        Returns empty list if input is empty or n <= 0.

    Example:
        >>> get_top_performers(students, n=1, subject='python')
        [{'name': 'Amit', ...}]
    """
    if not students or n <= 0:
        return []

    def score(student: dict) -> float:
        marks = student.get("marks", {})
        if not marks:
            return 0.0
        if subject:
            return marks.get(subject, 0)
        return sum(marks.values()) / len(marks)

    sorted_students = sorted(students, key=score, reverse=True)
    return sorted_students[:n]


# -----------------------------------------
# 4. generate_report
# -----------------------------------------
def generate_report(student: dict, **options) -> str:
    """
    Generates a formatted performance report for a student.

    Args:
        student: A student dict containing name, roll, marks, attendance.
        **options: Optional keyword arguments to customise the report.
            include_rank (bool): Include rank in report. Defaults to False.
            include_grade (bool): Include letter grade. Defaults to True.
            verbose (bool): Include all subject marks. Defaults to False.

    Returns:
        A formatted report string.
        Returns error message string if student dict is invalid.

    Example:
        >>> generate_report(student, include_grade=True, verbose=True)
        'Report for Amit (R001)...'
    """
    if not student or not isinstance(student, dict):
        return "Error: Invalid student data."

    include_grade = options.get("include_grade", True)
    include_rank  = options.get("include_rank",  False)
    verbose       = options.get("verbose",        False)

    name       = student.get("name", "Unknown")
    roll       = student.get("roll", "N/A")
    marks      = student.get("marks", {})
    attendance = student.get("attendance", 0.0)

    avg = sum(marks.values()) / len(marks) if marks else 0.0
    gpa = calculate_gpa(*marks.values())

    def get_grade(average: float) -> str:
        if average >= 90: return "A"
        if average >= 75: return "B"
        if average >= 60: return "C"
        return "D"

    lines = [
        f"Report for {name} ({roll})",
        f"  Attendance : {attendance:.1f}%",
        f"  Average    : {avg:.2f}",
        f"  GPA        : {gpa}",
    ]

    if include_grade:
        lines.append(f"  Grade      : {get_grade(avg)}")

    if include_rank:
        rank = options.get("rank", "N/A")
        lines.append(f"  Rank       : {rank}")

    if verbose and marks:
        lines.append("  Subject Marks:")
        for subject, mark in marks.items():
            lines.append(f"    - {subject}: {mark}")

    return "\n".join(lines)


# -----------------------------------------
# 5. classify_students
# -----------------------------------------
def classify_students(students: list[dict]) -> dict:
    """
    Classifies students into grade bands based on overall average.

    Grade bands:
        A: average >= 90
        B: average >= 75
        C: average >= 60
        D: average < 60

    Args:
        students: List of student dicts.

    Returns:
        Dict with keys 'A', 'B', 'C', 'D', each mapping to a list
        of student dicts in that band. Returns empty bands if input
        is empty.

    Example:
        >>> classify_students(students)
        {'A': [...], 'B': [...], 'C': [...], 'D': [...]}
    """
    bands: dict = defaultdict(list)

    for student in students:
        marks = student.get("marks", {})
        if not marks:
            bands["D"].append(student)
            continue
        avg = sum(marks.values()) / len(marks)
        if avg >= 90:
            bands["A"].append(student)
        elif avg >= 75:
            bands["B"].append(student)
        elif avg >= 60:
            bands["C"].append(student)
        else:
            bands["D"].append(student)

    return {grade: bands[grade] for grade in ["A", "B", "C", "D"]}


# -----------------------------------------
# Sample usage
# -----------------------------------------
if __name__ == "__main__":

    students = [
        create_student("Amit",    "R001", math=85, python=92, ml=78),
        create_student("Priya",   "R002", math=95, python=88, ml=91),
        create_student("Rahul",   "R003", math=60, python=65, ml=58),
        create_student("Sneha",   "R004", math=91, python=95, ml=93),
        create_student("Arjun",   "R005", math=72, python=70, ml=68),
        create_student("Divya",   "R006", math=55, python=50, ml=48),
        create_student("Karan",   "R007", math=88, python=84, ml=82),
        create_student("Meera",   "R008", math=45, python=55, ml=50),
    ]

    print("GPA (85, 92, 78):", calculate_gpa(85, 92, 78))

    print("\nTop 3 students overall:")
    for s in get_top_performers(students, n=3):
        print(f"  {s['name']}")

    print("\nTop 2 by Python:")
    for s in get_top_performers(students, n=2, subject="python"):
        print(f"  {s['name']} — {s['marks']['python']}")

    print("\nReport for Priya:")
    print(generate_report(students[1], include_grade=True, verbose=True))

    print("\nClassification:")
    classified = classify_students(students)
    for grade, group in classified.items():
        names = [s["name"] for s in group]
        print(f"  Grade {grade}: {names}")
