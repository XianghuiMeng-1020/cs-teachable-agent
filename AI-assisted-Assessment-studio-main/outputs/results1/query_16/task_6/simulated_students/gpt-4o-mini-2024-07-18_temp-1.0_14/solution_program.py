class Spaceship:
    def __init__(self, fuel_level=100.0, hyperdrive_multiplier=1.0):
        if fuel_level <= 0:
            raise ValueError('Fuel level must be positive.')
        if hyperdrive_multiplier <= 0:
            raise ValueError('Hyperdrive multiplier must be positive.')
        self.fuel_level = fuel_level
        self.hyperdrive_multiplier = hyperdrive_multiplier

    def calculate_travel_time(self, distance):
        if distance <= 0:
            raise ValueError('Distance must be positive.')
        fuel_efficiency = self.fuel_level / 100
        time = distance / (self.hyperdrive_multiplier * fuel_efficiency)
        return time