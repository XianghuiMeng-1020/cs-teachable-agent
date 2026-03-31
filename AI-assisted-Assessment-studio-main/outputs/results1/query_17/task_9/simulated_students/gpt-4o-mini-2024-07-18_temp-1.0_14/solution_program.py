class Ship:
    def __init__(self, name, max_speed):
        self.name = name
        self.max_speed = max_speed
        self.missions = []

class FleetManager:
    def __init__(self):
        self.ships = {}

    def add_ship(self, name, max_speed):
        if name in self.ships:
            raise ValueError("Ship with this name already exists.")
        self.ships[name] = Ship(name, max_speed)

    def record_mission(self, ship_name, mission):
        if ship_name not in self.ships:
            raise KeyError("Ship does not exist.")
        self.ships[ship_name].missions.append(mission)

    def get_missions(self, ship_name):
        if ship_name not in self.ships:
            return []
        return self.ships[ship_name].missions

    def get_fleet_summary(self):
        summary = {}
        for name, ship in self.ships.items():
            summary[name] = {'max_speed': ship.max_speed, 'missions': ship.missions}
        return summary