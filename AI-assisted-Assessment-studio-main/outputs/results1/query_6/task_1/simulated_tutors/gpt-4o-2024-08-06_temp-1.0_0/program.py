class MythicalCreature:
    def __init__(self, name, type, origin, power):
        self.name = name
        self.type = type
        self.origin = origin
        self.power = power

class CreatureManager:
    def __init__(self):
        self.creatures = []

    def add_creature(self, name, type, origin, power):
        creature = MythicalCreature(name, type, origin, power)
        self.creatures.append(creature)

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            for creature in self.creatures:
                line = f"{creature.name},{creature.type},{creature.origin},{creature.power}\n"
                file.write(line)

    def load_from_file(self, filename):
        self.creatures = []
        with open(filename, 'r') as file:
            for line in file:
                name, type, origin, power = line.strip().split(',')
                self.add_creature(name, type, origin, power)