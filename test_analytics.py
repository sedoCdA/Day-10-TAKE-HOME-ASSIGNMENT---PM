# test_analytics.py
# Day 10 PM - Tests for student_analytics.py

from student_analytics import (
    create_student,
    calculate_gpa,
    get_top_performers,
    generate_report,
    classify_students,
)

# -----------------------------------------
# Tests for create_student
# -----------------------------------------

# Test 1: Basic creation
s = create_student("Amit", "R001", math=85, python=92, ml=78)
assert s["name"] == "Amit"
assert s["roll"] == "R001"
assert s["marks"] == {"math": 85, "python": 92, "ml": 78}
assert s["attendance"] == 100.0
print("create_student Test 1 passed: basic creation")

# Test 2: Empty name raises ValueError
try:
    create_student("", "R001", math=85)
    assert False, "Should have raised ValueError"
except ValueError:
    print("create_student Test 2 passed: empty name raises ValueError")

# Test 3: Mark out of range raises ValueError
try:
    create_student("Amit", "R001", math=110)
    assert False, "Should have raised ValueError"
except ValueError:
    print("create_student Test 3 passed: mark out of range raises ValueError")

# -----------------------------------------
# Tests for calculate_gpa
# -----------------------------------------

# Test 1: Standard calculation on scale 10
assert calculate_gpa(85, 92, 78) == 8.5
print("calculate_gpa Test 1 passed: standard calculation")

# Test 2: Empty args returns 0.0
assert calculate_gpa() == 0.0
print("calculate_gpa Test 2 passed: empty args returns 0.0")

# Test 3: Custom scale
assert calculate_gpa(80, 80, scale=4.0) == 3.2
print("calculate_gpa Test 3 passed: custom scale")

# -----------------------------------------
# Tests for get_top_performers
# -----------------------------------------
students = [
    create_student("Amit",  "R001", math=85, python=92, ml=78),
    create_student("Priya", "R002", math=95, python=88, ml=91),
    create_student("Rahul", "R003", math=60, python=65, ml=58),
    create_student("Sneha", "R004", math=91, python=95, ml=93),
]

# Test 1: Top 1 overall
top1 = get_top_performers(students, n=1)
assert top1[0]["name"] == "Sneha"
print("get_top_performers Test 1 passed: top 1 overall is Sneha")

# Test 2: Top 1 by subject
top_python = get_top_performers(students, n=1, subject="python")
assert top_python[0]["name"] == "Sneha"
print("get_top_performers Test 2 passed: top 1 python is Sneha")

# Test 3: Empty list returns empty
assert get_top_performers([], n=3) == []
print("get_top_performers Test 3 passed: empty list returns empty")

# -----------------------------------------
# Tests for generate_report
# -----------------------------------------

# Test 1: Report contains student name
report = generate_report(students[0])
assert "Amit" in report
print("generate_report Test 1 passed: name appears in report")

# Test 2: Verbose includes subject marks
report_verbose = generate_report(students[0], verbose=True)
assert "math" in report_verbose
print("generate_report Test 2 passed: verbose includes subject marks")

# Test 3: Invalid input returns error string
report_invalid = generate_report(None)
assert "Error" in report_invalid
print("generate_report Test 3 passed: invalid input returns error string")

# -----------------------------------------
# Tests for classify_students
# -----------------------------------------

# Test 1: Sneha (avg 93) should be in grade A
classified = classify_students(students)
a_names = [s["name"] for s in classified["A"]]
assert "Sneha" in a_names
print("classify_students Test 1 passed: Sneha in grade A")

# Test 2: Rahul (avg 61) should be in grade C
c_names = [s["name"] for s in classified["C"]]
assert "Rahul" in c_names
print("classify_students Test 2 passed: Rahul in grade C")

# Test 3: Empty list returns empty bands
empty = classify_students([])
assert empty == {"A": [], "B": [], "C": [], "D": []}
print("classify_students Test 3 passed: empty list returns empty bands")

# -----------------------------------------
print("\nAll tests passed.")
