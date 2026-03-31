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
            raise ValueError("Spaceship with this name already exists.")
        self.spaceships[name] = Spaceship(name, speed, fuel)

    def remove_spaceship(self, name):
        if name not in self.spaceships:
            raise KeyError("No spaceship found with this name.")
        del self.spaceships[name]

    def get_fastest_spaceship(self):
        if not self.spaceships:
            raise RuntimeError("No spaceships in the fleet.")
        fastest = max(self.spaceships.values(), key=lambda s: s.speed)
        return fastest.name

    def get_fuel_status(self):
        fuel_status = [{"name": s.name, "fuel": s.fuel} for s in self.spaceships.values()]
        return sorted(fuel_status, key=lambda x: x["name"])
