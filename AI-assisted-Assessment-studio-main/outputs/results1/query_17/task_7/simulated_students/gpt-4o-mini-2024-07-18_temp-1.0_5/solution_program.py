class Spaceship:
    def __init__(self, name, fuel_level, destinations):
        self.name = name
        self.fuel_level = fuel_level
        self.destinations = destinations

    def add_fuel(self, amount):
        self.fuel_level += amount

    def travel(self, destination):
        if destination not in self.destinations:
            raise ValueError(f"Destination '{destination}' not in the ship's list.")
        if self.fuel_level < 10:
            raise RuntimeError("Not enough fuel to travel.")
        self.destinations.remove(destination)
        self.fuel_level -= 10

class Fleet:
    def __init__(self):
        self.spaceships = []

    def add_spaceship(self, spaceship):
        self.spaceships.append(spaceship)

    def diagnostic(self):
        return {ship.name: 'PASS' if ship.fuel_level > 50 else 'FAIL' for ship in self.spaceships}