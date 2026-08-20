import unittest

from RideBooking import RideBooking


class RideBookingQA(unittest.TestCase):

    def setUp(self):
        self.ride = RideBooking()

    def test_normal_booking(self):
        self.assertGreater(
            self.ride.calculate(
                "C",
                "A",
                "B",
                10,
                1,
                "Sedan",
                "14:00"
            ),
            0
        )

    def test_peak_hour(self):

        peak = self.ride.calculate(
            "C",
            "A",
            "B",
            10,
            1,
            "Sedan",
            "18:00"
        )

        normal = self.ride.calculate(
            "C",
            "A",
            "B",
            10,
            1,
            "Sedan",
            "14:00"
        )

        self.assertGreater(peak, normal)

    def test_night_booking(self):

        night = self.ride.calculate(
            "C",
            "A",
            "B",
            10,
            1,
            "Sedan",
            "23:00"
        )

        normal = self.ride.calculate(
            "C",
            "A",
            "B",
            10,
            1,
            "Sedan",
            "14:00"
        )

        self.assertGreater(night, normal)

    def test_invalid_distance(self):

        self.assertEqual(
            self.ride.calculate(
                "C",
                "A",
                "B",
                0,
                1,
                "Sedan",
                "14:00"
            ),
            "Invalid distance"
        )

    def test_invalid_passengers(self):

        self.assertEqual(
            self.ride.calculate(
                "C",
                "A",
                "B",
                10,
                5,
                "Sedan",
                "14:00"
            ),
            "Invalid passenger count"
        )

    def test_unavailable_driver(self):

        self.assertEqual(
            self.ride.calculate(
                "C",
                "A",
                "B",
                10,
                1,
                "Sedan",
                "14:00",
                False
            ),
            "Unavailable driver"
        )

    def test_maximum_discount(self):

        self.assertGreater(
            self.ride.calculate(
                "C",
                "A",
                "B",
                10,
                1,
                "Sedan",
                "14:00",
                True,
                30
            ),
            0
        )

    def test_multiple_vehicle_types(self):

        for vehicle in ["Bike", "Sedan", "SUV", "Premium"]:

            self.assertGreater(
                self.ride.calculate(
                    "C",
                    "A",
                    "B",
                    10,
                    1,
                    vehicle,
                    "14:00"
                ),
                0
            )

    def test_boundary_fare(self):

        self.assertGreaterEqual(
            self.ride.calculate(
                "C",
                "A",
                "B",
                1,
                1,
                "Bike",
                "14:00"
            ),
            0
        )

    def test_driver_allocation(self):

        self.assertEqual(
            self.ride.assign_driver("SUV", True),
            "Driver assigned to SUV"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
