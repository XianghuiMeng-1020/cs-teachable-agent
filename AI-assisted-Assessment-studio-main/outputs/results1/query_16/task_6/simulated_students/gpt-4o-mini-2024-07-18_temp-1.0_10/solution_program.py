class Spaceship:
    def __init__(self, fuel_level=100.0, hyperdrive_multiplier=1.0):
        if fuel_level <= 0:
            raise ValueError('Fuel level must be greater than zero.')
        if hyperdrive_multiplier <= 0:
            raise ValueError('Hyperdrive multiplier must be greater than zero.')
        self.fuel_level = fuel_level
        self.hyperdrive_multiplier = hyperdrive_multiplier

    def calculate_travel_time(self, distance):
        if distance <= 0:
            raise ValueError('Distance must be a positive value.')
        fuel_efficiency = self.fuel_level / 100
        travel_speed = self.hyperdrive_multiplier * fuel_efficiency
        if travel_speed <= 0:
            raise ValueError('Travel speed must be greater than zero.')
        return distance / travel_speed