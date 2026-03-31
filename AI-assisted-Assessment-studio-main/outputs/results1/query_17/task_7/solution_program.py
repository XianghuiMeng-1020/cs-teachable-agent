class Spaceship:
    def __init__(self, name, fuel_level, destinations):
        self.name = name
        self.fuel_level = fuel_level
        self.destinations = destinations

    def add_fuel(self, amount):
        self.fuel_level += amount

    def travel(self, destination):
        if destination not in self.destinations:
            raise Exception("Destination not found")
        if self.fuel_level < 10:
            raise Exception("Insufficient fuel")
        self.fuel_level -= 10
        self.destinations.remove(destination)


class Fleet:
    def __init__(self):
        self.spaceships = []

    def add_spaceship(self, spaceship):
        self.spaceships.append(spaceship)

    def diagnostic(self):
        report = {}
        for ship in self.spaceships:
            if ship.fuel_level > 50:
                report[ship.name] = 'PASS'
            else:
                report[ship.name] = 'FAIL'
        return report