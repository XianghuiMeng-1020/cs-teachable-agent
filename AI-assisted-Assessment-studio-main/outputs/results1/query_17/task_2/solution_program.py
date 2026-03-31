class Spaceship:
    def __init__(self, name, speed, fuel):
        self.name = name
        self.speed = speed
        self.fuel = fuel

class SpaceshipFleet:
    def __init__(self):
        self.ships = {}

    def add_spaceship(self, name, speed, fuel):
        if name in self.ships:
            raise ValueError("Spaceship with this name already exists.")
        self.ships[name] = Spaceship(name, speed, fuel)

    def remove_spaceship(self, name):
        if name not in self.ships:
            raise KeyError("Spaceship with this name does not exist.")
        del self.ships[name]

    def get_fastest_spaceship(self):
        if not self.ships:
            raise RuntimeError("No spaceships in fleet.")
        max_speed_ship = max(self.ships.values(), key=lambda ship: ship.speed)
        return max_speed_ship.name

    def get_fuel_status(self):
        return sorted(
            [{'name': ship.name, 'fuel': ship.fuel} for ship in self.ships.values()],
            key=lambda x: x['name']
        )
