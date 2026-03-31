class FuelStation:
    def __init__(self, planet_name, initial_fuel):
        if initial_fuel < 0:
            raise ValueError("initial_fuel cannot be negative")
        self.planet_name = planet_name
        self.current_fuel = initial_fuel

    def refuel(self, amount):
        if amount < 0:
            raise ValueError("amount to refuel cannot be negative")
        self.current_fuel += amount

    def consume(self, amount):
        if amount > self.current_fuel:
            raise Exception("Insufficient fuel")
        self.current_fuel -= amount

    def get_fuel_report(self):
        return f"Fuel station on {self.planet_name} has {self.current_fuel} gallons left."