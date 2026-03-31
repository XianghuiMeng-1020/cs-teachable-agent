class Spaceship:
    def __init__(self, name, distance, fuel):
        self.name = name
        self.distance = distance
        self.fuel = fuel

    def calculate_fuel_efficiency(self):
        if self.fuel == 0:
            raise ValueError('Fuel consumption cannot be zero for efficiency calculation.')
        return self.distance / self.fuel

    def efficiency_report(self):
        fes = self.calculate_fuel_efficiency()
        if fes > 0 and fes <= 2:
            return "Low Efficiency"
        elif fes > 2 and fes <= 5:
            return "Moderate Efficiency"
        elif fes > 5:
            return "High Efficiency"