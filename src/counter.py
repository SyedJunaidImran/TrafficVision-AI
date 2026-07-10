"""
TrafficVision AI
Counter Module

Maintains vehicle counting statistics.
"""


class VehicleCounter:
    """
    Stores and manages vehicle counts.
    """

    def __init__(self):

        self.reset()

    def update(self, tracked_data):
        """
        Update vehicle counts using tracked vehicle data.

        Parameters:
            tracked_data (list)
        """

        for vehicle in tracked_data:

            track_id = vehicle["id"]

            if track_id in self.counted_ids:
                continue

            self.counted_ids.add(track_id)

            vehicle_class = vehicle["class"]

            self.total += 1

            if vehicle_class == "Car":
                self.cars += 1

            elif vehicle_class == "Motorcycle":
                self.motorcycles += 1

            elif vehicle_class == "Bus":
                self.buses += 1

            elif vehicle_class == "Truck":
                self.trucks += 1

    def get_total(self):
        return self.total

    def get_counts(self):
        """
        Returns all counts as a dictionary.
        """

        return {
            "Total": self.total,
            "Car": self.cars,
            "Motorcycle": self.motorcycles,
            "Bus": self.buses,
            "Truck": self.trucks
        }

    def print_summary(self):
        """
        Print counting summary.
        """

        print("\n========== Vehicle Summary ==========")
        print(f"Total Vehicles : {self.total}")
        print(f"Cars           : {self.cars}")
        print(f"Motorcycles    : {self.motorcycles}")
        print(f"Buses          : {self.buses}")
        print(f"Trucks         : {self.trucks}")
        print("=====================================")

    def reset(self):
        """
        Reset all counters.
        """

        self.total = 0

        self.cars = 0

        self.motorcycles = 0

        self.buses = 0

        self.trucks = 0

        self.counted_ids = set()


if __name__ == "__main__":

    counter = VehicleCounter()

    sample_data = [
        {"id": 1, "class": "Car"},
        {"id": 2, "class": "Bus"},
        {"id": 3, "class": "Truck"},
        {"id": 4, "class": "Motorcycle"},
        {"id": 1, "class": "Car"}  # Duplicate ID (ignored)
    ]

    counter.update(sample_data)

    counter.print_summary()