class MythicalLibrary:
    def __init__(self, filename='mythical_creatures.txt'):
        self.filename = filename
        self.creatures = self.load_creatures()

    def load_creatures(self):
        creatures = {}
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    parts = line.strip().split(', ')
                    if len(parts) == 3:
                        name, origin, description = parts
                        creatures[name.lower()] = (origin, description)
        except FileNotFoundError:
            pass
        return creatures

    def get_description(self, creature_name):
        key = creature_name.lower()
        if key in self.creatures:
            return self.creatures[key][1]
        return 'Creature not found'

    def add_creature(self, creature_name, origin, description):
        key = creature_name.lower()
        if key in self.creatures:
            return 'Creature already exists'
        self.creatures[key] = (origin, description)
        self.save_creatures()
        return 'Creature added successfully'

    def save_creatures(self):
        with open(self.filename, 'w') as file:
            for name, (origin, description) in self.creatures.items():
                file.write(f'{name}, {origin}, {description}\n')

    def get_creatures_by_origin(self, origin):
        return [name for name, (orig, _) in self.creatures.items() if orig.lower() == origin.lower()]