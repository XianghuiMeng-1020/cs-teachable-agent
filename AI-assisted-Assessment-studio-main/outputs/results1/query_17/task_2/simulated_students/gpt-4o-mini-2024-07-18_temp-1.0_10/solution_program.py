class Spaceship:
    def __init__(self, name, speed, fuel):
        self.name = name
        self.speed = speed
        self.fuel = fuel


class SpaceshipFleet:
    def __init__(self):
        self.fleet = {}

    def add_spaceship(self, name, speed, fuel):
        if name in self.fleet:
            raise ValueError("A spaceship with this name already exists.")
        self.fleet[name] = Spaceship(name, speed, fuel)

    def remove_spaceship(self, name):
        if name not in self.fleet:
            raise KeyError("No spaceship found with this name.")
        del self.fleet[name]

    def get_fastest_spaceship(self):
        if not self.fleet:
            raise RuntimeError("No spaceships in the fleet.")
        return max(self.fleet.values(), key=lambda s: s.speed).name

    def get_fuel_status(self):
        fuel_status = [{"name": s.name, "fuel": s.fuel} for s in self.fleet.values()]
        return sorted(fuel_status, key=lambda x: x["name"])