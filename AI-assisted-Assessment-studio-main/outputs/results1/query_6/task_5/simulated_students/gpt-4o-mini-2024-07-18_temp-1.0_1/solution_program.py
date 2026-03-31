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
        self.creatures = [creature for creature in self.creatures if creature.name != name]

    def load_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    name, origin, description = line.strip().split(';')
                    creature = MythologicalCreature(name, origin, description)
                    self.add_creature(creature)
        except FileNotFoundError:
            pass

    def save_to_file(self, file_path):
        with open(file_path, 'w') as file:
            for creature in self.creatures:
                file.write(f'{creature.name};{creature.origin};{creature.description}\n')