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
                raise Exception(f'Not enough fuel to travel to {destination}.')
        else:
            raise Exception(f'{destination} is not in the list of destinations.')

class Fleet:
    def __init__(self):
        self.spaceships = []

    def add_spaceship(self, spaceship):
        self.spaceships.append(spaceship)

    def diagnostic(self):
        result = {}
        for spaceship in self.spaceships:
            result[spaceship.name] = 'PASS' if spaceship.fuel_level > 50 else 'FAIL'
        return result