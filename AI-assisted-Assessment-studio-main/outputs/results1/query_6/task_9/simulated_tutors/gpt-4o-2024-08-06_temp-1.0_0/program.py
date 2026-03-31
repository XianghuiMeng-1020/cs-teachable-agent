class MythicalLibrary:
    def __init__(self):
        self.filename = "mythical_creatures.txt"
        self.creatures = self._load_creatures()

    def _load_creatures(self):
        creatures = {}
        try:
            with open(self.filename, 'r') as f:
                for line in f:
                    creature_name, origin, description = line.strip().split(', ', 2)
                    creatures[creature_name.lower()] = {
                        'name': creature_name,
                        'origin': origin,
                        'description': description
                    }
        except FileNotFoundError:
            open(self.filename, 'w').close()  # Create the file if it does not exist
        return creatures

    def get_description(self, creature_name):
        creature = self.creatures.get(creature_name.lower())
        if creature:
            return creature['description']
        return "Creature not found"

    def add_creature(self, creature_name, origin, description):
        if creature_name.lower() in self.creatures:
            return "Creature already exists"
        with open(self.filename, 'a') as f:
            f.write(f"{creature_name}, {origin}, {description}\n")
        self.creatures[creature_name.lower()] = {
            'name': creature_name,
            'origin': origin,
            'description': description
        }
        return None

    def get_creatures_by_origin(self, origin):
        return [creature['name'] for creature in self.creatures.values() if creature['origin'].lower() == origin.lower()]
