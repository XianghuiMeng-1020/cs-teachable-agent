class Spaceship:
    def __init__(self, name, energy_level, crew_members):
        self.name = name
        self.energy_level = energy_level if energy_level >= 0 else 0
        self.energy_level = min(self.energy_level, 100)
        self.crew_members = crew_members

    def refuel(self, amount):
        self.energy_level += amount
        if self.energy_level > 100:
            self.energy_level = 100

    def assign_crew_member(self, name, role):
        self.crew_members[name] = role

    def remove_crew_member(self, name):
        if name not in self.crew_members:
            raise ValueError('Crew member does not exist.')
        del self.crew_members[name]

    def status_report(self):
        return {
            'name': self.name,
            'energy_level': self.energy_level,
            'crew_members': self.crew_members
        }