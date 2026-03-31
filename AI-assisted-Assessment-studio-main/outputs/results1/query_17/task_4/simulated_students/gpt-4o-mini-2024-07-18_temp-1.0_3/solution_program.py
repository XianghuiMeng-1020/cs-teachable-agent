class Spaceship:
    def __init__(self, name, energy_level, crew_members):
        self.name = name
        if energy_level < 0:
            self.energy_level = 0
        elif energy_level > 100:
            self.energy_level = 100
        else:
            self.energy_level = energy_level
        self.crew_members = crew_members

    def refuel(self, amount):
        self.energy_level += amount
        if self.energy_level > 100:
            self.energy_level = 100

    def assign_crew_member(self, name, role):
        self.crew_members[name] = role

    def remove_crew_member(self, name):
        if name in self.crew_members:
            del self.crew_members[name]
        else:
            raise ValueError(f'Crew member {name} does not exist.')

    def status_report(self):
        return {
            'name': self.name,
            'energy_level': self.energy_level,
            'crew_members': self.crew_members
        }