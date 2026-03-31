class MythicalLibrary:
    def __init__(self, filename):
        self.filename = filename
        self.creatures = self._load_creatures()

    def _load_creatures(self):
        creatures = {}
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    name, origin, description = line.strip().split(', ', 2)
                    creatures[name.lower()] = {'origin': origin, 'description': description}
        except FileNotFoundError:
            with open(self.filename, 'w') as file:
                pass
        return creatures

    def get_description(self, creature_name):
        return self.creatures.get(creature_name.lower(), 'Creature not found')['description'] if creature_name.lower() in self.creatures else 'Creature not found'

    def add_creature(self, creature_name, origin, description):
        creature_name_lower = creature_name.lower()
        if creature_name_lower in self.creatures:
            return 'Creature already exists'
        else:
            self.creatures[creature_name_lower] = {'origin': origin, 'description': description}
            with open(self.filename, 'a') as file:
                file.write(f'{creature_name}, {origin}, {description}\n')
            return None

    def get_creatures_by_origin(self, origin):
        return [name for name, details in self.creatures.items() if details['origin'].lower() == origin.lower()]