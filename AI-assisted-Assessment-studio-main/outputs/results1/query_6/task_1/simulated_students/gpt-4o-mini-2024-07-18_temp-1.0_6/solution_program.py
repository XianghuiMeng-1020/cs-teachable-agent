class MythicalCreature:
    def __init__(self, name, creature_type, origin, power):
        self.name = name
        self.creature_type = creature_type
        self.origin = origin
        self.power = power

class CreatureManager:
    def __init__(self):
        self.creatures = []

    def add_creature(self, name, creature_type, origin, power):
        creature = MythicalCreature(name, creature_type, origin, power)
        self.creatures.append(creature)

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            for creature in self.creatures:
                file.write(f"{creature.name},{creature.creature_type},{creature.origin},{creature.power}\n")

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            self.creatures = []
            for line in file:
                name, creature_type, origin, power = line.strip().split(',')
                self.add_creature(name, creature_type, origin, power)