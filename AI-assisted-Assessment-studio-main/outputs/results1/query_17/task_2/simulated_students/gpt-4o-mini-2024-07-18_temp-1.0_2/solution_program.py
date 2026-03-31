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
            raise ValueError(f"Spaceship '{name}' already exists.")
        self.spaceships[name] = Spaceship(name, speed, fuel)

    def remove_spaceship(self, name):
        if name not in self.spaceships:
            raise KeyError(f"Spaceship '{name}' not found.")
        del self.spaceships[name]

    def get_fastest_spaceship(self):
        if not self.spaceships:
            raise RuntimeError("No spaceships in the fleet.")
        fastest_spaceship = max(self.spaceships.values(), key=lambda s: s.speed)
        return fastest_spaceship.name

    def get_fuel_status(self):
        return sorted([{ 'name': s.name, 'fuel': s.fuel } for s in self.spaceships.values()], key=lambda x: x['name'])