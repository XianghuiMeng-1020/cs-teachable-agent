class Spaceship:
    def __init__(self, name, fuel_level, destinations):
        self.name = name
        self.fuel_level = fuel_level
        self.destinations = destinations

    def add_fuel(self, amount):
        self.fuel_level += amount

    def travel(self, destination):
        if destination in self.destinations:
            if self.fuel_level >= 10:
                self.destinations.remove(destination)
                self.fuel_level -= 10
            else:
                raise Exception("Not enough fuel to travel.")
        else:
            raise Exception("Destination not in list.")

class Fleet:
    def __init__(self):
        self.spaceships = []

    def add_spaceship(self, spaceship):
        self.spaceships.append(spaceship)

    def diagnostic(self):
        result = {}
        for ship in self.spaceships:
            result[ship.name] = 'PASS' if ship.fuel_level > 50 else 'FAIL'
        return result