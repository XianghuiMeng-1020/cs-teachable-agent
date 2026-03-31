# galaxy_explorer.py

class Spaceship:
    def __init__(self, name, fuel_level, destinations):
        self.name = name
        self.fuel_level = fuel_level
        self.destinations = destinations

    def add_fuel(self, amount):
        self.fuel_level += amount

    def travel(self, destination):
        if destination not in self.destinations:
            raise Exception(f"Destination {destination} not on the list.")

        if self.fuel_level < 10:
            raise Exception("Insufficient fuel to travel.")

        # Travel is successful
        self.destinations.remove(destination)
        self.fuel_level -= 10


class Fleet:
    def __init__(self):
        self.ships = []

    def add_spaceship(self, spaceship):
        self.ships.append(spaceship)

    def diagnostic(self):
        diagnostics = {}
        for ship in self.ships:
            status = 'PASS' if ship.fuel_level > 50 else 'FAIL'
            diagnostics[ship.name] = status
        return diagnostics
