"""
TrafficVision AI
Density Module

Calculates traffic density and congestion level.
"""


class TrafficDensity:

    def __init__(self):
        # Current vehicles in frame
        self.current_density = 0

        # Peak density
        self.peak_density = 0

        # Density history
        self.history = []

        # Congestion level
        self.level = "LOW"

    def update(self, tracked_data):
        """
        Updates traffic density using
        the number of tracked vehicles.
        """
        self.current_density = len(tracked_data)
        self.history.append(self.current_density)

        if self.current_density > self.peak_density:
            self.peak_density = self.current_density

        self.level = self.get_congestion_level()

        return self.current_density

    def get_congestion_level(self):
        """
        Returns congestion level.
        """
        if self.current_density < 5:
            return "LOW"
        elif self.current_density < 15:
            return "MEDIUM"

        return "HIGH"

    def get_density(self):
        """
        Returns current density.
        """
        return self.current_density

    def get_peak_density(self):
        """
        Returns peak density.
        """
        return self.peak_density

    def get_history(self):
        """
        Returns density history.
        """
        return self.history

    def get_statistics(self):
        """
        Returns all density statistics.
        """
        return {
            "current_density": self.current_density,
            "peak_density": self.peak_density,
            "congestion_level": self.level,
            "history": self.history
        }

    def reset(self):
        """
        Reset density statistics.
        """
        self.current_density = 0
        self.peak_density = 0
        self.history.clear()
        self.level = "LOW"


if __name__ == "__main__":
    density = TrafficDensity()

    sample_data = [
        {"id": 1},
        {"id": 2},
        {"id": 3},
        {"id": 4},
        {"id": 5},
        {"id": 6}
    ]

    density.update(sample_data)

    print("Current Density :", density.get_density())
    print("Peak Density    :", density.get_peak_density())
    print("Congestion      :", density.get_congestion_level())