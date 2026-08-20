class RideBooking:

    RATES = {
        "Bike": 10,
        "Sedan": 20,
        "SUV": 30,
        "Premium": 50
    }

    MAX_PASSENGERS = {
        "Bike": 1,
        "Sedan": 4,
        "SUV": 6,
        "Premium": 4
    }

    def calculate(
        self,
        customer_id,
        pickup,
        drop,
        distance,
        passengers,
        vehicle,
        booking_time,
        driver_available=True,
        discount=0
    ):

        if distance <= 0:
            return "Invalid distance"

        if vehicle not in self.RATES:
            return "Invalid vehicle"

        if passengers <= 0 or passengers > self.MAX_PASSENGERS[vehicle]:
            return "Invalid passenger count"

        if not driver_available:
            return "Unavailable driver"

        base_fare = self.RATES[vehicle]

        fare = base_fare + distance * self.RATES[vehicle]

        hour = int(booking_time.split(":")[0])

        # Peak hour
        if 7 <= hour <= 9 or 17 <= hour <= 20:
            fare *= 1.25

        # Night charge
        if hour >= 22 or hour < 6:
            fare *= 1.20

        # Additional passengers
        fare += max(0, passengers - 1) * 50

        # Discount limited to maximum 30%
        discount = min(max(discount, 0), 30)

        fare -= fare * discount / 100

        return round(fare, 2)

    def assign_driver(self, vehicle, available):

        if available:
            return f"Driver assigned to {vehicle}"

        return "No driver available"


if __name__ == "__main__":

    ride = RideBooking()

    print(
        ride.calculate(
            "C1",
            "A",
            "B",
            10,
            2,
            "Sedan",
            "14:00"
        )
    )

    print(ride.assign_driver("Sedan", True))
