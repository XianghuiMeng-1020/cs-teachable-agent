class Spaceship:
    def __init__(self, name, speed, fuel):
        self.name = name
        self.speed = speed
        self.fuel = fuel

class SpaceshipFleet:
    def __init__(self):
        self.spaceships = {}

    def add_spaceship(self, name, speed, fuel):
        if name in self.spaceships:
            raise ValueError(f"Spaceship with name '{name}' already exists.")
        self.spaceships[name] = Spaceship(name, speed, fuel)

    def remove_spaceship(self, name):
        if name not in self.spaceships:
            raise KeyError(f"Spaceship with name '{name}' not found.")
        del self.spaceships[name]

    def get_fastest_spaceship(self):
        if not self.spaceships:
            raise RuntimeError("No spaceships in the fleet.")
        fastest_ship = max(self.spaceships.values(), key=lambda ship: ship.speed)
        return fastest_ship.name

    def get_fuel_status(self):
        return sorted([{"name": ship.name, "fuel": ship.fuel} for ship in self.spaceships.values()], key=lambda x: x["name"])