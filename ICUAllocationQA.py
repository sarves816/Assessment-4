from ICUAllocation import ICUAllocation


def run_test_suite():

    print("=== STARTING ICU ALLOCATION QA TEST SUITE ===\n")

    # --------------------------------
    # Test 1: Critical patient
    # --------------------------------

    system = ICUAllocation(2)

    result = system.add_patient(
        "P001",
        70,
        80,
        140,
        80,
        40,
        "Heart disease"
    )

    patient = system.get_patient("P001")

    assert patient["priority"] == "CRITICAL", \
        "Critical patient classification failed"

    assert patient["bed"] == True, \
        "Critical patient did not receive bed"

    print("Test Critical patient: PASSED")


    # --------------------------------
    # Test 2: Normal patient
    # --------------------------------

    system = ICUAllocation(2)

    result = system.add_patient(
        "P002",
        30,
        98,
        75,
        120,
        37,
        "None"
    )

    patient = system.get_patient("P002")

    assert patient["priority"] == "LOW", \
        "Normal patient classification failed"

    assert patient["bed"] == True, \
        "Normal patient did not receive bed"

    print("Test Normal patient: PASSED")


    # --------------------------------
    # Test 3: Emergency case
    # --------------------------------

    system = ICUAllocation(1)

    system.add_patient(
        "P003",
        30,
        95,
        80,
        120,
        37,
        "None"
    )

    result = system.add_patient(
        "P004",
        40,
        92,
        100,
        110,
        37,
        "Emergency",
        emergency=True
    )

    waiting = system.get_waiting_list()

    assert waiting[0] == "P004", \
        "Emergency patient was not given priority"

    print("Test Emergency case: PASSED")


    # --------------------------------
    # Test 4: No ICU beds
    # --------------------------------

    system = ICUAllocation(1)

    system.add_patient(
        "P005",
        50,
        95,
        80,
        120,
        37,
        "None"
    )

    result = system.add_patient(
        "P006",
        40,
        95,
        80,
        120,
        37,
        "None"
    )

    assert "waiting list" in result.lower(), \
        "Patient was not placed on waiting list"

    assert "P006" in system.get_waiting_list(), \
        "Patient missing from waiting list"

    print("Test No ICU beds: PASSED")


    # --------------------------------
    # Test 5: Duplicate patient
    # --------------------------------

    system = ICUAllocation(2)

    system.add_patient(
        "P007",
        30,
        98,
        80,
        120,
        37,
        "None"
    )

    result = system.add_patient(
        "P007",
        40,
        95,
        90,
        110,
        37,
        "None"
    )

    assert "Duplicate" in result, \
        "Duplicate patient ID was not rejected"

    print("Test Duplicate patient: PASSED")


    # --------------------------------
    # Test 6: Invalid oxygen level
    # --------------------------------

    system = ICUAllocation(2)

    result = system.add_patient(
        "P008",
        30,
        150,
        80,
        120,
        37,
        "None"
    )

    assert "Invalid oxygen" in result, \
        "Invalid oxygen level was not detected"

    print("Test Invalid oxygen level: PASSED")


    # --------------------------------
    # Test 7: Invalid heart rate
    # --------------------------------

    system = ICUAllocation(2)

    result = system.add_patient(
        "P009",
        30,
        95,
        0,
        120,
        37,
        "None"
    )

    assert "Invalid heart rate" in result, \
        "Invalid heart rate was not detected"

    print("Test Invalid heart rate: PASSED")


    # --------------------------------
    # Test 8: Priority boundary values
    # --------------------------------

    system = ICUAllocation(2)

    score = system.calculate_priority(
        30,
        94,
        60,
        100,
        37,
        "None"
    )

    priority = system.classify_patient(score)

    assert priority in ["LOW", "MEDIUM", "HIGH", "CRITICAL"], \
        "Invalid priority classification"

    print("Test Priority boundary values: PASSED")


    # --------------------------------
    # Test 9: Multiple patients competing
    # --------------------------------

    system = ICUAllocation(2)

    system.add_patient(
        "P010",
        30,
        95,
        80,
        120,
        37,
        "None"
    )

    system.add_patient(
        "P011",
        70,
        80,
        140,
        80,
        40,
        "Heart disease"
    )

    system.add_patient(
        "P012",
        60,
        85,
        130,
        85,
        39,
        "Diabetes"
    )

    # P012 should be waiting because only 2 beds exist
    assert "P012" in system.get_waiting_list(), \
        "Third patient was not placed on waiting list"

    # Free one bed
    system.available_beds = 1

    allocated = system.allocate_waiting_patients()

    assert "P012" in allocated, \
        "Waiting patient was not allocated"

    print("Test Multiple patients competing for same bed: PASSED")


    print("\n=== ALL QA TESTS PASSED ===")


if __name__ == "__main__":
    run_test_suite()
