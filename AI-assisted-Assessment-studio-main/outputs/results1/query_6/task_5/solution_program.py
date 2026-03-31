class MythologicalCreature:
    def __init__(self, name, origin, description):
        self.name = name
        self.origin = origin
        self.description = description

class CreaturesRepository:
    def __init__(self):
        self.creatures = []

    def add_creature(self, creature):
        self.creatures.append(creature)

    def remove_creature(self, name):
        self.creatures = [c for c in self.creatures if c.name != name]

    def load_from_file(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                name, origin, description = line.strip().split(';')
                creature = MythologicalCreature(name, origin, description)
                self.creatures.append(creature)

    def save_to_file(self, file_path):
        with open(file_path, 'w') as file:
            for creature in self.creatures:
                line = f"{creature.name};{creature.origin};{creature.description}\n"
                file.write(line)