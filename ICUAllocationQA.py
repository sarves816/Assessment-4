from ICUAllocation import ICUAllocation


def run_test_suite():

    print("======================================")
    print(" ICU ALLOCATION QA TEST SUITE")
    print("======================================")

    # ----------------------------------
    # 1. Critical Patient
    # ----------------------------------

    system = ICUAllocation(2)

    result = system.add_patient(
        "P001",
        70,
        80,
        140,
        80,
        40,
        "Heart Disease"
    )

    patient = system.get_patient("P001")

    assert patient["priority"] == "CRITICAL"
    assert patient["bed_allocated"] is True

    print("Test Critical patient: PASSED")


    # ----------------------------------
    # 2. Normal Patient
    # ----------------------------------

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

    assert patient["priority"] == "LOW"
    assert patient["bed_allocated"] is True

    print("Test Normal patient: PASSED")


    # ----------------------------------
    # 3. Emergency Case
    # ----------------------------------

    system = ICUAllocation(1)

    # First patient occupies the only bed
    system.add_patient(
        "P003",
        30,
        98,
        80,
        120,
        37,
        "None"
    )

    # Emergency patient arrives
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

    assert "EMERGENCY" in result
    assert system.get_waiting_list()[0] == "P004"

    print("Test Emergency case: PASSED")


    # ----------------------------------
    # 4. No ICU Beds
    # ----------------------------------

    system = ICUAllocation(1)

    system.add_patient(
        "P005",
        40,
        98,
        80,
        120,
        37,
        "None"
    )

    result = system.add_patient(
        "P006",
        50,
        95,
        90,
        110,
        37,
        "None"
    )

    assert "waiting list" in result.lower()
    assert "P006" in system.get_waiting_list()

    print("Test No ICU beds: PASSED")


    # ----------------------------------
    # 5. Duplicate Patient
    # ----------------------------------

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

    assert "Duplicate" in result

    print("Test Duplicate patient: PASSED")


    # ----------------------------------
    # 6. Invalid Oxygen Level
    # ----------------------------------

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

    assert "Invalid oxygen level" in result

    print("Test Invalid oxygen level: PASSED")


    # ----------------------------------
    # 7. Invalid Heart Rate
    # ----------------------------------

    system = ICUAllocation(2)

    result = system.add_patient(
        "P009",
        30,
        98,
        0,
        120,
        37,
        "None"
    )

    assert "Invalid heart rate" in result

    print("Test Invalid heart rate: PASSED")


    # ----------------------------------
    # 8. Priority Boundary Values
    # ----------------------------------

    system = ICUAllocation(2)

    score = system.calculate_priority(
        30,
        98,
        75,
        120,
        37,
        "None"
    )

    priority = system.classify_patient(score)

    assert priority == "LOW"

    print("Test Priority boundary values: PASSED")


    # ----------------------------------
    # 9. Multiple Patients Competing
    # ----------------------------------

    system = ICUAllocation(2)

    # Patient 1
    system.add_patient(
        "P010",
        30,
        98,
        80,
        120,
        37,
        "None"
    )

    # Patient 2
    system.add_patient(
        "P011",
        70,
        80,
        140,
        80,
        40,
        "Heart Disease"
    )

    # Patient 3 - no bed
    system.add_patient(
        "P012",
        60,
        85,
        130,
        85,
        39,
        "Diabetes"
    )

    assert "P012" in system.get_waiting_list()

    # Make one bed available
    system.available_beds = 1

    allocated = system.allocate_waiting_patients()

    assert "P012" in allocated

    print("Test Multiple patients competing for same bed: PASSED")


    # ----------------------------------
    # Final Result
    # ----------------------------------

    print()
    print("======================================")
    print(" ALL QA TESTS PASSED")
    print("======================================")


if __name__ == "__main__":
    run_test_suite()
