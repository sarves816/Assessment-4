from CourseRegistration import CourseRegistration


def test_valid_registration():

    student = CourseRegistration("S001", "CSE", 3)

    result = student.register_course("DBMS")

    assert result == "SUCCESS: Course registered."
    assert student.get_total_credits() == 4

    print("Test Valid registration: PASSED")


def test_missing_prerequisite():

    student = CourseRegistration("S002", "CSE", 3)

    student.completed_courses = set()

    result = student.register_course("DBMS")

    assert result == "ERROR: Missing prerequisite."

    print("Test Missing prerequisite: PASSED")


def test_credit_limit():

    student = CourseRegistration(
        "S003",
        "CSE",
        3,
        max_credits=4
    )

    result1 = student.register_course("DBMS")

    # Change AI semester only for this test
    student.courses["AI"]["semester"] = 3

    result2 = student.register_course("AI")

    assert result1 == "SUCCESS: Course registered."
    assert result2 == "ERROR: Credit limit exceeded."

    print("Test Credit-limit violation: PASSED")


def test_timetable_conflict():

    student = CourseRegistration("S004", "CSE", 5)

    # Make both courses available in semester 5
    student.courses["AI"]["semester"] = 5
    student.courses["ML"]["semester"] = 5

    # Same timetable
    student.courses["AI"]["time"] = "10:00-11:00"
    student.courses["ML"]["time"] = "10:00-11:00"

    result1 = student.register_course("AI")
    result2 = student.register_course("ML")

    assert result1 == "SUCCESS: Course registered."
    assert result2 == "ERROR: Timetable conflict."

    print("Test Timetable conflict: PASSED")


def test_full_course():

    student = CourseRegistration("S005", "CSE", 3)

    student.course_enrollment["DBMS"] = 2

    result = student.register_course("DBMS")

    assert result == "ERROR: Course is full."

    print("Test Full course: PASSED")


def test_duplicate_registration():

    student = CourseRegistration("S006", "CSE", 3)

    result1 = student.register_course("DBMS")
    result2 = student.register_course("DBMS")

    assert result1 == "SUCCESS: Course registered."
    assert result2 == "ERROR: Duplicate registration."

    print("Test Duplicate registration: PASSED")


def test_invalid_course():

    student = CourseRegistration("S007", "CSE", 3)

    result = student.register_course("JAVA")

    assert result == "ERROR: Invalid course."

    print("Test Invalid course: PASSED")


def test_semester_restriction():

    student = CourseRegistration("S008", "CSE", 3)

    result = student.register_course("AI")

    assert result == "ERROR: Semester restriction."

    print("Test Semester restriction: PASSED")


def test_boundary_credit_values():

    student = CourseRegistration(
        "S009",
        "CSE",
        3,
        max_credits=4
    )

    result = student.register_course("DBMS")

    assert result == "SUCCESS: Course registered."
    assert student.get_total_credits() == 4

    print("Test Boundary credit value: PASSED")


def run_all_tests():

    print("=== STARTING COURSE REGISTRATION QA TEST SUITE ===")
    print()

    test_valid_registration()
    test_missing_prerequisite()
    test_credit_limit()
    test_timetable_conflict()
    test_full_course()
    test_duplicate_registration()
    test_invalid_course()
    test_semester_restriction()
    test_boundary_credit_values()

    print()
    print("=== ALL TESTS PASSED ===")


if __name__ == "__main__":
    run_all_tests()
