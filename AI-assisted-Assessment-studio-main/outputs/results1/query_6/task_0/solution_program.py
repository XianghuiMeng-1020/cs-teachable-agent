class MythicalCreature:
    def __init__(self, name, origin, description):
        self.name = name
        self.origin = origin
        self.description = description

    def __str__(self):
        return f"Name: {self.name}, Origin: {self.origin}, Description: {self.description}"


class MythicalDatabase:
    def __init__(self):
        self.creatures = []

    def add_creature(self, name, origin, description):
        creature = MythicalCreature(name, origin, description)
        self.creatures.append(creature)

    def list_creatures(self):
        return [str(creature) for creature in self.creatures]

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            for creature in self.creatures:
                file.write(f"{creature.name}|{creature.origin}|{creature.description}\n")

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
        for line in lines:
            name, origin, description = line.strip().split('|')
            self.add_creature(name, origin, description)
