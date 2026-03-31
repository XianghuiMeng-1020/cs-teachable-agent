class MythicalLibrary:
    def __init__(self, filename):
        self.filename = filename
        self.creatures = self.load_creatures() 

    def load_creatures(self):
        creatures = {}
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    name, origin, description = line.strip().split(', ', 2)
                    creatures[name.lower()] = (origin, description)
        except FileNotFoundError:
            with open(self.filename, 'w') as file:
                pass
        return creatures

    def get_description(self, creature_name):
        return self.creatures.get(creature_name.lower(), (None,))[1] or "Creature not found"

    def add_creature(self, creature_name, origin, description):
        if creature_name.lower() in self.creatures:
            return "Creature already exists"
        with open(self.filename, 'a') as file:
            file.write(f'{creature_name}, {origin}, {description}\n')
            self.creatures[creature_name.lower()] = (origin, description)

    def get_creatures_by_origin(self, origin):
        return [name for name, (orig, _) in self.creatures.items() if orig.lower() == origin.lower()]