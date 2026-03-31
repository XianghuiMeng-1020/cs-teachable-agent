class Spaceship:
    def __init__(self, name, energy_level, crew_members):
        self.name = name
        self.energy_level = max(0, min(100, energy_level))  # Initial energy level clamped between 0 and 100
        self.crew_members = crew_members

    def refuel(self, amount):
        self.energy_level = min(100, self.energy_level + amount)
        if self.energy_level < 0:
            self.energy_level = 0

    def assign_crew_member(self, name, role):
        self.crew_members[name] = role

    def remove_crew_member(self, name):
        if name in self.crew_members:
            del self.crew_members[name]
        else:
            raise ValueError("Crew member not found")

    def status_report(self):
        return {
            'name': self.name,
            'energy_level': self.energy_level,
            'crew_members': self.crew_members
        }

# Note: This class can be tested using the provided test suite with pytest.