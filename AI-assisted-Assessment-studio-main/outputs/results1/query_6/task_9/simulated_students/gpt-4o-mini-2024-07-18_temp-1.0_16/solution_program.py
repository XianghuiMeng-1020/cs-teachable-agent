class MythicalLibrary:
    def __init__(self, filename):
        self.filename = filename
        self.creatures = self.load_creatures()

    def load_creatures(self):
        creatures = {}
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    name, origin, description = line.strip().split(',', 2)
                    creatures[name.strip().lower()] = {'origin': origin.strip(), 'description': description.strip()}
        except FileNotFoundError:
            open(self.filename, 'w').close()
        return creatures

    def get_description(self, creature_name):
        creature_name = creature_name.strip().lower()
        if creature_name in self.creatures:
            return self.creatures[creature_name]['description']
        return 'Creature not found'

    def add_creature(self, creature_name, origin, description):
        creature_name = creature_name.strip().lower()
        if creature_name in self.creatures:
            return 'Creature already exists'
        self.creatures[creature_name] = {'origin': origin.strip(), 'description': description.strip()}
        with open(self.filename, 'a') as file:
            file.write(f'{creature_name.capitalize()}, {origin.strip()}, {description.strip()}\n')
        return 'Creature added'

    def get_creatures_by_origin(self, origin):
        origin = origin.strip().lower()
        return [name.capitalize() for name, data in self.creatures.items() if data['origin'].strip().lower() == origin]